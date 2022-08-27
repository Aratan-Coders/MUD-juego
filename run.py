# Autor victor Arbiol
# Titulo
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
        print("Fuerza:",self.fuerza)
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

    def morir(self):
        self.vida = 0
        print(self.nombre, "ha muerto")

    def daño(self, enemigo):
        return self.fuerza - enemigo.defensa

    def atacar(self, enemigo):
        daño = self.daño(enemigo)
        enemigo.vida = enemigo.vida - daño
        print(self.nombre, "ha realizado un ", daño, "puntos de daño", enemigo.nombre)
        if enemigo.esta_vivo():
            print("La vida de: ", enemigo.nombre, " es ", enemigo.vida)
        else:
            enemigo.morir()

# Instanciar / llamar personajes "crea"
miPersonaje = Personaje("Bert", 14, 130, 40, 10,1, False)
miEnemigo = Personaje('Hogro',15,1,5,5,1, False)

# Muestra todo
#miPersonaje.atributos()

# Subir nivel
#miPersonaje.subir_nivel(1,2,4)

#miPersonaje.atributos()
#miEnemigo.atributos()
#print(f" vive = ", miPersonaje.esta_vivo() )
#miPersonaje.morir()
#miPersonaje.atributos()
#print(miPersonaje.daño(miEnemigo))
miPersonaje.atacar(miEnemigo)
miEnemigo.atributos()