PARED = '#'
CAJA = '$'
JUGADOR = '@'
OBJETIVO = '.'
OBJETIVO_CAJA = '*'
OBJETIVO_JUGADOR = '+'
VACIO = ' '

def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Ejemplo:
    
    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    '''
    return [[desc[f][c] for c in range(len(desc[0]))] for f in range(len(desc))]        
     
def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    return len(grilla[0]),len(grilla)
        

def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    return grilla[f][c] == PARED

def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    return grilla[f][c] == OBJETIVO or grilla[f][c]== OBJETIVO_JUGADOR or grilla[f][c]== OBJETIVO_CAJA

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    return grilla[f][c] == CAJA or grilla[f][c] == OBJETIVO_CAJA
        
def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    return grilla[f][c] == JUGADOR or grilla[f][c] == OBJETIVO_JUGADOR

def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    caracteres = ''
    for f in range(len(grilla)):
        for c in range(len(grilla[f])):
            caracteres += grilla[f][c]
    return OBJETIVO not in caracteres and OBJETIVO_JUGADOR not in caracteres
    
def mover(grilla, direccion): #lista de cadenas o lista de listas
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''
    x,y= direccion
    grilla_nueva,j1,j2 = crear_grilla_nueva(grilla)
    sig_j1,sig_j2 = j1+y,j2+x
    sig_jugador = grilla_nueva[sig_j1][sig_j2] 
    
    if es_mov_valido(grilla_nueva,sig_jugador,sig_j1+y,sig_j2+x):
        cambiar_celda(grilla_nueva,j1,j2,OBJETIVO_JUGADOR,OBJETIVO_JUGADOR,OBJETIVO,JUGADOR,JUGADOR,VACIO)
        cambiar_celda(grilla_nueva,sig_j1,sig_j2,VACIO,CAJA,JUGADOR,OBJETIVO,OBJETIVO_CAJA,OBJETIVO_JUGADOR)
        if sig_jugador == CAJA or sig_jugador == OBJETIVO_CAJA:
            cambiar_celda(grilla_nueva,sig_j1+y,sig_j2+x,VACIO,VACIO,CAJA,OBJETIVO,OBJETIVO,OBJETIVO_CAJA)
        return grilla_nueva
    return grilla


def cambiar_celda(grilla,x,y,condicion1,condicion2,cambio1,condicion3,condicion4,cambio2):
    '''Recibe por parámetro una lista de listas, dos números y 6 caracteres, si cumple la condiciones
    devuelve la lista de lista cambiada en la ubicación de esos dos números con los cambios respectivos.'''
    if grilla[x][y] == condicion1 or grilla[x][y] == condicion2:
        grilla[x][y] = cambio1
    if grilla[x][y] == condicion3 or grilla[x][y] == condicion4:
        grilla[x][y] = cambio2
    return grilla

def es_mov_valido(grilla,caracter,x,y):
    '''
    Función que recibe lista de listas, un caracter y dos numeros, y devuelve True si se cumplen las condiciones.
    '''
    if caracter != PARED:
        celdas = caracter,grilla[x][y]
        cajas = CAJA,CAJA
        caja_pared = CAJA,PARED
        caja_objetivo = OBJETIVO_CAJA,PARED
        caja_objetivo2 = OBJETIVO_CAJA,OBJETIVO_CAJA
        objetivo_caja = OBJETIVO_CAJA,CAJA
        caja_objetivo_caja = CAJA,OBJETIVO_CAJA
        return celdas != cajas and celdas != caja_pared and celdas != caja_objetivo and celdas != caja_objetivo2 and celdas != objetivo_caja and celdas != caja_objetivo_caja
       
def crear_grilla_nueva(grilla): 
    '''Función que crea una lista de listas nueva, a partir de la grilla que entra por parámetro,
    y devuelve la grilla nueva y dos números, que es la posición del jugador.'''
    grilla_nueva = []
    for f in range(len(grilla)):
        fila = []
        for c in range(len(grilla[f])):
            if grilla[f][c] == JUGADOR or grilla[f][c] == OBJETIVO_JUGADOR:
                j1,j2 = f,c
            fila.append(grilla[f][c])
        grilla_nueva.append(fila)
    return grilla_nueva,j1,j2