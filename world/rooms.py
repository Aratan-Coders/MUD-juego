# Este fichero define la clase 'Room', por lo que no necesita importarla.
# Solo importa las utilidades que usa, como los colores.
from utils.colors import Colors, strip_colors

class Room:
    """
    Representa una localización o sala en el mundo del juego.
    Contiene a los personajes y gestiona los eventos que ocurren en ella.
    """
    def __init__(self, id, name, description, world):
        self.id = id
        self.name = name
        self.description = description
        self.world = world
        self.characters = []
        self.recent_events = []
        self.major_event_occurred = False
        self.exits = {}

    def add_exit(self, direction, room_object):
        """Añade una salida desde esta sala a otra."""
        self.exits[direction] = room_object

    def get_description(self):
        """Genera la descripción completa, ahora incluyendo las salidas."""
        desc = f"\n{Colors.SYSTEM}--- {self.name} ---{Colors.RESET}\n"
        desc += f"{self.description}\n\n"
        
        other_characters = [c for c in self.characters if c.name != "V"]
        if other_characters:
            desc += "Ves a las siguientes personas aquí:\n"
            for char in other_characters:
                 desc += f"  - {Colors.NPC}{char.name}{Colors.RESET} ({char.description})\n"
        else:
            desc += "Estás a solas.\n"
        
        if self.exits:
            desc += f"\n{Colors.SYSTEM}Salidas obvias: {', '.join(self.exits.keys())}{Colors.RESET}\n"
            
        return desc
    
    def add_character(self, character):
        if character not in self.characters: self.characters.append(character)

    def remove_character(self, character):
        if character in self.characters: self.characters.remove(character)

    def add_event(self, event_text, is_major=False):
        self.recent_events.append(event_text)
        if is_major: self.major_event_occurred = True
        self.broadcast(event_text)

    def broadcast(self, message):
        """Muestra un mensaje al jugador y lo guarda en el log global."""
        log_message = f"[{self.name}] {strip_colors(message)}"
        self.world['global_log'].append(log_message)
        if len(self.world['global_log']) > 200:
            self.world['global_log'].pop(0)

        player = self.world.get("player")
        if player and player in self.characters:
            print(message)

    def clear_events(self):
        """Limpia la lista de eventos y resetea el flag de evento mayor."""
        self.recent_events = []
        self.major_event_occurred = False