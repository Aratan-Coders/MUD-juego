# Mud-Game
## Es una prueba de concepto escrita en python 3.x

La idea es hacer un MUD, juego de texto/consola tipo ROL.

hacer algo sencillo que funcione para mejorar mis habilidades
de programación en Python con POO, que pueda escalar y conectar a la red.

1. Por TCP/IP como servidor.
2. Usar el chat de youtube directos para las partidas.
3. Integración
4. En un futuro quizas añadirle una I.A.

### comandos

mirar

ir callejon

decir

pido

recibo, disoarar, escanear

le lanzo 

salir 
examinar <objeto>: Para ver la descripción de un objeto.
coger <objeto>: Para mover un objeto de la sala al inventario del jugador.
dejar <objeto>: Para mover un objeto del inventario a la sala.
inventario: Para ver lo que llevas encima.

intimidar al ganger


### Cómo Jugar la Misión

Reinicia el juego para cargar todos los nuevos ficheros y la lógica.

Habla con Jackie: No tienes que hacer nada. Como su active_quest está en 1, 

- su IA estará predispuesta a decirte algo como: "Choom, necesito un favor. Se me cayó un datapad en el callejón de al lado, es importante. ¿Puedes buscarlo?".
- 
Acepta (implícitamente): Ve al callejón con ir callejon.

Encuentra el objeto: Usa mirar. Verás que en la lista de objetos aparece "Datapad Corporativo".

Coge el objeto: Escribe coger datapad corporativo. El juego te dirá que lo has cogido y que tu misión se ha actualizado.

Comprueba tu estado: Escribe inventario (verás el datapad) y misiones (verás que la descripción ha cambiado a la etapa 2).

Vuelve con Jackie: Usa ir bar.

Entrega el objeto: Escribe dar datapad corporativo a jackie.

¡Misión completada! El juego te notificará. Si miras tus misiones ahora, verás que la descripción ha cambiado a la etapa 3. Jackie, en el próximo tick, podría darte las gracias.

