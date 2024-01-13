#!/usr/bin/env python

def translate_text(target: str, text: str, source=None: str) -> dict:
    """Translates text into the target language using Google Cloud Translate
    API. Falls back to Helsinki-NLP LLM models if that fails.

    Target and source must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages

    Returns a dictionary with the result, containing:
      input: the input text
      translatedText: the translated output text
      detectedSourceLanguage: the detected language of the input text
    """
    from google.cloud import translate_v2 as translate
    from transformers import pipeline
    import logging

    logger = logging.getLogger(__name__)

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    try
        # Text can also be a sequence of strings, in which case this method
    	# will return a sequence of results for each text.
    	result = translate_client.translate(text, target_language=target)

        return result
    except Exception as e:
	logger.exception()

	source_to_target_code = source + "-" + target
	model_name = "Helsinki-NLP/opus-mt-" + source_to_target_code
	translator = pipeline("translation", model=model_name)

	return translator(text)

