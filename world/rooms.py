from utils.colors import Colors

class Room:
    """
    Representa una localización o sala en el mundo del juego.
    Contiene a los personajes y gestiona los eventos que ocurren en ella.
    """
    def __init__(self, name, description, world):
        """
        Constructor de la sala.
        Guarda una referencia al 'mundo' para saber dónde está el jugador.
        """
        self.name = name
        self.description = description
        self.world = world
        self.characters = []
        self.recent_events = []
        self.major_event_occurred = False # Flag para eventos que cambian la escena

    def add_character(self, character):
        """Añade un personaje a la lista de la sala."""
        if character not in self.characters:
            self.characters.append(character)

    def remove_character(self, character):
        """Quita a un personaje de la lista de la sala."""
        if character in self.characters:
            self.characters.remove(character)

    def add_event(self, event_text, is_major=False):
        """
        Añade un evento a la sala. Los eventos 'mayores' le indican al
        Director de Juego que debe narrar la consecuencia de una acción.
        """
        self.recent_events.append(event_text)
        if is_major:
            self.major_event_occurred = True
        
        # Muestra el evento inmediatamente a los jugadores en la sala
        self.broadcast(event_text)

    def broadcast(self, message):
        """
        Muestra un mensaje, PERO SOLO si el jugador principal
        se encuentra físicamente en esta sala.
        """
        player = self.world.get("player")
        if player and player in self.characters:
            print(message)
        
    def clear_events(self):
        """
        Limpia la lista de eventos y resetea el flag de evento mayor.
        Se llama después de cada tick del juego.
        """
        self.recent_events = []
        self.major_event_occurred = False

    def get_description(self):
        """
        Genera la descripción completa de la sala para el comando 'mirar'.
        """
        # Nombre y descripción de la sala
        desc = f"\n{Colors.SYSTEM}--- {self.name} ---{Colors.RESET}\n"
        desc += f"{self.description}\n\n"
        
        # Personajes en la sala (excluyendo al propio jugador)
        other_characters = [c for c in self.characters if c.name != "V"]
        if other_characters:
            desc += "Ves a las siguientes personas aquí:\n"
            # Hacemos la lista más legible
            for char in other_characters:
                 desc += f"  - {Colors.NPC}{char.name}{Colors.RESET} ({char.description})\n"
        else:
            desc += "Estás a solas.\n"
            
        return desc