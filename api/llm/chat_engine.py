from api.llm.model_loader import load_model

def run_chat(message: str):
    model = load_model()
    response = model.chat(message)  # Mocked call
    return {"response": response}
