import asyncio
import sys
import glob
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
    "player": None
}

def setup_world():
    """
    Crea el mundo, las salas, al jugador y carga dinámicamente
    a todos los NPCs desde sus ficheros .json.
    """
    print(f"{Colors.SYSTEM}Cargando Night City...{Colors.RESET}")
    
    # --- Creación de Salas ---
    coyote_cojo = Room("El Coyote Cojo", "Un bar de mala muerte, con olor a alcohol barato y sueños rotos. La música rock atrona desde una gramola.", world)
    callejon_lluvioso = Room("Callejón Lluvioso", "Un callejón oscuro y estrecho. El neón de los rascacielos apenas ilumina los charcos de agua sucia.", world)
    world["rooms"].extend([coyote_cojo, callejon_lluvioso])

    # --- Creación del Jugador ---
    player = Player("V")
    world["player"] = player
    player.room = coyote_cojo
    coyote_cojo.add_character(player)

    # --- Carga Dinámica de NPCs ---
    npc_files = glob.glob('world/npcs/*.json')
    print(f"{Colors.SYSTEM}Encontrados {len(npc_files)} perfiles de personaje para cargar...{Colors.RESET}")
    
    for file_path in npc_files:
        try:
            npc = NPC(file_path)
            world["npcs"].append(npc)
            if "maelstrom" in npc.name.lower():
                npc.room = callejon_lluvioso
            else:
                npc.room = coyote_cojo
            npc.room.add_character(npc)
            print(f"{Colors.SYSTEM}  - '{npc.name}' cargado y colocado en '{npc.room.name}'.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.HOSTILE}ERROR: No se pudo cargar el NPC desde {file_path}: {e}{Colors.RESET}")
    
    print(f"{Colors.SYSTEM}...Mundo cargado. ¡Bienvenido a Night City, V!{Colors.RESET}")
    print("=====================================================")
    print(f"{Colors.NARRATOR}Apareces en...{Colors.RESET}")
    print(player.room.get_description())

async def handle_player_input():
    """
    Bucle principal para la entrada del jugador, ahora robusto contra el cierre de la consola.
    """
    loop = asyncio.get_running_loop()
    command_handler = CommandHandler(world)

    while True:
        try:
            raw_input = await loop.run_in_executor(None, sys.stdin.readline)

            # --- ¡LA CORRECCIÓN ESTÁ AQUÍ! ---
            # Si raw_input es una cadena vacía, significa que el flujo de entrada
            # se ha cerrado (por ejemplo, con Ctrl+D en Linux o Ctrl+Z en Windows).
            if not raw_input:
                print(f"\n{Colors.SYSTEM}Flujo de entrada cerrado. Iniciando apagado...{Colors.RESET}")
                loop.stop() # Detenemos el bucle de eventos principal
                break       # Salimos del bucle while

            # El comando 'salir' también detiene el juego de forma controlada
            if raw_input.strip().lower() == "salir":
                print(f"{Colors.SYSTEM}Guardando estado final de los personajes...{Colors.RESET}")
                for npc in world['npcs']:
                    npc.save_state()
                print(f"{Colors.SYSTEM}Conexión terminada.{Colors.RESET}")
                loop.stop()
                break

            # Si hay texto, se lo pasamos al manejador de comandos
            if raw_input.strip():
                command_handler.execute(raw_input)
        
        except Exception as e:
            # Captura de cualquier otro error inesperado en el bucle de entrada
            print(f"{Colors.HOSTILE}Error en el bucle de entrada: {e}{Colors.RESET}")
            loop.stop()
            break


async def main():
    """
    Función principal que inicia el juego y todas las tareas asíncronas.
    """
    setup_world()
    master_ai = MasterAI()
    clock = GameClock(world, master_ai)

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