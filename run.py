# Autor victor Arbiol
# Titulo
# ──────────────────────────────────────────────────────────────────────────────────────
# 1.  Importaciones necesarias
# ──────────────────────────────────────────────────────────────────────────────────────
import requests   # para llamar a Ollama
import json

# ──────────────────────────────────────────────────────────────────────────────────────
# 2.  Clase Personaje (con el nuevo atributo)
# ──────────────────────────────────────────────────────────────────────────────────────
class Personaje:
    """Representa a un personaje del juego."""

    # ──────────────────────────────────────────────────────────────────────────────────────
    # Constructor
    # ──────────────────────────────────────────────────────────────────────────────────────
    def __init__(self,
                 nombre, fuerza, inteligencia,
                 defensa, vida, aguante, turno,
                 personalidad=None):
        self.nombre = nombre
        self.fuerza = fuerza
        self.inteligencia = inteligencia
        self.defensa = defensa
        self.vida = vida
        self.aguante = aguante
        self.turno = turno
        self.personalidad = personalidad   # <-- nuevo atributo

    # ──────────────────────────────────────────────────────────────────────────────────────
    # Método que muestra los datos
    # ──────────────────────────────────────────────────────────────────────────────────────
    def atributos(self):
        print("Nombre:", self.nombre)
        print("Fuerza:", self.fuerza)
        print("Inteligencia:", self.inteligencia)
        print("Defensa:", self.defensa)
        print("Vida:", self.vida)
        print("Aguante:", self.aguante)
        print("Turno:", self.turno)
        print("Personalidad:", self.personalidad)

    # ──────────────────────────────────────────────────────────────────────────────────────
    # Método que llama a Ollama y guarda la personalidad
    # ──────────────────────────────────────────────────────────────────────────────────────
    def obtener_personalidad_ollama(self, api_key="gemma3:4b"):
        """
        Llama a la API de Ollama y asigna la personalidad al personaje.
        """
        # Construimos la URL con la API key
        url = f"https://api.ollama.com/v1/personality?key={api_key}"
        # Parámetros opcionales: idioma (español), longitud, etc.
        payload = {
            "name": self.nombre,
            "language": "es",
            "length": "medium",
            "style": "persona"
        }
        # Hacemos la petición GET
        response = requests.get(url, params=payload)
        # Si la respuesta es exitosa
        if response.status_code == 200:
            data = response.json()          # suponemos que devuelve JSON
            # Extraemos el campo de personalidad
            self.personalidad = data.get("description", "Sin descripción")  # default
        else:
            print("¡Error al llamar a Ollama! Código:", response.status_code)

    # ──────────────────────────────────────────────────────────────────────────────────────
    # Métodos ya existentes (atacar, etc.) siguen igual
    # ──────────────────────────────────────────────────────────────────────────────────────
    def atacar(self, enemigo):
        daño = self.daño(enemigo)
        enemigo.vida -= daño
        print(self.nombre, "ha realizado un", daño, "puntos de daño a", enemigo.nombre)
        if enemigo.esta_vivo():
            print("La vida de", enemigo.nombre, "es", enemigo.vida)
        else:
            enemigo.morir()

    # ──────────────────────────────────────────────────────────────────────────────────────
    def daño(self, enemigo):
        return self.fuerza - enemigo.defensa

    # ──────────────────────────────────────────────────────────────────────────────────────
    def esta_vivo(self):
        return self.vida > 0

    def morir(self):
        self.vida = 0
        print(self.nombre, "ha muerto")

    def subir_nivel(self, fuerza, inteligencia, defensa):
        self.fuerza += fuerza
        self.inteligencia += inteligencia
        self.defensa += defensa

# ──────────────────────────────────────────────────────────────────────────────────────
# 3.  Instanciación de los personajes
# ──────────────────────────────────────────────────────────────────────────────────────
miPersonaje = Personaje(
    nombre="Bert",
    fuerza=14,
    inteligencia=130,
    defensa=40,
    vida=10,
    aguante=1,
    turno=True
)

miEnemigo = Personaje(
    nombre="Hogro",
    fuerza=15,
    inteligencia=1,
    defensa=5,
    vida=5,
    aguante=1,
    turno=False
)

# ──────────────────────────────────────────────────────────────────────────────────────
# 4.  Llamamos a Ollama para que cada personaje tenga su personalidad
# ──────────────────────────────────────────────────────────────────────────────────────
miPersonaje.obtener_personalidad_ollama()
miEnemigo.obtener_personalidad_ollama()

# ──────────────────────────────────────────────────────────────────────────────────────
# 5.  Probamos el juego
# ──────────────────────────────────────────────────────────────────────────────────────
miPersonaje.atributos()
miEnemigo.atributos()
