from utils.colors import Colors
from world.characters import NPC

class CommandHandler:
    """
    Procesa y ejecuta los comandos introducidos por el jugador.
    Esta versión utiliza una lógica de procesado más simple y fiable.
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
        # La palabra clave es la primera palabra, en minúsculas para que no importe si escribes "Ir" o "ir".
        keyword = parts[0].lower()
        # Los argumentos son TODO lo demás, exactamente como se escribió.
        args = parts[1] if len(parts) > 1 else ""

        method_to_call = getattr(self, f"do_{keyword}", None)
        
        if method_to_call:
            # Si encontramos un comando (ej: do_ir), lo llamamos con sus argumentos originales.
            method_to_call(args)
        else:
            # Si no, toda la línea de comando se considera una acción.
            self.do_action(command)

    def do_mirar(self, args: str):
        """Comando para mirar la sala."""
        print(self.player.room.get_description())

    def do_decir(self, args: str):
        """Comando para hablar. Ahora preserva la puntuación original."""
        if not args:
            print(f"{Colors.SYSTEM}¿Qué quieres decir? Uso: decir <mensaje>{Colors.RESET}")
            return
        
        event_display = f"{Colors.PLAYER}V (tú) dices: '{args}'{Colors.RESET}"
        event_log = f"V (el jugador) dijo: '{args}'"
        
        self.player.room.add_event(event_display, is_major=False)
        for char in self.player.room.characters:
            if isinstance(char, NPC):
                char.add_memory(event_log)

    def do_ir(self, args: str):
        """Comando para moverse. Limpia la entrada aquí dentro, donde es seguro."""
        # Limpiamos los espacios y convertimos a minúsculas solo el destino.
        destination_keyword = args.strip().lower()
        if not destination_keyword:
            print(f"{Colors.SYSTEM}¿A dónde quieres ir? Uso: ir <salida>{Colors.RESET}")
            return

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
        """Gestiona cualquier otra entrada como una acción física."""
        event_display = f"{Colors.PLAYER}V (tú) realiza la acción: '{action_text}'{Colors.RESET}"
        event_log = f"V (el jugador) realizó la acción: '{action_text}'"
        
        self.player.room.add_event(event_display, is_major=True)
        for char in self.player.room.characters:
            if isinstance(char, NPC):
                char.add_memory(event_log)