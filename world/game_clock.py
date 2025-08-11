# world/game_clock.py
import asyncio
from utils.colors import Colors

class GameClock:
    def __init__(self, world, master_ai, tick_speed_seconds=17):
        """
        Constructor del reloj del juego.
        """
        self.world = world
        self.master_ai = master_ai
        self.tick_speed_seconds = tick_speed_seconds
        print(f"{Colors.SYSTEM}Reloj del juego iniciado. Un 'tick' ocurrirá cada {tick_speed_seconds} segundos.{Colors.RESET}")

    async def start(self):
        """
        Bucle principal asíncrono que hace "latir" al mundo a intervalos regulares.
        """
        while True:
            await asyncio.sleep(self.tick_speed_seconds)
            self.tick()

    def tick(self):
        """
        Un "tick" representa un pulso de tiempo en el mundo del juego.
        Aquí es donde ocurren todas las actualizaciones automáticas.
        """
        print(f"\n{Colors.SYSTEM}--- TICK DEL MUNDO (Hora: {asyncio.get_event_loop().time():.0f}) ---{Colors.RESET}")
        
        # 1. El Director (MasterAI) actualiza la ambientación de cada sala con gente.
        for room in self.world['rooms']:
            if room.characters:
                self.master_ai.update(room)

        # 2. Los NPCs reaccionan al entorno y a los eventos recientes.
        for npc in self.world['npcs']:
            npc.update()
            
        # 3. ¡PERSISTENCIA! Guardamos el estado de cada NPC a su fichero JSON.
        #    Esto incluye su memoria y relaciones actualizadas.
        for npc in self.world['npcs']:
            npc.save_state()
            
        # 4. Limpiamos los eventos de la sala para el siguiente turno.
        for room in self.world['rooms']:
            room.clear_events()