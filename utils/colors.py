# utils/colors.py
from colorama import Fore, Style

# Definimos una paleta de colores para nuestro juego
# Usaremos colores brillantes (BRIGHT) para que destaquen sobre un fondo oscuro

class Colors:
    PLAYER = Fore.CYAN + Style.BRIGHT      # El jugador hablará en cian brillante
    NPC = Fore.YELLOW + Style.BRIGHT       # Los NPCs normales en amarillo brillante
    HOSTILE = Fore.RED + Style.BRIGHT      # Los enemigos en rojo brillante
    NARRATOR = Fore.MAGENTA + Style.BRIGHT # El Director/Narrador en magenta brillante
    SYSTEM = Fore.GREEN + Style.BRIGHT     # Mensajes del sistema en verde brillante
    RESET = Style.RESET_ALL                # Para resetear al color por defecto