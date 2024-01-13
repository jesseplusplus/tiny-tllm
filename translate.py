#!/usr/bin/env python

import argparse
import os
import requests

# use temporary spaces API to test for now (will be replaced by a permanent API)
API_URL = "https://qgyd2021-multilingual-translation.hf.space/run/predict"

def query(payload):
    headers = {"Authorization": f"Bearer {os.environ['HUGGINGFACE_TOKEN']}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def translate_text(target: str, text: str, source: str) -> dict:
    """Translates text into the target language using the M2M100 model
    """
    payload = { "data": [text, source, target, "facebook/m2m100_418M"] }
    result = query(payload)
    print(result)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate text")
    parser.add_argument("target", help="target language")
    parser.add_argument("text", help="text to translate")
    parser.add_argument("source", help="source language")
    args = parser.parse_args()
    translate_text(args.target, args.text, args.source)
