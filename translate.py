#!/usr/bin/env python

import argparse

def translate_text(target: str, text: str, source: str) -> dict:
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

    try:
        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(text, target_language=target)

        print(u"Result: {}".format(result["translatedText"]))
        return result
    except Exception as e:
        logger.exception(e)
        print("Google Translate failed, falling back to Helsinki-NLP LLM models")

        source_to_target_code = source + "-" + target
        model_name = "Helsinki-NLP/opus-mt-" + source_to_target_code
        translator = pipeline("translation", model=model_name)

        result = translator(text)
        print(u"Result: {}".format(result[0]["translation_text"]))
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate text")
    parser.add_argument("target", help="target language")
    parser.add_argument("text", help="text to translate")
    parser.add_argument("--source", required=False, help="source language")
    args = parser.parse_args()
    translate_text(args.target, args.text, args.source)
