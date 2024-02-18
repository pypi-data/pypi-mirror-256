from typing import TYPE_CHECKING, Any, Dict, List, Optional

import torch
from aiconfig.callback import CallbackEvent
from aiconfig_extension_hugging_face.local_inference.util import get_hf_model
from transformers import Pipeline, pipeline

from aiconfig import InferenceOptions, ModelParser
from aiconfig.schema import (
    Attachment,
    AttachmentDataWithStringValue,
    ExecuteResult,
    Output,
    Prompt,
    PromptInput,
)

if TYPE_CHECKING:
    from aiconfig import AIConfigRuntime


class HuggingFaceAutomaticSpeechRecognitionTransformer(ModelParser):
    """
    Model Parser for HuggingFace ASR (Automatic Speech Recognition) models.
    """

    def __init__(self):
        """
        Returns:
            HuggingFaceAutomaticSpeechRecognitionTransformer

        Usage:
        1. Create a new model parser object with the model ID of the model to use.
                parser = HuggingFaceAutomaticSpeechRecognitionTransformer()
        2. Add the model parser to the registry.
                config.register_model_parser(parser)
        """
        super().__init__()
        self.pipelines: dict[str, Pipeline] = {}

    def id(self) -> str:
        """
        Returns an identifier for the Model Parser
        """
        return "HuggingFaceAutomaticSpeechRecognitionTransformer"

    async def serialize(
        self,
        prompt_name: str,
        data: Any,
        ai_config: "AIConfigRuntime",
        parameters: Optional[Dict[str, Any]] = None,
    ) -> List[Prompt]:
        """
        Defines how a prompt and model inference settings get serialized in the .aiconfig.
        Assume input in the form of input(s) being passed into an already constructed pipeline.

        Args:
            prompt (str): The prompt to be serialized.
            data (Any): Model-specific inference settings to be serialized.
            ai_config (AIConfigRuntime): The AIConfig Runtime.
            parameters (Dict[str, Any], optional): Model-specific parameters. Defaults to None.

        Returns:
            str: Serialized representation of the prompt and inference settings.
        """
        # TODO: See https://github.com/lastmile-ai/aiconfig/issues/822
        raise NotImplementedError(
            "serialize is not implemented for HuggingFaceAutomaticSpeechRecognitionTransformer"
        )

    async def deserialize(
        self,
        prompt: Prompt,
        aiconfig: "AIConfigRuntime",
        params: Optional[Dict[str, Any]] = {},
    ) -> Dict[str, Any]:
        await aiconfig.callback_manager.run_callbacks(
            CallbackEvent(
                "on_deserialize_start",
                __name__,
                {"prompt": prompt, "params": params},
            )
        )

        # Build Completion data
        model_settings = self.get_model_settings(prompt, aiconfig)
        [
            _pipeline_creation_params,
            unfiltered_completion_params,
        ] = refine_pipeline_creation_params(model_settings)
        completion_data = refine_asr_completion_params(
            unfiltered_completion_params
        )

        # ASR Pipeline supports input types of bytes, file path, and a dict containing raw sampled audio. Also supports multiple input
        # For now, support multiple or single uri's as input
        # TODO: Support or figure out if other input types are needed (base64, bytes), as well as the sampled audio dict
        # See api docs for more info:
        # - https://github.com/huggingface/transformers/blob/v4.36.1/src/transformers/pipelines/automatic_speech_recognition.py#L313-L317
        # - https://huggingface.co/docs/transformers/main_classes/pipelines#transformers.AutomaticSpeechRecognitionPipeline
        inputs = validate_and_retrieve_audio_from_attachments(prompt)

        completion_data["inputs"] = inputs

        await aiconfig.callback_manager.run_callbacks(
            CallbackEvent(
                "on_deserialize_complete",
                __name__,
                {"output": completion_data},
            )
        )
        return completion_data

    async def run(
        self,
        prompt: Prompt,
        aiconfig: "AIConfigRuntime",
        options: InferenceOptions,
        parameters: Dict[str, Any],
        **kwargs,
    ) -> list[Output]:
        await aiconfig.callback_manager.run_callbacks(
            CallbackEvent(
                "on_run_start",
                __name__,
                {
                    "prompt": prompt,
                    "options": options,
                    "parameters": parameters,
                },
            )
        )

        model_settings = self.get_model_settings(prompt, aiconfig)
        [pipeline_creation_data, _] = refine_pipeline_creation_params(
            model_settings
        )
        model_name = get_hf_model(aiconfig, prompt, self)
        key = model_name if model_name is not None else "__default__"

        if key not in self.pipelines:
            device = self._get_device()
            if pipeline_creation_data.get("device", None) is None:
                pipeline_creation_data["device"] = device
            self.pipelines[key] = pipeline(
                task="automatic-speech-recognition",
                model=model_name,
                **pipeline_creation_data,
            )

        asr_pipeline = self.pipelines[key]
        completion_data = await self.deserialize(prompt, aiconfig, parameters)

        response = asr_pipeline(**completion_data)

        # response is a list of text outputs. This can be tested by running an asr pipeline and noticing the outputs are a list of text.
        outputs = construct_outputs(response)

        prompt.outputs = outputs
        await aiconfig.callback_manager.run_callbacks(
            CallbackEvent(
                "on_run_complete", __name__, {"result": prompt.outputs}
            )
        )
        return prompt.outputs

    def _get_device(self) -> str:
        if torch.cuda.is_available():
            return "cuda"
        # Mps backend is not supported for all asr models. Seen when spinning up a default asr pipeline which uses facebook/wav2vec2-base-960h 55bb623
        return "cpu"

    def get_output_text(
        self,
        prompt: Prompt,
        aiconfig: "AIConfigRuntime",
        output: Optional[Output] = None,
    ) -> str:
        if output is None:
            output = aiconfig.get_latest_output(prompt)

        if output is None:
            return ""

        # TODO (rossdanlm): Handle multiple outputs in list
        # https://github.com/lastmile-ai/aiconfig/issues/467
        if output.output_type == "execute_result":
            output_data = output.data
            if isinstance(output_data, str):
                return output_data
        return ""


def validate_attachment_type_is_audio(attachment: Attachment):
    if not hasattr(attachment, "mime_type"):
        raise ValueError(
            f"Attachment has no mime type. Specify the audio mimetype in the aiconfig"
        )

    if not attachment.mime_type.startswith("audio/"):
        raise ValueError(
            f"Invalid attachment mimetype {attachment.mime_type}. Expected audio mimetype."
        )


def validate_and_retrieve_audio_from_attachments(prompt: Prompt) -> list[str]:
    """
    Retrieves the audio uri's or base64 from each attachment in the prompt input.

    Throws an exception if
    - attachment is not audio
    - attachment data is not a uri
    - no attachments are found
    - operation fails for any reason
    """

    if not isinstance(prompt.input, PromptInput):
        raise ValueError(
            f"Prompt input is of type {type(prompt.input) }. Please specify a PromptInput with attachments for prompt {prompt.name}."
        )

    if prompt.input.attachments is None or len(prompt.input.attachments) == 0:
        raise ValueError(
            f"No attachments found in input for prompt {prompt.name}. Please add an audio attachment to the prompt input."
        )

    audio_inputs: list[str] = []

    for i, attachment in enumerate(prompt.input.attachments):
        validate_attachment_type_is_audio(attachment)

        if not isinstance(attachment.data, AttachmentDataWithStringValue):
            raise ValueError(
                f"""Attachment data must be of type `AttachmentDataWithStringValue` with a `kind` and `value` field. 
                         Please specify a uri for the audio attachment in prompt {prompt.name}."""
            )

        audio_inputs.append(attachment.data.value)

    return audio_inputs


def refine_pipeline_creation_params(
    model_settings: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Refines the pipeline creation params for the HF text2Image generation api.
    Defers unsupported params as completion params, where they can get processed in
    `refine_image_completion_params()`. The supported keys were found by looking at
    the HF Pipelines AutomaticSpeechRecognition API:
    https://huggingface.co/docs/transformers/v4.36.1/en/main_classes/pipelines#transformers.AutomaticSpeechRecognitionPipeline

    Note that this is not the same as the image completion params, which are passed to
    the pipeline later to generate the image:
    https://huggingface.co/docs/transformers/v4.36.1/en/main_classes/pipelines#transformers.AutomaticSpeechRecognitionPipeline.__call__

    TODO: Distinguish pipeline creation and refine completion https://github.com/lastmile-ai/aiconfig/issues/825 https://github.com/lastmile-ai/aiconfig/issues/824
    """

    supported_keys = {
        "chunk_length_s",
        "decoder",
        "device",
        "framework",
        "feature_extractor",
        "stride_length_s",
        "tokenizer",
    }

    pipeline_creation_params: Dict[str, Any] = {}
    completion_params: Dict[str, Any] = {}
    for key in model_settings:
        if key.lower() in supported_keys:
            pipeline_creation_params[key.lower()] = model_settings[key]
        else:
            if key.lower() == "kwargs" and isinstance(
                model_settings[key], Dict
            ):
                completion_params.update(model_settings[key])
            else:
                completion_params[key.lower()] = model_settings[key]

    return [pipeline_creation_params, completion_params]


def refine_asr_completion_params(
    unfiltered_completion_params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Refines the ASR params for the HF asr generation api after a
    pipeline has been created via `refine_pipeline_creation_params`. Removes any
    unsupported params. The supported keys were found by looking at the HF asr
    API for asr pipelines:
    https://huggingface.co/docs/transformers/v4.36.1/en/main_classes/pipelines#transformers.AutomaticSpeechRecognitionPipeline

    Note that this is not the same as the pipeline completion params, which were passed
    earlier to generate the pipeline:
    https://huggingface.co/docs/transformers/v4.36.1/en/main_classes/pipelines#transformers.AutomaticSpeechRecognitionPipeline.__call__

    Note: This doesn't support base pipeline params like `num_workers`
    TODO: Figure out how to find which params are supported.

    TODO: Distinguish pipeline creation and refine completion
    https://github.com/lastmile-ai/aiconfig/issues/825
    https://github.com/lastmile-ai/aiconfig/issues/824
    """

    supported_keys = {
        # inputs
        "return_timestamps",
        "generate_kwargs",
        "max_new_tokens",
    }

    completion_params: Dict[str, Any] = {}
    for key in unfiltered_completion_params:
        if key.lower() in supported_keys:
            completion_params[key.lower()] = unfiltered_completion_params[key]

    return completion_params


def construct_outputs(response: list[Any]) -> list[Output]:
    """
    Constructs an output from the response of the HF ASR pipeline.

    Response from pipeline could contain multiple outputs and time stamps. No Docs found for this.
    """
    outputs: list[Output] = []

    if not isinstance(response, list):
        # response contains a single output. Found by testing variations of the asr pipeline
        response = [response]

    for i, result in enumerate(response):
        # response is expected to be a dict containing the text output and timestamps if specified. Could not find docs for this.
        result: dict[str, Any]
        text_output = (
            result.get("text")
            if "text" in result and isinstance(result, dict)
            else result
        )
        output = ExecuteResult(
            **{
                "output_type": "execute_result",
                "data": text_output,
                "execution_count": i,
                "metadata": {"result": result}
                if result.get("chunks", False)
                else {},  # may contain timestamps and chunks, for now pass result
            }
        )
        outputs.append(output)

    return outputs
