**El algoritmo**

*Kruskal*: Algoritmo que consiste en la mezcla de las paredes de cada celda del grafo, de manera aleatoria
(con el uso de SEED y .random()) Siguiendo las siguientes normas:

    Analizo por cada pared: Las celdas que comparten esta pared, ya estan "conectadas" por otro lado? (por otro camino)
        Si lo estan: Dejo la pared intacta (si la rompo, armaria un bucle de caminos, por lo que el laberitno ya no seria perfecto.
        Si no lo estan: Rompo el muro (uniendo las celdas intervinientes en un mismo conjunto)

    Consideraciones: de toda celda que se analiza por primera vez, se convierte en Jefa de si misma:
        self.parent = self. Cada vez que esta habre un muro e interconecta una nueva celda, esta pasa a referenciar
        al mismo jefe que el de la anterior, que siempre sera la primera desde la que se inicio el cojunto, del cual
        ahora, pasara a ser parte.


    En cuanto a la salida. EL formato del output del maze-generator es en numeros hexadecimales, en la que cada
        valor representa el status de la totalidad de los muros que conforman una celda, donde se utiliza una
        mascara de bits y cada bit equivale a un muro segun su direccion cardinal:

        Bit 1 = N = 1
        Bit 2 = E = 2
        Bit 3 = S = 4
        Bit 4 = W = 8

    Entonces, la suma total de los valores relativos a cada Bit, señalaran el estado de los muros de la selda. Bit
    encendido(1) igual a muro existente(cerrado), bit apagado(0) igual a muro inexistente(abierto)


**COLOR_PALETTE & display()**

Ambas estructuras utilizan la formula \033[. Esta  Indica que lo que sigue no es texto comun, sino un comando de control.

En el caso de los colores, estos estan definidos por 3 valores, ej: "48;5;229m" Sus valores corresponden a:

    La estructura usa 3 partes principales separadas por punto y coma (;):

    1ro: Tipo de objetivo (48 o 38):
        38 significa Foreground (color del texto / letra).
        48 significa Background (color de fondo).

    2do: Formato elegido (5):
        El 5 le indica a la terminal que vas a usar la paleta extendida estándar de 256 colores (la paleta de 8 bits).

    3ro: Índice exacto del color (del 0 al 255):
        Ese número es el color específico que consultas de la tabla estándar de la terminal.

    Ejemplos:

        \033[48;5;17m: 48 (pinta el fondo), 5 (en modo 256 colores), 17 (que en la tabla es azul noche marino).
        \033[38;5;214m: 38 (pinta el texto), 5 (en modo 256 colores), 214 (que es el color naranja/oro vibrante).

    Al final siempre llevan la letra m, que es la manera de cerrar el comando de color o estilo en el estándar ANSI.


Navegacion por cursor de la terminal:

    En el caso de la navegacion a travez del cursor, por la terminal, tenemos otros comandos como
    "\033[{n_moves_up}A" en el que estoy indicandole una orden de movimiento al cursor de la terminal N veces
    en direccion hacia arriba, de fila en fila. En este caso, al haber primero impreso el maze, el cursor se
    encontrara en la ultima posicion, es decir en al ultima fila de la ultima columna. Por otro lado, al avanzar
    un movimiento en direccion hacia arriba el cursor automaticamente sube una fila Y se posiciona en la primer
    columna de la misma, (viajando a la linea superior en su primera posicion).

    Comandos:

        A es el comando estándar ANSI para "Mover el Cursor Hacia Arriba".
        C es el comando para "Mover el Cursor Hacia la Derecha".

        B es abajo
        D es izquierda.

    Ejs:
        Si digo \033[10A el cursor subira diez posiciones y se hubicara en la primera posicion de esta linea,
        a la izquierda del todo.


Comandos de CheckPoint: (save o unsave/return_to_checkpoint)

    El comandos de control \033[s (save checkpoint): 

        Lo que hace es grabar la posicion actual del cursor en la consola a modo checkpoint,
        para poder reubicar el cursor a esta posicion con una sola accion: comando de control \033[u


    El comando de control \033[u (un-save/restore_checkpoint):

        Lo que hace es retornar el cursor, de donde sea la posicion en que se encuentre en la terminal a la ultima
        posicion guardada de \033[s


Respecto a "flush=True": 
    Lo que estamos indicando aquí, en contexto de print() es que si utilizamos la flag end="" para neutralizar
    el \n por defecto de print(), lo que sucede es que print no soltara los printeos almacenados en su buffer
    interno, sino hasta que este se llene o aparezca un \n que fuerza el flush. Con esta flag, el print siempre
    que tenga algo por imprimir lo devolvera de manera directa una vez leida la linea, sin importarle cuantos datos
    se encuentran en ese momento en el buffer ni su ocupacion actual.  
