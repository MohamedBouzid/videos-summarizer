import ollama

class LLMChat:
    def __init__(self, model="mistral"):
        self.model = model

    def ask(self, prompt):
        response = ollama.chat(
            model=self.model,
            messages=prompt
        )
        return response

