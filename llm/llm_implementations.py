import os
import json
import ollama
from openai import OpenAI
from llm.llm_interface import LLMInterface

class OllamaLLM(LLMInterface):
    def __init__(self, model):
        self.model = model

    def chat(self, messages, response_format):
        response = ollama.chat(model=self.model, messages=messages)
        return json.loads(response['message']['content'])

class OpenAILLM(LLMInterface):
    def __init__(self, model):
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chat(self, messages, response_format):
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=response_format
        )
        return completion.choices[0].message.parsed

class LLMFactory:
    @staticmethod
    def create_llm(model):
        if model.startswith("llama"):
            return OllamaLLM(model)
        elif model.startswith("gpt"):
            return OpenAILLM(model)
        else:
            raise ValueError(f"Unsupported model: {model}")
