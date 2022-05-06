# Uso Básico de la Librería
Cada función está debidamente comentada, pero para no adentraros en código, resumo las funciones. 

`Declaración: LCD(d4, d5, d6, d7, en, rs)`

- `writeRAM(data=8bit array)`: Escribir directamente en la ram de escritura en pantalla, consultar datasheet para conocer los bits de cada char.
- `home()`: Devuelve cursor a inicio.
- `display(display="activa/desactiva pantalla", cursor="activa/desactiva vision del cursor", blink="activa/desactiva cursor blinking") 
  `: Función que configura el cursor, y la visión de la pantalla
- `moveCursor(direction="dirección a la que mover el cursor", times="veces que movemos el cursor") `: Mover cursor por la pantalla para posicionarnos.
- `clearDisplay() `: Limpia todos los chars de la pantalla, **importante** cada vez que queramos escribir en pantalla.
- `textLeftRight() `: Escritura de izquierda a derecha. (la buena)
- `textRightLeft() `: Escritura de derecha a izquierda.
- `writeMessage(string message) `: Llamada primordial para escribir chars en pantalla.