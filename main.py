from pila import Pila

import soko 
import gamelib

RUTA_NIVELES = 'niveles.txt'
RUTA_TECLAS = 'teclas.txt'

PARED = '#'
CAJA = '$'
JUGADOR = '@'
OBJETIVO = '.'
OBJETIVO_CAJA = '*'
OBJETIVO_JUGADOR = '+'
VACIO = ' '
DIM_CELDA = 64
DIRECCIONES = {'NORTE':(0,-1),'SUR':(0,1),'OESTE':(-1,0),'ESTE':(1,0)}

def archivo_niveles(archivo):
    '''
    Recibe como parametro como archivo.
    Devuelve un diccionario que tiene como clave un número (1 al 155) y como valor lista de cadenas,
    que representan los niveles del juego.
    '''
    niveles = {}
    clave = 0
    with open(archivo) as entrada:
        for lineas in entrada.readlines(): #se carga en memoria el archivo completo en una lista de cadenas['Linea 1/n','']
            linea = lineas.rstrip('\n')
            if linea != '' and linea[0] != "'":
                if linea[0] == 'L': #cuando es Level 1
                    clave += 1
                if linea[0] == ' ' or linea[0] == '#': #niveles
                    niveles[clave] = niveles.get(clave, []) + [linea]
    return niveles

def archivo_teclas(archivo):
    '''
    Recibe como parametro un archivo.
    Devuelve un diccionario que tiene como 
    clave la accion y como valor la tecla.
    '''
    teclas = {}
    with open(archivo) as entrada:
        for lineas in entrada.readlines(): #todas las lineas en una lista de strings
            if lineas == '\n':
                continue
            tecla,accion = lineas.rstrip('\n').split('=')
            tecla,accion = tecla.strip(),accion.strip()
            teclas[tecla]= teclas.get(tecla,'') + accion
    return teclas       

def emparejar(grilla_nivel): 
    '''
    Recibe una lista de cadenas.
    Si el largo de las cadenas no son iguales al maximo largo,
    se le agregan la cantidad de espacios de la diferencia.
    '''
    maximo = 0
    for fila in grilla_nivel: 
        if len(fila) > maximo:
            maximo = len(fila)
    for pos, fila in enumerate(grilla_nivel):
        if len(fila) == maximo:
            continue
        diferencia = maximo - len(fila)
        grilla_nivel[pos] += ' '*diferencia
    return grilla_nivel       

def juego_mostrar(grilla):                                                                 
    '''
    Recibe por parámetro una lista de listas y dibuja en pantalla.
    '''
    for f in range (len(grilla)):
        for c in range(len(grilla[0])):
            y = f * DIM_CELDA
            x = c * DIM_CELDA
            gamelib.draw_image('img/ground.gif',x,y) 
            if soko.hay_pared(grilla,c,f):
                gamelib.draw_image('img/wall.gif', x, y)
            if soko.hay_jugador(grilla,c,f):
                gamelib.draw_image('img/player.gif',x,y)
            if soko.hay_caja(grilla,c,f):
                gamelib.draw_image('img/box.gif',x,y)
            if soko.hay_objetivo(grilla,c,f):
                gamelib.draw_image('img/goal.gif', x, y)
        
def es_nivel(caracter,diccionario):
    '''
    Recibe un caracter y un diccionario, entra en el ciclo indefinido y 
    si el caracter ingresado po rel ususario es un numero y esta en el 
    diccionario lo retorna, de lo contrario vuelve a preguntar.
    '''
    while True:
        if caracter.isdigit() and int(caracter) in diccionario:
            return int(caracter)
        caracter = gamelib.input("Elegí otro nivel, por favor:")

def es_tecla(caracter,diccionario):
    '''
    Si el caracter esta en el diccionario lo retorna, sino devuelve None.
    '''
    if caracter in diccionario:
        return caracter

def backtraking(numero,juego):
    '''
    Recibe el estado del juego, busca las soluciones del juego y lo devuelve.
    '''
    visitados = set()
    dibujar_juego(numero,juego,3) #pensando
    verdadero, resultado = backtrack(juego,visitados)
    if not verdadero:
        dibujar_juego(numero,juego,4)
        gamelib.say("No hay Pistas Disponibles, reinicie o deshaga los movimientos")
    else:    
        dibujar_juego(numero,juego,2) #pista disponible
        return resultado

def backtrack(estado, visitados): # nivel juego, conjunto
    '''
    Función recursiva que recibe el estado del juego y un conjunto vacio, que tiene como caso base
    si el juego se gano de lo contrario entra en un ciclo definido que llama recursivamente hasta
    agotar todas las posibilidades.
    '''
    visitados.add(transformar_a_cadena(estado))                           
    if soko.juego_ganado(estado):
        # ¡encontramos la solución!
        return True, []

    for _,direccion in DIRECCIONES.items():
        nuevo_estado = soko.mover(estado, direccion) #a = (-1,0)
        if transformar_a_cadena(nuevo_estado) in visitados:            
            continue
        solución_encontrada, acciones = backtrack(nuevo_estado, visitados) #solucion encontrada es true o false
        if solución_encontrada:
            acciones.append(direccion)
            return True, acciones
    return False, None

def transformar_a_cadena(juego):
    '''
    Recibe el estado del juego y lo devuelve en una cadena.
    '''
    #[['#','#','#'],['1','@','#']]
    cadena = ''
    for fila in juego:
        cadena += ''.join(fila) +'\n'
    return cadena

def dibujar_juego(numero,juego,opcion):
    '''
    Recibe el nivel del juego, el estado del juego y un numero (1,2,3 o 4)
    y dibuja de acuerdo al número pasado por parámetro.
    '''
    opciones = {1:'',2:'Pista Disponible',3:'Pensando....',4:'Pista No Disponible'}
    gamelib.draw_begin()
    gamelib.title(f'SOKOBAN    Level : {numero}')
    juego_mostrar(juego) #muestra el juego en la ventana
    gamelib.draw_text(opciones[opcion], 10, 10, fill='yellow', anchor='nw')
    gamelib.draw_end()

def main():
    # Inicializar el estado del juego
    deshacer = Pila()
    pistas = []

    teclas = archivo_teclas(RUTA_TECLAS) 
    niveles = archivo_niveles(RUTA_NIVELES)
    
    contador = es_nivel(gamelib.input("Eliga un nivel:"),niveles)
    juego = emparejar(niveles[contador]) #lista de cadenas

    c, f = soko.dimensiones(juego)
    gamelib.resize(c*DIM_CELDA, f*DIM_CELDA)

    juego = soko.crear_grilla(juego) #lista de listas
    dibujar_juego(contador,juego,1)

    while gamelib.is_alive():
        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break
        # Actualizar el estado del juego, según la `tecla` presionada
        tecla = ev.key

        if es_tecla(tecla,teclas) == None:
            continue

        if tecla == 'Escape':
            gamelib.say("Gracias por jugar Sokoban :)")
            break

        if tecla == 'h':
            if len(pistas) == 0:
                pistas = backtraking(contador,juego) 
                if pistas == None:
                    pistas = []
            else:
                pista = pistas.pop()
                juego = soko.mover(juego,pista)
                deshacer.apilar(juego)
                dibujar_juego(contador,juego,2) #pista disponible

        if soko.juego_ganado(juego):
            contador +=1
            while not deshacer.esta_vacia():
                deshacer.desapilar()
            gamelib.say("Pasaste al siguiente nivel :)")

            juego = emparejar(niveles[contador])
            c, f = soko.dimensiones(juego)
            gamelib.resize(c*DIM_CELDA, f*DIM_CELDA)
            juego = soko.crear_grilla(juego)
            dibujar_juego(contador,juego,1)

        if tecla == 'r': 
            if len(pistas) != 0:
                pistas = []
            juego = emparejar(niveles[contador])
            c, f = soko.dimensiones(juego)
            gamelib.resize(c*DIM_CELDA, f*DIM_CELDA)
            juego = soko.crear_grilla(juego) 
            dibujar_juego(contador,juego,1)

        if tecla == 'Control_L':
            if not deshacer.esta_vacia():
                juego = deshacer.desapilar()
            dibujar_juego(contador,juego,1)

        if teclas[tecla] in DIRECCIONES:
            deshacer.apilar(juego)
            juego = soko.mover(juego,DIRECCIONES[teclas[tecla]]) 
            dibujar_juego(contador,juego,1)

        if tecla != 'h': #vaciar la lista
            if len(pistas) != 0:
                pistas = []
        
gamelib.init(main)