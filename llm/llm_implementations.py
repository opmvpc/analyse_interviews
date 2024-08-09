import os
import json
import ollama
from openai import OpenAI
from llm.llm_interface import LLMInterface
from pydantic import ValidationError
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OllamaLLM(LLMInterface):
    def __init__(self, model):
        self.model = model

    def json(self, messages, response_format):
        logger.debug(f"Sending request to Ollama with model: {self.model}")
        response = ollama.chat(model=self.model, messages=messages)
        content = response['message']['content']
        logger.debug(f"Raw response from Ollama: {content}")

        # Extraire le JSON de la réponse
        start = content.find('{')
        end = content.rfind('}') + 1
        json_str = content[start:end]
        logger.debug(f"Extracted JSON: {json_str}")

        try:
            # Parse le JSON et valide avec Pydantic
            parsed_data = json.loads(json_str)
            logger.debug(f"Parsed data: {parsed_data}")
            validated_data = response_format(**parsed_data)
            logger.debug(f"Validated data: {validated_data}")
            return validated_data
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise ValueError(f"Invalid JSON: {e}")
        except ValidationError as e:
            logger.error(f"Pydantic validation error: {e}")
            raise ValidationError(f"Validation error: {e}")

class OpenAILLM(LLMInterface):
    def __init__(self, model):
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def json(self, messages, response_format):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_model=response_format
        )
        return completion.choices[0].message.model_dump()

class LLMFactory:
    @staticmethod
    def create_llm(model):
        if model.startswith("llama"):
            return OllamaLLM(model)
        elif model.startswith("gpt"):
            return OpenAILLM(model)
        else:
            raise ValueError(f"Unsupported model: {model}")
