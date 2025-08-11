from llm.ollama_client import OllamaClient
# --- CORRECCIÓN AQUÍ ---
# Importamos los nombres de función nuevos y correctos que existen en prompt_builder.py
from utils.prompt_builder import build_gm_ambient_prompt, build_gm_action_narration_prompt
from utils.colors import Colors

class MasterAI:
    """
    Actúa como el Director de Juego (Game Master).
    Narra las consecuencias de las acciones o describe el ambiente.
    """
    def __init__(self):
        self.llm_client = OllamaClient()

    def update(self, room):
        """
        Decide si narrar una acción o describir el ambiente
        basándose en si ha ocurrido un "evento mayor" en la sala.
        """
        # No narramos nada si el jugador no está físicamente en la sala
        if not any(c.name == "V" for c in room.characters):
            return

        prompt = ""
        # Lógica principal del Director de Juego
        if room.major_event_occurred:
            # Si ha ocurrido algo importante, usamos el prompt para narrar la acción
            prompt = build_gm_action_narration_prompt(room)
        else:
            # Si no, simplemente describimos el ambiente de la sala
            prompt = build_gm_ambient_prompt(room)
            
        # Generamos la respuesta de la IA y la mostramos
        narration_text = self.llm_client.generate_response(prompt).strip()
        narration_text = narration_text.replace('"', '').replace('*', '')
        message = f"{Colors.NARRATOR}[[ NARRADOR: {narration_text} ]]{Colors.RESET}"
        room.broadcast(message)