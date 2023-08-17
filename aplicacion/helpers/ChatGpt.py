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
        temperature = 0.7  # Controla la creatividad del modelo
        max_tokens = 4000  # Controla la longitud de la respuesta generada
        engine = "gpt-4" # Especifica el motor de inferencia GPT-3 5x turbo

        # Realizar la solicitud al modelo de lenguaje
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres el encargado de atencioón al publico de un restaurant"},
            {"role": "user", "content": f"{prompt}"}
        ]
        )

        # Imprime la respuesta
        print(response.choices[0].message['content'])
        return response.choices[0].message['content']