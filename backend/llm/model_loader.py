def load_model():
    class DummyModel:
        def chat(self, message):
            return f"Echo: {message}"
    return DummyModel()
