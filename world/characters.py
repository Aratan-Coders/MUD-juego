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
    La clase que representa al jugador. Carga y guarda su estado, incluyendo
    su inventario, estadísticas y un registro de sus misiones activas.
    """
    def __init__(self, json_path='world/player/data.json'):
        self.json_path = json_path
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"{Colors.HOSTILE}AVISO: No se encontró el fichero del jugador. Se creará uno nuevo.{Colors.RESET}")
            data = {
                "name": "V",
                "description": "Un/a mercenario/a con la mirada de quien ha visto demasiado.",
                "stats": {"Salud": 100, "Reflejos": 5, "Inteligencia": 5, "Temple": 5},
                "skills": {"Pistolas": 30, "Persuasion": 20, "Hacking": 15, "Pelea": 25},
                "inventory": [{"id": "arma_basica", "name": "Pistola Básica", "description": "Una pistola barata pero fiable."}],
                "active_quests": []
            }
            self.save_state_data(data)

        super().__init__(data['name'], data['description'])
        
        self.stats = data.get('stats', {})
        self.skills = data.get('skills', {})
        self.inventory = data.get('inventory', [])
        self.active_quests = data.get('active_quests', [])

    def save_state_data(self, data):
        """Función interna para guardar un diccionario de datos en el fichero JSON."""
        try:
            os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.HOSTILE}ERROR: No se pudo guardar el estado del jugador: {e}{Colors.RESET}")

    def save_state(self):
        """Construye el diccionario de estado actual y lo manda a guardar."""
        current_state = {
            "name": self.name, "description": self.description,
            "stats": self.stats, "skills": self.skills,
            "inventory": self.inventory, "active_quests": self.active_quests
        }
        self.save_state_data(current_state)

class NPC(Character):
    """
    Una clase compleja para Personajes No Jugadores, cuya IA es dirigida por
    su personalidad, memoria, metas y ahora, ¡misiones!
    """
    def __init__(self, json_path):
        self.json_path = json_path
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"{Colors.HOSTILE}ERROR: No se encontró el fichero de personaje: {json_path}{Colors.RESET}")
            data = {"name": "Entidad Perdida", "description": "Un error en la realidad."}
        
        super().__init__(data['name'], data['description'])
        
        self.personality = data.get('personality', 'No tengo personalidad definida.')
        self.is_hostile = data.get('is_hostile', False)
        self.goals = data.get('goals', [])
        self.relationships = data.get('relationships', {})
        self.memory_log = data.get('memory_log', [])
        self.schedule = data.get('schedule', [])
        # --- ¡CAMBIOS AQUÍ! ---
        self.active_quest = data.get('active_quest', None)
        self.quest_stage = data.get('quest_stage', 0)
        # Cargamos las estadísticas y habilidades del NPC
        self.stats = data.get('stats', {})
        self.skills = data.get('skills', {})
        self.llm_client = OllamaClient()

    def add_memory(self, event_summary):
        self.memory_log.append(event_summary)
        if len(self.memory_log) > 20: self.memory_log.pop(0)

    def save_state(self):
        """Guarda el estado completo del NPC, incluyendo el progreso de su misión."""
        state = {
            "id": self.name.lower().replace(" ", "_"),
            "name": self.name,
            "description": self.description,
            "is_hostile": self.is_hostile,
            "start_location": self.room.name if self.room else "",
            "schedule": self.schedule,
            "personality": self.personality,
            "goals": self.goals,
            "relationships": self.relationships,
            "memory_log": self.memory_log,
            # --- ¡CAMBIOS AQUÍ! ---
            "active_quest": self.active_quest,
            "quest_stage": self.quest_stage
        }
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.HOSTILE}ERROR: No se pudo guardar el estado para {self.name}: {e}{Colors.RESET}")

    def update(self):
        if not self.room: return
        prompt = build_npc_prompt(self, self.room)
        action_text = self.llm_client.generate_response(prompt).strip()
        action_text = action_text.replace('"', '').replace('*', '')
        color = Colors.HOSTILE if self.is_hostile else Colors.NPC
        message = f"{color}[{self.room.name}] {self.name} {action_text}{Colors.RESET}"
        self.room.broadcast(message)