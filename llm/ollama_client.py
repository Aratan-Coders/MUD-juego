# llm/ollama_client.py
import ollama

class OllamaClient:
    def __init__(self, model="gemma3:4b"):
        self.model = model

    # CAMBIO DE NOMBRE AQUÍ: 'generate_npc_action' se convierte en 'generate_response'
    def generate_response(self, prompt):
        """
        Genera una respuesta de texto usando el modelo de lenguaje.
        Esta es la función genérica para comunicarse con Ollama.
        """
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.85} # Un poco más de creatividad
            )
            return response['message']['content']
        except Exception as e:
            print(f"!! ERROR: No se pudo contactar con Ollama. Asegúrate de que está en ejecución. Detalle: {e}")
            return "..."