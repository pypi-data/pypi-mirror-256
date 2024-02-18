from .local_inference.automatic_speech_recognition import (
    HuggingFaceAutomaticSpeechRecognitionTransformer,
)
from .local_inference.image_2_text import HuggingFaceImage2TextTransformer
from .local_inference.text_2_image import HuggingFaceText2ImageDiffusor
from .local_inference.text_2_speech import HuggingFaceText2SpeechTransformer
from .local_inference.text_generation import (
    HuggingFaceTextGenerationTransformer,
)
from .local_inference.text_summarization import (
    HuggingFaceTextSummarizationTransformer,
)
from .local_inference.text_translation import (
    HuggingFaceTextTranslationTransformer,
)
from .local_inference.util import get_hf_model
from .remote_inference_client.image_2_text import (
    HuggingFaceImage2TextRemoteInference,
)
from .remote_inference_client.text_2_image import (
    HuggingFaceText2ImageRemoteInference,
)
from .remote_inference_client.text_2_speech import (
    HuggingFaceText2SpeechRemoteInference,
)
from .remote_inference_client.text_generation import (
    HuggingFaceTextGenerationRemoteInference,
)
from .remote_inference_client.text_summarization import (
    HuggingFaceTextSummarizationRemoteInference,
)
from .remote_inference_client.text_translation import (
    HuggingFaceTextTranslationRemoteInference,
)
from .remote_inference_client.automatic_speech_recognition import (
    HuggingFaceAutomaticSpeechRecognitionRemoteInference,
)
from .remote_inference_client.conversational import (
    HuggingFaceConversationalRemoteInference,
)

UTILS = [get_hf_model]

LOCAL_INFERENCE_CLASSES = [
    "HuggingFaceAutomaticSpeechRecognitionTransformer",
    "HuggingFaceImage2TextTransformer",
    "HuggingFaceText2ImageDiffusor",
    "HuggingFaceText2SpeechTransformer",
    "HuggingFaceTextGenerationTransformer",
    "HuggingFaceTextSummarizationTransformer",
    "HuggingFaceTextTranslationTransformer",
]

REMOTE_INFERENCE_CLASSES = [
    "HuggingFaceAutomaticSpeechRecognitionRemoteInference",
    "HuggingFaceImage2TextRemoteInference",
    "HuggingFaceConversationalRemoteInference",
    "HuggingFaceText2ImageRemoteInference",
    "HuggingFaceText2SpeechRemoteInference",
    "HuggingFaceTextGenerationRemoteInference",
    "HuggingFaceTextSummarizationRemoteInference",
    "HuggingFaceTextTranslationRemoteInference",
]
__ALL__ = LOCAL_INFERENCE_CLASSES + REMOTE_INFERENCE_CLASSES + UTILS
