import os
import glob
import json
import random
from utils.colors import Colors
from world.characters import NPC

class CommandHandler:
    def __init__(self, world):
        self.world = world
        self.player = world["player"]
        self.quests = self.load_quests()

    def load_quests(self):
        quests = {}
        quest_path = os.path.join('world', 'quests', '*.json')
        quest_files = glob.glob(quest_path)
        for file_path in quest_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    quests[data['id']] = data
            except Exception as e:
                print(f"{Colors.HOSTILE}ERROR: No se pudo cargar la misión desde {file_path}: {e}{Colors.RESET}")
        return quests

    def execute(self, raw_command: str):
        command = raw_command.strip()
        if not command: return
        parts = command.split(' ', 1)
        keyword = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        method_to_call = getattr(self, f"do_{keyword}", None)
        if method_to_call:
            method_to_call(args)
        else:
            self.do_action(command)

    def do_mirar(self, args: str):
        print(self.player.room.get_description())

    def do_decir(self, args: str):
        if not args: print(f"{Colors.SYSTEM}Uso: decir <mensaje>{Colors.RESET}"); return
        event_display = f"{Colors.PLAYER}V (tú) dices: '{args}'{Colors.RESET}"
        event_log = f"V (el jugador) dijo: '{args}'"
        self.player.room.add_event(event_display, is_major=False)
        for char in self.player.room.characters:
            if isinstance(char, NPC): char.add_memory(event_log)

    def do_ir(self, args: str):
        destination_keyword = args.strip().lower()
        if not destination_keyword: print(f"{Colors.SYSTEM}Uso: ir <salida>{Colors.RESET}"); return
        current_room = self.player.room
        target_room = current_room.exits.get(destination_keyword)
        if target_room:
            action_text = f"V (tú) se va hacia '{destination_keyword}'."
            current_room.add_event(action_text, is_major=True)
            current_room.remove_character(self.player)
            target_room.add_character(self.player)
            self.player.room = target_room
            print(target_room.get_description())
        else:
            print(f"{Colors.SYSTEM}No ves una salida llamada '{destination_keyword}' desde aquí.{Colors.RESET}")

    def do_action(self, action_text: str):
        event_display = f"{Colors.PLAYER}V (tú) realiza la acción: '{action_text}'{Colors.RESET}"
        event_log = f"V (el jugador) realizó la acción: '{action_text}'"
        self.player.room.add_event(event_display, is_major=True)
        for char in self.player.room.characters:
            if isinstance(char, NPC): char.add_memory(event_log)

    def do_examinar(self, args: str):
        target_name = args.strip().lower()
        if not target_name: print(f"{Colors.SYSTEM}Uso: examinar <objeto>{Colors.RESET}"); return
        item_found = next((item for item in self.player.inventory if target_name in item['name'].lower()), None)
        if not item_found:
            item_found = next((obj for obj in self.player.room.objects if target_name in obj['name'].lower()), None)
        if item_found:
            print(f"{Colors.PLAYER}Examinas {item_found['name']}:{Colors.RESET} {item_found['description']}")
        else:
            print(f"No ves ningún '{args}' por aquí.")

    def do_coger(self, args: str):
        target_name = args.strip().lower()
        item_to_get = next((obj for obj in self.player.room.objects if target_name in obj['name'].lower()), None)
        if not item_to_get: print(f"No hay ningún '{args}' en esta sala."); return
        if not item_to_get.get('can_be_taken', False): print(f"No puedes coger {item_to_get['name']}."); return
        self.player.room.remove_object(item_to_get)
        self.player.inventory.append(item_to_get)
        print(f"Has cogido: {Colors.PLAYER}{item_to_get['name']}{Colors.RESET}.")
        if item_to_get['id'] == 'datapad_corporativo':
            jackie = next((c for c in self.world['npcs'] if c.name == "Jackie Welles" and c.active_quest == 'q001' and c.quest_stage == 1), None)
            if jackie:
                print(f"{Colors.SYSTEM}¡OBJETIVO DE MISIÓN ACTUALIZADO!{Colors.RESET}")
                jackie.quest_stage = 2
                self.player.active_quests.append({'id': 'q001', 'stage': 2, 'description': self.quests['q001']['stages']['2']['description']})

    def do_dar(self, args: str):
        parts = args.split(" a ");
        if len(parts) < 2: print(f"{Colors.SYSTEM}Uso: dar <objeto> a <personaje>{Colors.RESET}"); return
        item_name = parts[0].strip().lower()
        npc_name = parts[1].strip().lower()
        item_to_give = next((item for item in self.player.inventory if item_name in item['name'].lower()), None)
        if not item_to_give: print(f"No tienes '{parts[0]}' en tu inventario."); return
        npc_target = next((npc for npc in self.player.room.characters if isinstance(npc, NPC) and npc_name in npc.name.lower()), None)
        if not npc_target: print(f"No hay nadie llamado '{parts[1]}' aquí."); return
        print(f"Le das {item_to_give['name']} a {npc_target.name}.")
        self.player.inventory.remove(item_to_give)
        if npc_target.name == "Jackie Welles" and item_to_give['id'] == 'datapad_corporativo' and npc_target.active_quest == 'q001' and npc_target.quest_stage == 2:
            print(f"{Colors.SYSTEM}¡MISIÓN COMPLETADA: {self.quests['q001']['name']}!{Colors.RESET}")
            npc_target.quest_stage = 3; npc_target.active_quest = None
            for quest in self.player.active_quests:
                if quest['id'] == 'q001': quest['stage'] = 3; quest['description'] = self.quests['q001']['stages']['3']['description']
            reaction_event = f"{Colors.NPC}[{self.player.room.name}] Jackie Welles: ¡Lo encontraste, choom! ¡Preem!{Colors.RESET}"
            self.player.room.add_event(reaction_event); npc_target.add_memory("Le di las gracias a V por encontrar el datapad.")

    def do_misiones(self, args: str):
        print(f"\n{Colors.SYSTEM}--- Diario de Misiones ---{Colors.RESET}")
        if not self.player.active_quests: print("No tienes ninguna misión activa.")
        else:
            for quest in self.player.active_quests:
                quest_name = self.quests.get(quest['id'], {}).get('name', 'Misión Desconocida')
                status_color = Colors.SYSTEM if quest['stage'] >= 3 else Colors.PLAYER
                status_text = "(Completada)" if quest['stage'] >= 3 else "(Activa)"
                print(f"- {status_color}{quest_name} {status_text}{Colors.RESET}: {quest['description']}")
        print(f"{Colors.SYSTEM}------------------------{Colors.RESET}")

    def do_preguntar(self, args: str):
        parts = args.split(" sobre ");
        if len(parts) < 2: print(f"{Colors.SYSTEM}Uso: preguntar a <personaje> sobre <tema>{Colors.RESET}"); return
        npc_name_parts = parts[0].split(" a ");
        if len(npc_name_parts) < 2: print(f"{Colors.SYSTEM}Uso: preguntar a <personaje> sobre <tema>{Colors.RESET}"); return
        npc_name = npc_name_parts[1].strip().lower()
        topic = parts[1].strip().lower()
        npc_target = next((npc for npc in self.player.room.characters if isinstance(npc, NPC) and npc_name in npc.name.lower()), None)
        if not npc_target: print(f"No hay nadie llamado '{npc_name}' aquí."); return
        question_event_display = f"{Colors.PLAYER}Le preguntas a {npc_target.name} sobre '{topic}'.{Colors.RESET}"
        question_event_log = f"V (el jugador) me preguntó sobre '{topic}'."
        self.player.room.add_event(question_event_display); npc_target.add_memory(question_event_log)
        print(f"Le preguntas a {npc_target.name} sobre '{topic}'. Esperas su respuesta...")

    def do_inventario(self, args: str):
        print(f"\n{Colors.SYSTEM}--- Inventario ---{Colors.RESET}")
        if not self.player.inventory: print("No llevas nada encima.")
        else:
            for item in self.player.inventory:
                print(f"- {Colors.PLAYER}{item.get('name', 'N/A')}{Colors.RESET} ({item.get('description', 'N/A')})")
        print(f"{Colors.SYSTEM}------------------{Colors.RESET}")

    def do_stats(self, args: str):
        print(f"\n{Colors.SYSTEM}--- Ficha de Personaje: {self.player.name} ---{Colors.RESET}")
        print(f"{Colors.PLAYER}Atributos:{Colors.RESET}")
        if self.player.stats:
            for stat, value in self.player.stats.items(): print(f"  - {stat}: {value}")
        else: print("  Sin atributos definidos.")
        print(f"\n{Colors.PLAYER}Habilidades:{Colors.RESET}")
        if self.player.skills:
            for skill, value in self.player.skills.items(): print(f"  - {skill}: {value}")
        else: print("  Sin habilidades definidas.")
        print(f"{Colors.SYSTEM}----------------------------------{Colors.RESET}")
        
    def do_escanear(self, args: str):
        target_name = args.strip().lower()
        if not target_name: print(f"{Colors.SYSTEM}Uso: escanear <personaje>{Colors.RESET}"); return
        npc_target = next((npc for npc in self.player.room.characters if isinstance(npc, NPC) and target_name in npc.name.lower()), None)
        if not npc_target: print(f"No hay nadie llamado '{args}' aquí."); return
        print(f"Inicias un escaneo rápido sobre {npc_target.name}...")
        hacking_skill = self.player.skills.get("Hacking", 0)
        difficulty = 50
        roll = hacking_skill + random.randint(1, 20)
        if roll >= difficulty:
            print(f"{Colors.SYSTEM}¡Escaneo exitoso!{Colors.RESET}")
            print(f"{Colors.PLAYER}--- Ficha de Objetivo: {npc_target.name} ---{Colors.RESET}")
            if hasattr(npc_target, 'stats'):
                print(f"  {Colors.PLAYER}Atributos:{Colors.RESET}")
                for stat, value in npc_target.stats.items(): print(f"    - {stat}: {value}")
            if hasattr(npc_target, 'skills'):
                print(f"  {Colors.PLAYER}Habilidades:{Colors.RESET}")
                for skill, value in npc_target.skills.items(): print(f"    - {skill}: {value}")
            print(f"{Colors.SYSTEM}----------------------------------{Colors.RESET}")
        else:
            print(f"{Colors.HOSTILE}Escaneo fallido. Tu software no es lo bastante bueno o han detectado la intrusión.{Colors.RESET}")

    def do_disparar(self, args: str):
        target_name = args.replace(" a ", "").strip().lower()
        if not target_name: print(f"{Colors.SYSTEM}Uso: disparar <personaje>{Colors.RESET}"); return
        npc_target = next((npc for npc in self.player.room.characters if isinstance(npc, NPC) and target_name in npc.name.lower()), None)
        if not npc_target: print(f"No hay nadie llamado '{args}' aquí."); return
        action_text = f"V (tú) dispara a {npc_target.name}"
        event_display = f"{Colors.PLAYER}{action_text}{Colors.RESET}"
        event_log = f"V (el jugador) me disparó."
        self.player.room.add_event(event_display, is_major=True)
        npc_target.add_memory(event_log)
        print(f"Apuntas a {npc_target.name} y aprietas el gatillo...")