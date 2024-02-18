import copy
import json
from typing import TYPE_CHECKING, Any, List, Optional

# HuggingFace API imports
from huggingface_hub import InferenceClient

from aiconfig import CallbackEvent
from aiconfig.default_parsers.parameterized_model_parser import (
    ParameterizedModelParser,
)
from aiconfig.model_parser import InferenceOptions
from aiconfig.schema import (
    ExecuteResult,
    Output,
    Prompt,
    PromptMetadata,
)
from aiconfig.util.config_utils import get_api_key_from_environment
from aiconfig.util.params import resolve_prompt


# Circuluar Dependency Type Hints
if TYPE_CHECKING:
    from aiconfig.Config import AIConfigRuntime


# Step 1: define Helpers
def refine_completion_params(model_settings: dict[Any, Any]) -> dict[str, Any]:
    """
    Refines the completion params for the HF text summarization api. Removes any unsupported params.
    See https://huggingface.co/docs/api-inference/detailed_parameters#summarization-task for supported params.
    """

    supported_keys = {
        "model",
        # "parameters" will contain dict of remaining completion params, see parameters_keys
    }

    parameters_keys = {
        "min_length",
        "max_length",
        "top_k",
        "top_p",
        "temperature",
        "repetition_penalty",
        "max_time",
        "options",  # sub-dict containing use_cache, wait_for_model (all optional)
    }

    completion_data = {}
    for key in model_settings:
        if key.lower() in supported_keys:
            completion_data[key.lower()] = model_settings[key]
        elif key.lower() in parameters_keys:
            parameters = completion_data.get("parameters", {})
            parameters[key.lower()] = model_settings[key]
            completion_data["parameters"] = parameters

    # The default model in HF is sshleifer/distilbart-cnn-12-6, which raises a
    # KeyError, "summary_text", when calling the inference client.
    # Instead, default to the model (which supports remote inference) with the
    # most "likes" in HF
    # https://huggingface.co/models?pipeline_tag=summarization&sort=likes
    if completion_data.get("model") is None:
        completion_data["model"] = "facebook/bart-large-cnn"

    return completion_data


def construct_output(response: str) -> Output:
    metadata: dict[str, str] = {"raw_response": response}

    output = ExecuteResult(
        **{
            "output_type": "execute_result",
            "data": response,
            "execution_count": 0,
            "metadata": metadata,
        }
    )
    return output


class HuggingFaceTextSummarizationRemoteInference(ParameterizedModelParser):
    """
    A model parser for HuggingFace text summarization models.
    """

    def __init__(self, model_id: str = None, use_api_token=False):
        """
        Args:
            model_id (str): The model ID of the model to use.
            no_token (bool): Whether or not to require an API token. Set to False if you don't have an api key.

        Returns:
            HuggingFaceTextSummarizationRemoteInference: The HuggingFaceTextSummarizationRemoteInference object.

        Usage:

        1. Create a new model parser object with the model ID of the model to use.
                parser = HuggingFaceTextSummarizationRemoteInference("facebook/bart-large-cnn", use_api_token=False)
        2. Add the model parser to the registry.
                config.register_model_parser(parser)

        If use_api_token is set to True, then the model parser will require an API token to be set in the environment variable HUGGING_FACE_API_TOKEN.


        """
        super().__init__()

        token = None

        if use_api_token:
            # You are allowed to use Hugging Face for a bit before you get
            # rate limited, in which case you will receive a clear error
            token = get_api_key_from_environment(
                "HUGGING_FACE_API_TOKEN", required=False
            ).unwrap()

        self.client = InferenceClient(model_id, token=token)

    def id(self) -> str:
        """
        Returns an identifier for the Model Parser
        """
        return "HuggingFaceTextSummarizationRemoteInference"

    async def serialize(
        self,
        prompt_name: str,
        data: Any,
        ai_config: "AIConfigRuntime",
        parameters: Optional[dict[Any, Any]] = None,
        **kwargs,
    ) -> list[Prompt]:
        """
        Defines how a prompt and model inference settings get serialized in the .aiconfig.

        Args:
            prompt (str): The prompt to be serialized.
            inference_settings (dict): Model-specific inference settings to be serialized.

        Returns:
            str: Serialized representation of the prompt and inference settings.
        """
        await ai_config.callback_manager.run_callbacks(
            CallbackEvent(
                "on_serialize_start",
                __name__,
                {
                    "prompt_name": prompt_name,
                    "data": data,
                    "parameters": parameters,
                    "kwargs": kwargs,
                },
            )
        )

        # assume data is completion params for HF text generation
        prompt_input = data["text"]

        # actual completion params are nested under 'parameters' key, so
        # extract them and merge them with the rest of the settings
        settings = copy.deepcopy(data)
        if "parameters" in settings:
            completion_params = settings["parameters"]
            settings.update(completion_params)
            settings.pop("parameters", None)

        # text is handled, remove from settings
        settings.pop("text", None)

        prompts = []

        model_metadata = ai_config.get_model_metadata(settings, self.id())
        prompt = Prompt(
            name=prompt_name,
            input=prompt_input,
            metadata=PromptMetadata(
                model=model_metadata, parameters=parameters, **kwargs
            ),
        )

        prompts.append(prompt)

        await ai_config.callback_manager.run_callbacks(
            CallbackEvent(
                "on_serialize_complete", __name__, {"result": prompts}
            )
        )

        return prompts

    async def deserialize(
        self,
        prompt: Prompt,
        aiconfig: "AIConfigRuntime",
        params: Optional[dict[Any, Any]] = {},
    ) -> dict[Any, Any]:
        """
        Defines how to parse a prompt in the .aiconfig for a particular model
        and constructs the completion params for that model.

        Args:
            serialized_data (str): Serialized data from the .aiconfig.

        Returns:
            dict: Model-specific completion parameters.
        """
        await aiconfig.callback_manager.run_callbacks(
            CallbackEvent(
                "on_deserialize_start",
                __name__,
                {"prompt": prompt, "params": params},
            )
        )

        resolved_prompt = resolve_prompt(prompt, params, aiconfig)

        # Build Completion data
        model_settings = self.get_model_settings(prompt, aiconfig)

        completion_data = refine_completion_params(model_settings)

        completion_data["text"] = resolved_prompt

        await aiconfig.callback_manager.run_callbacks(
            CallbackEvent(
                "on_deserialize_complete",
                __name__,
                {"output": completion_data},
            )
        )

        return completion_data

    async def run_inference(
        self,
        prompt: Prompt,
        aiconfig: "AIConfigRuntime",
        options: InferenceOptions,
        parameters: dict[Any, Any],
    ) -> List[Output]:
        """
        Invoked to run a prompt in the .aiconfig. This method should perform
        the actual model inference based on the provided prompt and inference settings.

        Args:
            prompt (str): The input prompt.
            inference_settings (dict): Model-specific inference settings.

        Returns:
            InferenceResponse: The response from the model.
        """
        sanitized_options = copy.deepcopy(options)
        run_override_api_token = getattr(sanitized_options, "api_token", None)
        # Redact api token from logs if it exists
        if run_override_api_token:
            setattr(sanitized_options, "api_token", "hf_********")

        await aiconfig.callback_manager.run_callbacks(
            CallbackEvent(
                "on_run_start",
                __name__,
                {
                    "prompt": prompt,
                    "options": sanitized_options,
                    "parameters": parameters,
                },
            )
        )

        # Summarization api doesn't support stream
        completion_data = await self.deserialize(prompt, aiconfig, parameters)

        # If api token is provided in the options, use it for the client
        client = self.client
        if run_override_api_token:
            client = InferenceClient(
                self.client.model, token=run_override_api_token
            )

        response = client.summarization(**completion_data)

        # HF Text Summarization api doesn't support multiple outputs. Expect only one output.
        # Output spec: response is literal string
        outputs = [construct_output(response)]

        prompt.outputs = outputs

        await aiconfig.callback_manager.run_callbacks(
            CallbackEvent("on_run_complete", __name__, {"result": outputs})
        )

        return outputs

    def get_output_text(
        self,
        prompt: Prompt,
        aiconfig: "AIConfigRuntime",
        output: Optional[Output] = None,
    ) -> str:
        if not output:
            output = aiconfig.get_latest_output(prompt)

        if not output:
            return ""

        if output.output_type == "execute_result":
            output_data = output.data
            if isinstance(output_data, str):
                return output_data

            # HuggingFace summarization outputs should only ever be string
            # format so shouldn't get here, but just being safe
            return json.dumps(output_data, indent=2)
        return ""
