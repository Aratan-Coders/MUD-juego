import json
import os
from llm.ollama_client import OllamaClient
from utils.prompt_builder import build_npc_prompt
from utils.colors import Colors

class Character:
    """
    Clase base para cualquier entidad viviente en el mundo (Jugadores y NPCs).
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.room = None

class Player(Character):
    """
    La clase que representa al jugador. Por ahora es simple, pero se puede expandir.
    """
    def __init__(self, name, description="Te ves en un espejo roto. Eres tú."):
        super().__init__(name, description)

class NPC(Character):
    """
    Una clase compleja para Personajes No Jugadores.
    Su personalidad, memoria y estado se cargan y guardan en un fichero JSON.
    """
    def __init__(self, json_path):
        """
        El constructor carga el estado inicial del NPC desde un fichero JSON.
        """
        self.json_path = json_path
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"{Colors.HOSTILE}ERROR: No se encontró el fichero de personaje: {json_path}{Colors.RESET}")
            # Salimos o creamos un estado por defecto para evitar un crash total
            data = {"name": "Entidad Perdida", "description": "Un error en la realidad."}
        
        # Inicializamos los atributos base desde el fichero
        super().__init__(data['name'], data['description'])
        
        # Cargamos los nuevos atributos de personalidad, memoria y metas
        self.personality = data.get('personality', 'No tengo personalidad definida.')
        self.is_hostile = data.get('is_hostile', False)
        self.goals = data.get('goals', [])
        self.relationships = data.get('relationships', {})
        self.memory_log = data.get('memory_log', [])
        self.schedule = data.get('schedule', [])
        # Cada NPC tiene su propio cliente para hablar con la IA
        self.llm_client = OllamaClient()

    def update_relationship(self, character_name, value):
        """
        Modifica la relación con otro personaje y la guarda.
        Por ejemplo: `npc.update_relationship("V", -5)` si el jugador le ataca.
        """
        if character_name not in self.relationships:
            self.relationships[character_name] = 0
        self.relationships[character_name] += value
        # print(f"{Colors.SYSTEM}Debug: Relación de {self.name} con {character_name} ahora es {self.relationships[character_name]}{Colors.RESET}")


    def add_memory(self, event_summary):
        """
        Añade un recuerdo al log de memoria del personaje.
        Para evitar una memoria infinita, mantenemos solo los últimos 20 recuerdos.
        """
        self.memory_log.append(event_summary)
        
        if len(self.memory_log) > 20:
            self.memory_log.pop(0) # Elimina el recuerdo más antiguo

    def save_state(self):
        """
        Guarda el estado actual completo del NPC (memoria, relaciones, etc.)
        de vuelta a su fichero JSON, haciéndolo persistente.
        """
        state = {
            "id": self.name.lower().replace(" ", "_"),
            "name": self.name,
            "description": self.description,
            "is_hostile": self.is_hostile,
            "personality": self.personality,
            "goals": self.goals,
            "relationships": self.relationships,
            "memory_log": self.memory_log
        }
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.HOSTILE}ERROR: No se pudo guardar el estado para {self.name}: {e}{Colors.RESET}")


    def update(self):
        """
        El "latido" del NPC. Decide qué hacer basándose en su estado completo.
        """
        if not self.room:
            return

        # 1. Construye el prompt usando toda la información del personaje.
        prompt = build_npc_prompt(self, self.room)
        
        # 2. Obtiene la acción o diálogo desde el modelo de lenguaje.
        action_text = self.llm_client.generate_response(prompt).strip()
        
        # 3. Limpia y formatea la respuesta.
        action_text = action_text.replace('"', '').replace('*', '')
        
        # 4. Elige un color según la hostilidad.
        color = Colors.HOSTILE if self.is_hostile else Colors.NPC
            
        # 5. Crea y emite el mensaje final.
        message = f"{color}[{self.room.name}] {self.name} {action_text}{Colors.RESET}"
        self.room.broadcast(message)