import asyncio
import sys
import glob
import json
import colorama
from world.rooms import Room
from world.characters import NPC, Player
from world.game_clock import GameClock
from world.master_ai import MasterAI
from utils.colors import Colors
from commands.commands import CommandHandler

# El diccionario del mundo que contiene todo el estado del juego
world = {
    "rooms": [],
    "npcs": [],
    "player": None,
    "time": 18,
    "global_log": []
}

def setup_world():
    """
    Crea el mundo cargando dinámicamente las salas y los NPCs desde
    sus respectivos ficheros JSON, asegurando que las salidas se conecten.
    Esta versión es más robusta y da más información durante la carga.
    """
    print(f"{Colors.SYSTEM}Iniciando la carga del mundo...{Colors.RESET}")
    
    # --- Carga de Salas desde 'world/rooms/' en DOS PASOS ---
    room_path = 'world/rooms/*.json'
    print(f"{Colors.SYSTEM}Buscando ficheros de sala en: '{room_path}'{Colors.RESET}")
    room_files = glob.glob(room_path)
    print(f"{Colors.SYSTEM}Ficheros encontrados: {len(room_files)} -> {room_files}{Colors.RESET}")
    
    if not room_files:
        print(f"{Colors.HOSTILE}FATAL: No se encontraron ficheros de sala en la carpeta 'world/rooms/'. El mundo no puede ser creado.{Colors.RESET}")
        return False # Indicamos que la carga falló

    room_data_map = {} # Guardará los datos crudos del JSON para el segundo paso

    # PASO 1: Crear todos los objetos Room para que existan en memoria.
    for file_path in room_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            room_data_map[data['id']] = data
            room_obj = Room(data['id'], data['name'], data['description'], world)
            world['rooms'].append(room_obj)

    # PASO 2: Ahora que todas las salas existen, conectamos sus salidas.
    for room_obj in world['rooms']:
        exit_data = room_data_map[room_obj.id].get('exits', {})
        for direction, target_room_id in exit_data.items():
            target_room_obj = next((r for r in world['rooms'] if r.id == target_room_id), None)
            if target_room_obj:
                room_obj.add_exit(direction.lower(), target_room_obj)

    print(f"{Colors.SYSTEM}Cargadas {len(world['rooms'])} salas y conectadas las salidas.{Colors.RESET}")

    # --- Creación del Jugador y Colocación Inicial ---
    player = Player("V")
    world["player"] = player
    start_room = next((r for r in world['rooms'] if r.id == 'el_coyote_cojo'), None)
    if start_room:
        player.room = start_room
        start_room.add_character(player)
    else:
        print(f"{Colors.HOSTILE}FATAL: La sala de inicio con id 'el_coyote_cojo' no se encontró entre los ficheros JSON cargados. El jugador no puede ser colocado.{Colors.RESET}")
        return False

    # --- Carga y Colocación Automática de NPCs ---
    npc_files = glob.glob('world/npcs/*.json')
    print(f"{Colors.SYSTEM}Cargando {len(npc_files)} perfiles de personaje...{Colors.RESET}")
    for file_path in npc_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f: npc_data = json.load(f)
            location_name = npc_data.get("start_location")
            target_room = next((room for room in world["rooms"] if room.name == location_name), None)
            if location_name and target_room:
                npc = NPC(file_path)
                world["npcs"].append(npc)
                npc.room = target_room
                target_room.add_character(npc)
                print(f"{Colors.SYSTEM}  - '{npc.name}' cargado en '{target_room.name}'.{Colors.RESET}")
            else:
                print(f"{Colors.HOSTILE}AVISO: No se pudo colocar al NPC de {file_path}. La sala '{location_name}' no existe o no fue cargada.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.HOSTILE}ERROR al procesar {file_path}: {e}{Colors.RESET}")
    
    print(f"{Colors.SYSTEM}...Mundo cargado. ¡Bienvenido a Night City, V!{Colors.RESET}")
    print("=====================================================")
    print(player.room.get_description())
    return True # Indicamos que la carga fue exitosa

async def handle_player_input():
    loop = asyncio.get_running_loop()
    command_handler = CommandHandler(world)
    while True:
        raw_input = await loop.run_in_executor(None, sys.stdin.readline)
        if not raw_input:
            print(f"\n{Colors.SYSTEM}Flujo de entrada cerrado. Iniciando apagado...{Colors.RESET}")
            loop.stop(); break
        if raw_input.strip().lower() == "salir":
            print(f"{Colors.SYSTEM}Guardando estado final...{Colors.RESET}")
            for npc in world['npcs']: npc.save_state()
            print(f"{Colors.SYSTEM}Conexión terminada.{Colors.RESET}")
            loop.stop(); break
        if raw_input.strip():
            command_handler.execute(raw_input)

async def main():
    if not setup_world(): # Si la carga del mundo falla, no continuamos
        print(f"{Colors.HOSTILE}La inicialización del mundo ha fallado. Revisa los ficheros y la configuración. El programa se cerrará.{Colors.RESET}")
        return

    master_ai = MasterAI()
    clock = GameClock(world, master_ai, tick_speed_seconds=30)
    
    game_loop_task = asyncio.create_task(clock.start())
    player_input_task = asyncio.create_task(handle_player_input())
    
    await asyncio.gather(game_loop_task, player_input_task, return_exceptions=True)

if __name__ == "__main__":
    colorama.init()
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, RuntimeError):
        print(f"\n{Colors.SYSTEM}Cierre forzoso. ¡Hasta la próxima, choom!{Colors.RESET}")
    finally:
        colorama.deinit()