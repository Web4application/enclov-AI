import os, yaml

def load_model():
    with open("model_config.yaml") as f:
        config = yaml.safe_load(f)
    provider = config.get("provider", "openai")
    model_name = config.get("model", "gpt-4")

    if provider == "openai":
        import openai
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        class OpenAIWrapper:
            def chat(self, message):
                response = openai.ChatCompletion.create(
                    model=model_name,
                    messages=[{"role": "user", "content": message}],
                    temperature=config.get("temperature", 0.7),
                    max_tokens=config.get("max_tokens", 2048)
                )
                return response.choices[0].message.content
        return OpenAIWrapper()

    raise ValueError(f"Unsupported provider: {provider}")
