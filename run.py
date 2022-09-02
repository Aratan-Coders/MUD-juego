# Autor victor Arbiol
# Titulo
import time
import random
#from typing_extensions import Self

print("Loibra mundo de Luz \n")

# Clase personaje


class Personaje:

    # Inicializador Atributos
    def __init__(self,
                 nombre, fuerza, inteligencia,
                 defensa, vida, aguante, turno):
        # Metodo
        self.nombre = nombre
        self.fuerza = fuerza
        self.inteligencia = inteligencia
        self.defensa = defensa
        self.vida = vida
        self.aguante = vida * fuerza
        self.turno = True

    def atributos(self):

        print("Nombre: ", self.nombre)
        print("Fuerza:", self.fuerza)
        print("Inteligencia", self.inteligencia)
        print(f"defensa:", self.defensa)
        print(f"vida:", self.vida)
        print(f"aguante:", self.aguante)
        print(f"turno:", self.turno)

    def subir_nivel(self, fuerza, inteligencia, defensa):
        self.fuerza = self.fuerza + fuerza
        self.inteligencia = self.inteligencia + inteligencia
        self.defensa = self.defensa + defensa

    def esta_vivo(self):
        return self.vida > 0

    def daño(self, enemigo):
        return self.fuerza - enemigo.defensa

    def atacar(self, enemigo):
        daño = self.daño(enemigo)
        enemigo.vida = enemigo.vida - daño
        print(self.nombre, "ha realizado un ", daño,
              "puntos de daño", enemigo.nombre)
        if enemigo.esta_vivo():
            print("La vida de: ", enemigo.nombre, " es ", enemigo.vida)
        else:
            enemigo.morir()

    def morir(self):
        self.vida = 0
        self.inteligencia = 0
        self.fuerza = 0
        self.espada = 0
        self.libro = 0
        print(self.nombre, "ha muerto")
        pass


class Guerrero(Personaje):
    # Aqui ponemos las peculiaridades de cara Raza de Guerrero
    def __init__(self, nombre, fuerza, inteligencia, defensa, vida, aguante, turno, espada):
        super().__init__(nombre, fuerza, inteligencia, defensa, vida, aguante, turno)

        self.inventario = {
            "Objeto_1": 0,
            "Objeto_2": 4
        }
        self.espada = espada
        self.nivel = 0
        self.experiencia = 0
        self.hold = 0
        self.anterior_criterio_subida = 10
        self.criterio_subida_nivel = 10

# daño de la espada

    def daño(self, enemigo):
        return self.fuerza * self.espada - enemigo.defensa

# daño del arma segun su material
    def cambiar_arma(self):
        opcion = int(
            input("Elige un arma: 1. Espada de Acero, 2. Cuchillo de Vanadio"))
        if opcion == 1:
            self.espada = 10
        elif opcion == 2:
            self.espada = 12
        else:
            print('Tu opcion no existe')


class Mago(Personaje):
    # Aqui ponemos las peculiaridades de cara Raza de Guerrero
    def __init__(self, nombre, fuerza, inteligencia, defensa, vida, aguante, turno, libro):
        super().__init__(nombre, fuerza, inteligencia, defensa, vida, aguante, turno)
        self.libro = libro
# daño de la espada

    def daño(self, enemigo):
        return self.inteligencia * self.libro - enemigo.defensa


jugador = Personaje("David", 10, 15, 10, 100, 1, False)
mago = Mago('Mago', 15, 15, 10, 100, 1, False, 5)
troll = Guerrero('Troll', 20, 10, 10, 100, 1, False, 5)

# Lucha


def combate(luchador1, luchador2):
    turno = 0
    while luchador1.esta_vivo() and luchador2.esta_vivo():
        print(luchador1.nombre, ">>>", luchador2.nombre)
        luchador1.atacar(luchador2)
        time.sleep(5)
        if luchador2.vida == 0:
            print("\n", luchador1.nombre, "Ha Ganado !!!")
            # subir experiencia
            luchador1.experiencia += 6
            break
        else:
            print(luchador1.nombre, "<<<", luchador2.nombre)
            luchador2.atacar(luchador1)

    turno = turno + 1


def check_nivel(self):
    print(f"El nivel actual es {self.nivel}")


def check_experiencia(self, experiencia):
    self.experiencia += experiencia
    if self.experiencia >= self.criterio_subida_nivel:
        self.subeNivel()


def subeNivel(self):
    """
    Esta clase aumenta el nivel de nuestro personaje y además actualiza el criterio para el siguiente nivel
    :return:
    """
    self.nivel += 1

    self.hold = self.criterio_subida_nivel
    self.criterio_subida_nivel = self.criterio_subida_nivel + \
        self.anterior_criterio_subida
    self.anterior_criterio_subida = self.hold
# fin codigo

# aleatorio
#rnd = random.sample(['Alien', 'Desactivado'], counts=[4, 2], k=5)


def mapa(self,pasos):
    x = 0
    plano = [0, 3, 1, 0, 0, 0, 0,
             0, 2, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, ]
    if plano[pasos] == 1:
        x = "te llevas religuia"
    elif plano[pasos] == 2:
        x = "no puedes pasar"
    elif plano[pasos] == 3:
        x = "Hospital"
        self.vida += 100
    return x


def suerte():
    dados = random.randint(1, 10)
    return dados


print(suerte())
# Historia:
intro = f'''
Vas en una bave de la confederación minera de Marte, estás con tus compañeros en 
HiperSueño de camino a cada, Tierra2 despues de 4 lasgos año sacando Hidrogeno Pesado
 salta una alarma y te despierta solo a ti:  . describe a tu personaje, una 
 fortajeza y una debilidad, como es y que relación tiene con
'''
print(intro)
#entrada = input("Personaje:")
# print(entrada)


# llamada a combate
print("Experiencia", troll.experiencia)

combate(troll, mago)
print("Experiencia", troll.experiencia)

combate(troll, jugador)
print("Experiencia", troll.experiencia)

print("...", troll.vida)
print(mapa(troll, 1))
print("Hospital", troll.vida)
#print(f"Libro de hechizos:", mago.libro)


# troll.cambiar_arma()
# troll.atributos()
#print(f"espada power:", troll.espada)


#TODO: Pruebas
# Instanciar / llamar personajes "crea"
#miPersonaje = Personaje("Bert", 14, 130, 40, 10,1, False)
#miEnemigo = Personaje('Hogro',15,1,5,5,1, False)
#miConsejero = Personaje('Druida',15,1,5,5,1, False)
# Muestra todo
# miPersonaje.atributos()

# Subir nivel
# miPersonaje.subir_nivel(1,2,4)

# miPersonaje.atributos()
# miEnemigo.atributos()
#print(f" vive = ", miPersonaje.esta_vivo() )
# miPersonaje.morir()
# miPersonaje.atributos()
# print(miPersonaje.daño(miEnemigo))
# miPersonaje.atacar(miEnemigo)
# miEnemigo.atributos()
# miConsejero.atributos()
