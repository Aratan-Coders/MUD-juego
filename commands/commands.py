from utils.colors import Colors
from world.characters import NPC

class CommandHandler:
    """
    Procesa y ejecuta los comandos introducidos por el jugador.
    """
    def __init__(self, world):
        self.world = world
        self.player = world["player"]

    def execute(self, raw_command: str):
        """
        Analiza un comando en crudo y lo delega a la función 'do_' apropiada.
        """
        command = raw_command.strip()
        if not command:
            return

        parts = command.split(' ', 1)
        keyword = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        # Busca una función en esta clase que se llame 'do_<keyword>'
        # Por ejemplo, para el comando 'mirar', busca 'self.do_mirar'
        method_to_call = getattr(self, f"do_{keyword}", None)
        
        if method_to_call:
            # Si se encuentra un método (ej. do_mirar), lo llama con sus argumentos
            method_to_call(args)
        else:
            # Si no es un comando conocido (como 'mirar', 'decir', 'ir'),
            # lo trata como una acción física genérica.
            self.do_action(raw_command)

    def do_mirar(self, args: str):
        """Comando para mirar la sala."""
        print(self.player.room.get_description())

    def do_decir(self, args: str):
        """Comando para hablar."""
        if not args:
            print(f"{Colors.SYSTEM}¿Qué quieres decir? Uso: decir <mensaje>{Colors.RESET}")
            return
        
        # El evento que se muestra en pantalla, con colores
        event_display = f"{Colors.PLAYER}V (tú) dices: '{args}'{Colors.RESET}"
        # El evento que se guarda en la memoria del NPC, sin colores
        event_log = f"V (el jugador) dijo: '{args}'"
        
        self.player.room.add_event(event_display, is_major=False) # Hablar no es una acción 'mayor'
        for char in self.player.room.characters:
            if isinstance(char, NPC):
                char.add_memory(event_log)

    def do_ir(self, args: str):
        """Comando para moverse a otra localización."""
        destination_name = args.strip().lower()
        if not destination_name:
            print(f"{Colors.SYSTEM}¿A dónde quieres ir? Uso: ir <lugar>{Colors.RESET}")
            return

        current_room = self.player.room
        target_room = None
        
        # Lógica de movimiento simple. Esto podría ser un mapa en el futuro.
        for room in self.world["rooms"]:
            if destination_name in room.name.lower() and room != current_room:
                target_room = room
                break

        if target_room:
            # Crea un evento 'mayor' para que el Director de Juego lo narre
            action_text = f"V (tú) decide ir a {target_room.name}."
            self.player.room.add_event(action_text, is_major=True)
            
            # Mueve al jugador de una sala a otra
            current_room.remove_character(self.player)
            target_room.add_character(self.player)
            self.player.room = target_room
        else:
            print(f"{Colors.SYSTEM}No parece que puedas ir a '{args}' desde aquí.{Colors.RESET}")
            
    def do_action(self, action_text: str):
        """Gestiona cualquier otra entrada como una acción física."""
        event_display = f"{Colors.PLAYER}V (tú) realiza la acción: '{action_text}'{Colors.RESET}"
        event_log = f"V (el jugador) realizó la acción: '{action_text}'"
        
        # Las acciones físicas siempre son eventos 'mayores' para el Director
        self.player.room.add_event(event_display, is_major=True)
        for char in self.player.room.characters:
            if isinstance(char, NPC):
                char.add_memory(event_log)