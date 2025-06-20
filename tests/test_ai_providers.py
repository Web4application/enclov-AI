import pytest
from providers.openai_provider import call_openai
from providers.googleai_provider import call_google_ai
from providers.enclovai_provider import call_enclovai

def test_openai():
    prompt = "Say hello from OpenAI"
    result = call_openai(prompt)
    assert "hello" in result.lower()

def test_google_ai():
    prompt = "Say hello from Google AI"
    result = call_google_ai(prompt)
    assert "hello" in result.lower()

def test_enclovai():
    prompt = "Say hello from EnclovAI"
    result = call_enclovai(prompt)
    assert "hello" in result.lower()
