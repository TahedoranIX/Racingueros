## CuentaRevoluciones
Cuentarevoluciones hecho con RPi zero W con pantalla lcd 16x2 y rotary-encoder. Funciona mediante OBDII.

### Que es? Como funciona?
Pantalla para coches sin cuentarevoluciones, que se conecta por el protocolo OBDII (todos los coches a partir de los 2000 tienen).

Mediante la librería LCD, podemos mostrar en pantalla todos los datos que escojamos del coche.

Mediante la librería Rotary Encoder, podemos interactuar con la pantalla mediante menús.

### Cambios

#### LCD Library
	Librería para controlador ST7066U hecha por mí. Al ser más específica que la Adafruit funciona a mayor velocidad.

#### Rotary encoder Library
	Le he realizado unos cambios para que funcione con el rotary conectado de GPIO -> GND y he añadido la función de botón para los rotary con botón.


#### Modelos 3D
	Modelos 3D en formato stl de la caja **Modelos**

#### Conexiones:
	Cableados a la RPi en carpeta **Images**

### Productos:
- [Librería OBD original](https://github.com/brendan-w/python-OBD)
- [Librería Rotary encoder original](https://github.com/nstansby/rpi-rotary-encoder-python)
- [Librería original LCD Adafruit](https://github.com/adafruit/Adafruit_Python_CharLCD)
- [Pantalla](https://es.aliexpress.com/item/32397063365.html?spm=a2g0o.productlist.0.0.779a3a31I4vpfB&algo_pvid=adf133c7-1ed9-4de1-b14b-2ab022e3496c&algo_exp_id=adf133c7-1ed9-4de1-b14b-2ab022e3496c-3&pdp_ext_f=%7B%22sku_id%22%3A%2212000026861398048%22%7D&pdp_pi=-1%3B1.9%3B-1%3B-1%40salePrice%3BEUR%3Bsearch-mainSearch): LCD 1602
- [Obd](https://es.aliexpress.com/item/4000809053108.html?spm=a2g0o.productlist.0.0.70e571ackddOMQ&algo_pvid=ea560480-3cf9-416e-9c37-55a7fe459be6&algo_exp_id=ea560480-3cf9-416e-9c37-55a7fe459be6-1&pdp_ext_f=%7B%22sku_id%22%3A%2212000025091114231%22%7D&pdp_pi=-1%3B4.22%3B-1%3B-1%40salePrice%3BEUR%3Bsearch-mainSearch): elm327
- [Rotativo](https://es.aliexpress.com/item/4000028678187.html?gatewayAdapt=glo2esp&spm=a2g0o.9042311.0.0.274263c0LgHA3h)

### Pruebas:
Useful to program without having to be in the car.
- [OBD VIRTUAL](https://github.com/Ircama/ELM327-emulator)
OBD II Codes.
- [OBD PIDs] (https://en.wikipedia.org/wiki/OBD-II_PIDs)

### Raspberry AP:
Useful to debug the RPi while it's in the box.
- [raspberry](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-routed-wireless-access-point)

### TODO:
#### POR HACER:
- Calcular el consumo dependiendo de cuanto esta pulsado el pedal de acelerador (variar mezcla esquetiometrica).
- El boton del cronometro va un poco raro debido a las condiciones de activación.
- Cambiar libreria del rotary.
- Boton pulsado 10s, entra en modo debug y el wifi de la raspberry se enciende.
#### EN PROCESO:
- Consumo de gasolina
