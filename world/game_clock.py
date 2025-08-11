import asyncio
from utils.colors import Colors

class GameClock:
    def __init__(self, world, master_ai, tick_speed_seconds=30):
        self.world = world
        self.master_ai = master_ai
        self.tick_speed_seconds = tick_speed_seconds
        print(f"{Colors.SYSTEM}Motor de Vida Propia iniciado. Un 'tick' ocurrirá cada {tick_speed_seconds} segundos.{Colors.RESET}")

    async def start(self):
        while True:
            await asyncio.sleep(self.tick_speed_seconds)
            self.tick()

    def tick(self):
        # 1. AVANZAR LA HORA MUNDIAL
        self.world['time'] = (self.world['time'] + 1) % 24 # Ciclo de 24 horas
        current_time = self.world['time']
        
        print(f"\n{Colors.SYSTEM}--- TICK DEL MUNDO (Hora: {current_time}:00) ---{Colors.RESET}")

        # 2. PROCESAR LA VIDA AUTÓNOMA DE LOS NPCS
        self.process_npc_schedules(current_time)

        # 3. El Director narra las consecuencias o el ambiente
        for room in self.world['rooms']:
            self.master_ai.update(room)

        # 4. Los NPCs reaccionan al tick
        for npc in self.world['npcs']:
            npc.update()
            
        # 5. Guardamos el estado
        for npc in self.world['npcs']:
            npc.save_state()
            
        # 6. Limpiamos los eventos
        for room in self.world['rooms']:
            room.clear_events()

    def process_npc_schedules(self, current_time):
        """Comprueba el horario de cada NPC y ejecuta acciones si es la hora."""
        for npc in self.world['npcs']:
            if not hasattr(npc, 'schedule'): continue # Si el NPC no tiene horario, saltamos

            for schedule_entry in npc.schedule:
                # Comprobación robusta: se asegura de que el tiempo sea un número
                schedule_time = schedule_entry.get("time")
                if isinstance(schedule_time, int) and schedule_time == current_time:
                    
                    target_location_id = schedule_entry.get("location_id")
                    new_goal = schedule_entry.get("goal", "Seguir mi rutina.")
                    
                    target_room = next((r for r in self.world['rooms'] if r.id == target_location_id), None)
                    
                    if not target_room:
                        print(f"{Colors.HOSTILE}AVISO: La sala con id '{target_location_id}' del horario de {npc.name} no existe.{Colors.RESET}")
                        continue

                    # Actualizamos la meta principal del NPC
                    if npc.goals: npc.goals[0] = new_goal
                    else: npc.goals.append(new_goal)

                    # Si el NPC no está ya en su destino, lo movemos
                    if npc.room != target_room:
                        old_room = npc.room
                        
                        event_msg = f"{npc.name} se mueve de '{old_room.name}' a '{target_room.name}' como parte de su rutina."
                        print(f"{Colors.SYSTEM}VIDA AUTÓNOMA: {event_msg}{Colors.RESET}")
                        
                        # Creamos eventos para que el Director los narre
                        if old_room: old_room.add_event(f"{npc.name} mira a su alrededor y se va.", is_major=True)
                        target_room.add_event(f"{npc.name} entra en la sala.", is_major=True)
                        
                        if old_room: old_room.remove_character(npc)
                        target_room.add_character(npc)
                        npc.room = target_room
                    
                    break # Solo una acción del horario por tick