import openai
# from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
# load_dotenv()
class GPT():
    
    @staticmethod
    def consultar_chatgpt(prompt):
        # return prompt
        # Configura la clave de API de OpenAI
        openai.api_key = "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"
        model_engine = "text-davinci-002"  # El ID del modelo y motor de inferencia
        prompt = prompt #"Hello, I'm a language model created by OpenAI. What can I help you with today?"  # El texto de entrada para el modelo
        temperature = 0.9  # Controla la creatividad del modelo
        max_tokens = 4000  # Controla la longitud de la respuesta generada
        engine = "text-davinci-003" # Especifica el motor de inferencia GPT-3 5x turbo

        # Realizar la solicitud al modelo de lenguaje
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Obtener la respuesta generada por el modelo
        output = response.choices[0].text.strip()

        # Imprimir la respuesta generada por el modelo
        print(output)
        return output