class mapa:

	def miPosicion(self, pos):
		self.pos += pos
		pass

	def plano(self,cardinal):
		x = 0
		posicion = 9 
		if cardinal == "n":
			posicion -= 7
		if cardinal == "s":
			posicion += 7
		if cardinal == "e":
			posicion += 1
		if cardinal == "o":
			posicion -= 1

		plano = [
			0, 1 ,  2,  3,  4,  5,  6,
			7, 8 ,  9, 10, 11, 12, 13,
			14,15, 16, 17, 18, 19, 20,
			21,22, 23, 24, 25, 26, 27,
			0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 
			]
		
		if plano[posicion] == 1:
			x = "te llevas religuia"
		elif plano[posicion] == 2:
			x = "no puedes pasar"
		elif plano[posicion] == 3:
			x = "Hospital"
			#self.vida += 100
		#posicion a acumular
		#mapa.miPosicion(plano[posicion])
		dondeEsta = plano[posicion]
		return x, dondeEsta

print(mapa.plano("troll", "n"))
print(mapa.plano("troll", "s"))
print(mapa.plano("troll", "s"))
print(mapa.plano("troll", "s"))
print(mapa.plano("troll", "e"))
print(mapa.plano("troll", "o"))