
25/04/26

[CREAR ISUE] -> Laura
EL save_to_file() tiene alguna incompatibilidad con el maze.tx harcodeado, siendo que ya existe un self.output_file
configurado en el ConfigFormat del maze_generator.py  

[ISSUE] -> 
En a-maze-ing.py hay metodo y variable con nombres identicos.
La salida del error, deberia indicar salida no exitosa, no? EL mensaje de error es entendible, pero creo que deberia
de indicar que fallo algo en su funcionamiento, aparte del print.

[ISSUE]

    "Arreglar encapsulamiento de los _metodos". En a-maze-ing.py 
    El error fue hacer el motor interno pero obligar a que el archivo principal (a_maze_ing.py) llame a esos procesos
    uno por uno. Eso rompe un principio llamado Encapsulamiento.

    Lo que debería haber pasado es que en a_maze_ing.py solo llames a una función pública, por ejemplo
    maze.build(), y adentro de la clase Maze, ese método se encargue de llamar internamente a los métodos protegidos
    self._generate_maze(), etc.

Pendientes: 


Validar límites estructurales del patrón 42
Objetivo: evitar estados inválidos de generación.
Acción: validar dimensiones mínimas antes de bloquear patrón.
Criterio de cierre: error claro y temprano para tamaños no compatibles.

Resolver modo dinámico animado vs instantáneo
Objetivo: evitar rotura visual por terminal chica.
Acción: medir viewport y forzar instant_solution cuando no alcance alto/ancho.
Criterio de cierre: en terminal pequeña no se rompe la animación, cae en modo instantáneo.

Harden de calidad
Objetivo: asegurar estabilidad.
Acción: pruebas manuales con casos: maze chico, grande, random_color true, instant true/false, salida de archivo.
Criterio de cierre: contrato UI + archivo consistente en todos los casos.



-----
24/04/26

1. ¿Por qué el nombre is_static (es_estático)?
El nombre viene de comparar los dos modos de mostrar la solución que diseñamos para tu laberinto:

    Modo Animado / Dinámico:
        (Es lo que hace animate_solution()). El laberinto ya está en pantalla, y un punto
        se va moviendo, dibujando el camino en tiempo real. Hay movimiento, hay cambios a lo largo del tiempo.

    Modo Estático:
        (Es lo que introdujimos en print_maze_st()). La solución se dibuja al mismo tiempo que se van
        imprimiendo las paredes del laberinto. Cuando la función termina, te escupe un bloque entero de texto a la
        pantalla con el laberinto ya resuelto desde el primer milisegundo. No se mueve, no parpadea, no hay cursores
        saltando. Es un "bloque estático" de texto.
        Entonces, la flag is_static (que podríamos traducir al español como dibujar_como_bloque_estatico) le dice a
        print_maze_st: "Oye, necesito que al imprimir las celdas, incluyas también la solución dentro de la tinta de
        una sola pasada".

2. ¿Qué pasa si es False (y cuál es la consecuencia)?
    Ahí llegamos al núcleo de la línea de código que estabas revisando:


#   Si is_static es False, esto devuelve set() (un conjunto vacío)sol_set = set(solution_path) if solution_path and
#   is_static else set()

    Consecuencias en cadena si es False:

        Valor de la variable:
            sol_set se convierte en set(), es decir, un conjunto sin ningún elemento adentro.
        Evaluación de celdas:
            Más abajo, el código va recorriendo cada (x, y) del laberinto para decidir qué pintar
            adentro (un asterisco rojo, una pared, un espacio vacío...). 

    Cuando llega al bucle:  elif (x, y) in sol_set:
#   ¿Está la coordenada actual dentro del set de la solución?

    Como sol_set está vacío, esa pregunta siempre da "NO".

    Resultado visual: 
        Como siempre da "NO", nunca entra a pintar la línea content = sol + " • " + ec + r_style. Entra al
        else final y simplemente pinta un espacio vacío "   ".

    ¿Para qué queremos que pase esto?

        Para que print_maze_st haga su trabajo normal y te imprima un laberinto en blanco, limpio. Dejando así lista
        la pantalla (viewport) para que, milisegundos después, la otra función (animate_solution) tome el control del
        cursor y comience el show de dibujar la serpiente animada.

En resumen:

    is_static = True:
        Imprime las paredes Y los puntitos al mismo tiempo (salvataje para laberintos enormes).
        MATA la animación.

    is_static = False (estado por defecto): 
        Imprime SOLO las paredes. DEJA VIVO el mapa en blanco para que animate_solution haga su magia.


-----
22/04/26

Ha de tratarse la exception en open de:
IsADirectoryError: [Errno 21] Is a directory: 'config'
FileNotFoundError: Config file not found: config.txt

  File "/home/laviles/Python/a-maze-ing_lma/a-maze-ing/config/parser.py", line 55, in parse_config

CONFIG/PARSER.PY - Correcciones pendientes:

1.- if __name__ == "__main__": 
Es necesario para evitar la ejecucion de las lineas 133-134 -> openfile -> print_output.
O, quitar la impresion y llamarlo desde corresponda.

2.- Except (130-131) Excepcion sin medida. Solo printea, no re-raise.
    Solucion: except ConfigFileError as e: raise

3.- Bloque try enorme (60-131) 
    Solucion: Separar en funciones privadas (_read_file, _parse_lines, validate_keys, _parse_values(), etc)
             tratar excepciones por separado y elevar los raises correspondientes.
4.- MazeConfigError vacio - Necesita un mensaje contextual
    Excepciones jerarquicas que hereden de MazeConfigError especificas.

        Exceptions: ConfigFileError > ConfigFormatError > ConfigKeyError/ConfigValueError/ConfigBoundsError

Mantener API publica: 



-----
08/04/

Display 
Tengo q implementar la impresion de la respuesta del laberinto.
    El tema de que la generacionsea sleepeada, es viable? He de plantear que no puedo printear sobre otro
        fondo.
    He de designar el color final antes del coloreado de cada celda independiente. Seria, definir el
        camino de resolve como figura reservada, cual 42 block, y permitir el printeo personalizado de
        este en una version de display diferente.
    CONCLUSION: Hemos de generar perfiles de printeo de Dysplay function, segun el flag detectado por el
        user_input. Si el user inpt indica comando: Mostrar respuesta, ocultarla, generar un nuevo
        laberinto, cambiar de perfil de colores, etc.

MazeGen
    Se ha de limitar la impresion del 42 block si el height y weight no son suficientemente grandes
    Generacion del mensaje de error que debe printearse en caso de que el bloque 42 no se printee.
    Se ha de establecer los limites max & min en la generacion del Maze. En funcion de lo que la
        resolucion de la terminal soporta(o en la practica visual) y segun el minimo de casillas en el
        que se puedan unir entrada y salida sin generar ciclos. Hasta que cantidad de celdas se considera
        una grilla un laberinto? COnsultar definicion.

Validator
    Ha de encargarse de validar la ubicacion de la entrada y salida, dentro de los margenes del laberinto y fuera de las casillas reservadas ("bloque 42")


-----
2-04-26

Organización:

├── a-maze-ing
│   ├── README.md
│   ├── __init__.py
│   ├── a_maze_ing.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   └── validator.py
│   ├── config.txt
│   ├── maze.txt
│   ├── mazegen
│   │   ├── __init__.py
│   │   └── maze_generator.py
│   └── ui
│       ├── __init__.py
│       ├── display.py
│       └── header.txt
└── project-notes

5 directories, 13 files

Raiz contiene el main, archivo config.txt, se crea el archivo que contiene la representación en hexadecimal del laberinto y README.md

/config: contiene el script de parseo y el de validación
/mazegen: contiene el script que genera el laberinto. En ese archivo solo debería ir lo estrictamente para generar un laberinto con su solución.
/ui: contiene el script para visualizar el laberinto y el archivo que contiene el header en texto.

Está implementado el algoritmo Kruskal para crear el laberinto y el DFS (Depth-First Search) para encontrar la solución. El kruskal revisa parejas de celdas contiguas, las "añade" a un parent y quita las dos paredes que las unen (ex, si una está al lado de la otra, quita la pared derecha de una y la izquierda de la otra).
*Discplaimer: Esto se supone que crea un laberinto perfecto, pero tengo un vacio de entendimiento porque lo que determina si es perfecto es la celda de entrada y de salida.
El algoritmo DFS es para encontrar la salida: desde la celda entry_xy revisa todas las celdas a las que puede acceder, va guardando de que celda viene y que dirección tomó y guarda tambien las celdas exploradas. Cuando llega a exit_xy tiene guardado el camino que le llevó hasta allí.

Paso a paso rápido:

El programa se inicia ejecutando python3 a_maze_ing.py config.txt

- Se ejecuta el script de parseo que devuelve un diccionario
- Los valores de ese diccionario se usan para inicializar el objeto Maze
- Una vez creado, se ejecuta el método _generate_maze, que verifica qué celdas tendrán el patron 42, crea un grid de objetos "Cell" para las celdas, organiza las tuplas de paredes en una lista que luego "desordena" y aplica el algoritmo Kruskal para eliminar paredes aleatoriamente.
- luego, para mostrarlo usa la función display que recibe el laberinto y el patron 42 para poderlo imprimir. 
- finalmente crea el archivo que guarda la representación hexadecimal del laberinto.



==== Cosas que faltan: ====

- El laberinto debe tener la opción de ser perfecto. Ya se supone que lo es, asi que hay que ver como hacemos que sea imperfecto tambien.


- Falta el script validator, debería verificar que entry_xy y exit_exy esté dentro del rango de width y height y que no esté dentro del patron 42.
- Falta que, si el laberinto es muy pequeño para mostrar el patron 42, salga un mensaje, no tengo claro si tiene que mostrarse el laberinto o no.
** The program should be able to display a centered 42 pattern on the maze, if the maze dimensions allow it. If the maze dimensions do not allow the 42 pattern to be centered, the program should NOT display the pattern and continue execution without it. **


- Del parseo falta toda la parte de la interfaz de usuario. El laberinto debería mostrar un menú que permita: mostrar y ocultar la solución, cambiar el laberinto de color, generar un nuevo laberinto y salir.
- En el script de maze_generator.py está la función de crear el archivo maze.txt, no debería estar ahí.
- Todo lo que tenga que ver con la norma, flake8, docstrings, y probablemente hints también.

Y seguramente muchas cosas más, pero eso es lo principal por ahora.
