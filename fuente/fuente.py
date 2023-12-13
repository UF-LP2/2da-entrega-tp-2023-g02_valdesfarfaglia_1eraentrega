from enum import Enum
import time
import random
import random_name_generator as rng
import sys

from PyQt6.QtCore import QThread, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, \
    QListWidgetItem, QListWidget
from PyQt6 import QtCore


global lastid
lastid = 0


#---------pedir tiempo----------------
class AlmacenarNumero(QMainWindow,QObject):
    closed = pyqtSignal()
    numero_guardado = pyqtSignal(int)
    def __init__(self):
        super().__init__()

        self.closed = None
        self.setWindowTitle("Almacenar Número")
        self.setGeometry(100, 100, 400, 100)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.input_numero = QLineEdit(self)
        self.layout.addWidget(self.input_numero)

        self.boton_guardar = QPushButton("Guardar Número", self)
        self.boton_guardar.clicked.connect(self.guardar_numero)
        self.layout.addWidget(self.boton_guardar)

        self.numero = 0  # Variable para almacenar el número

    def guardar_numero(self):
        try:
            numero = int(self.input_numero.text())
            self.numero = numero
            self.input_numero.clear()  # Limpiar el campo de entrada
            print(f"Número guardado: {numero}")
            self.numero_guardado.emit(numero)  # Emitir la señal 'numero_guardado'
            self.close()
            return numero
        except ValueError:
            print("¡Ingresa un número válido!")
    def cerrar_y_abrir_ventana2(self):
        self.closed.emit()  # Emitir la señal 'closed' al cerrar la ventana


#-------------------actualizar lista-------------------------------

class ActualizarLista(QMainWindow):
    def __init__(self, lista_pacientes, lista_llegados, salas_libres,hora):
        super().__init__()

        self.setWindowTitle("Simulación de Triage Hospitalario")
        self.setGeometry(100, 100, 800, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.lista_pacientes_widget = QListWidget()
        self.lista_llegados_widget = QListWidget()
        self.salas_libres_label = QLabel()
        self.hora_label=QLabel()

        self.layout.addWidget(QLabel("Lista de Pacientes:"))
        self.layout.addWidget(self.lista_pacientes_widget)
        self.layout.addWidget(QLabel("Lista de Pacientes Llegados:"))
        self.layout.addWidget(self.lista_llegados_widget)
       # self.layout.addWidget(QLabel("Salas Libres:"))
        self.layout.addWidget(self.salas_libres_label)
        self.layout.addWidget(self.hora_label)

        self.lista_pacientes = lista_pacientes
        self.lista_llegados = lista_llegados
        self.salas_libres = salas_libres
        self.hora= hora


                           #   alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)


        self.update_lists()

    def update_lists(self):
        self.lista_pacientes_widget.clear()
        self.lista_llegados_widget.clear()
        for paciente in self.lista_pacientes:
            self.lista_pacientes_widget.addItem(QListWidgetItem(f"Nombre: {paciente.nombre}, Edad: {paciente.edad}, Color: {paciente.color}, Tiempo: {paciente.tiempo}"))
        for paciente in self.lista_llegados:
            self.lista_llegados_widget.addItem(QListWidgetItem(f"Nombre: {paciente.nombre}, Edad: {paciente.edad}, Color: {paciente.color}, Tiempo: {paciente.tiempo}"))
        self.salas_libres_label.setText(f"Salas Libres: {self.salas_libres}")
        self.hora_label.setText(f"Hora: {self.hora}")

def fusionar(izquierda, derecha):
    resultado = []
    i = 0
    j = 0

    # Agregar pacientes con tiempo de vida 0 al principio
    while i < len(izquierda) and izquierda[i].tiempo == 0:
        resultado.append(izquierda[i])
        i += 1

    # Combinar pacientes
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i].tiempo <= derecha[j].tiempo:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    # Agregar pacientes restantes
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

    return resultado

#def mostrar_lista(lista):
 #   app = QApplication(sys.argv)
  #  ventana = ActualizarLista(lista)
   # ventana.show()
    #sys.exit(app.exec())





#region enum
class Color(Enum):
    red = 1
    orange = 2
    yellow = 3
    green = 4
    blue = 5
    white = 6   # el color white se hizo para salvar cualquier error en asignacion de gravedad,
                # iria automaticamente al final de la lista con un tiempo virtualmente inagotable
#endredgion enum


#region clases
class Persona:
    def __init__(self, nombre, edad, id):
        self.nombre = nombre
        self.edad = edad
        self.id = id

class Paciente(Persona):
    def __init__(self, nombre, edad, id, color, tiempo):
        Persona.__init__(self, nombre, edad, id)
        self.color = color
        self.tiempo = tiempo
    def to_string(self):
        return str(f"Nombre: {self.nombre}, Edad: {self.edad}, Color: {self.color}, Edad: {self.tiempo}, ID: {self.id}")

#endregion clases

#region funciones

def num_llegados():
    ran_cant = random.randint(0, 100) # probabilidad ajustable respecto a num llegados
    if ran_cant < 56:
        cant1 = 0
        return cant1
    elif 55 < ran_cant < 80:
        cant1 = 1
        return cant1
    elif 79 < ran_cant < 101:
        cant1 = 2
        return cant1

def generador_pac(num_pac): # crea la cantidad de pacientes indicadas segun funcion num_llegados()
    list_pac = []

    num_aux = num_pac
    if str(num_aux).isdigit() and num_pac > -1:

        for i in range(0, num_pac):
            global lastid
            col = Color.white
            edad = random.randrange(3, 80)
            id = lastid+1
            lastid = lastid + 1
            sex = random.randint(0, 1)
            if sex == 0:
                nombre = rng.generate(descent=rng.Descent.ENGLISH, sex=rng.Sex.MALE, limit=1)
            elif sex == 1:
                nombre = rng.generate(descent=rng.Descent.ENGLISH, sex=rng.Sex.FEMALE, limit=1)
            vivo = 0
            pac = Paciente(nombre, edad, id, col, 100000)
            list_pac.append(pac)
        return list_pac
    else:

        return list_pac
def sistema_salas(pool, salas_libres):
    pool_proc = []
    for i in range(0, salas_libres):
        if len(pool)!=0:
            pac = pool.pop(0) # se hace pop de cada paciente del pool de llegados a las salas, segun disponibilidad
            ran = random.randrange(0, 100) # probabilidad ajustable por color
            if ran < 6:
                pac.color = Color.red
                pac.tiempo = 0
            elif 5 < ran < 15:
                pac.color = Color.orange
                pac.tiempo = 10
            elif 14 < ran < 30:
                pac.color = Color.yellow
                pac.tiempo = 60
            elif 29 < ran < 60:
                pac.color = Color.green
                pac.tiempo = 120
            elif 59 < ran < 101:
                pac.color = Color.blue
                pac.tiempo = 240
            pool_proc.append(pac) # se lo agrega al pool de devolucion
        else:
            break
    return pool_proc

def sist_salas_libres(hora): #asignacion de salas por horario
    if 22 < hora < 24:
        return 1
    elif -1 < hora < 7:
        return 1
    elif 5 < hora < 11:
        return 2
    elif 9 < hora < 17:
        return 5
    elif 15 < hora < 23:
        return 3


def sort_prior_llegados(lista_pac, pool):
    for i in range(0, len(pool)): # hago pop de cada uno de los que me llega para trabajar de forma individual
        pac_actual = pool.pop(0)
        if len(lista_pac)==0: # el primero que me llega lo agrego a la pos 0
            lista_pac.append(pac_actual)
        elif pac_actual.tiempo == 0: #si tiene tiempo 0 (es rojo) lo agrego al final de los que tienen tiempo 0
            for j in range(0, len(lista_pac)):
                if pac_actual.tiempo != lista_pac[j].tiempo: #busco el primero con tiempo != 0 y lo inserto en esa pos
                    lista_pac.insert(j, pac_actual)
                    break
                elif j == len(lista_pac) - 1: # si llega al final sin encontrar != 0 lo agrego en la ultima pos
                    lista_pac.append(pac_actual)
                    break
        elif pac_actual.tiempo != 0: #repito procedimiento pero a partir del color
            for k in range(0, len(lista_pac)):
                if pac_actual.color.value < lista_pac[k].color.value:
                    lista_pac.insert(k, pac_actual)
                    break
                elif k == len(lista_pac) - 1:
                    lista_pac.append(pac_actual)
                    break
    return lista_pac

def sort_prior_tiempo(lista_pac):
    if len(lista_pac) <= 1:
        return lista_pac  # Caso base
    # Dividir  lista
    mitad = len(lista_pac) // 2
    izquierda = lista_pac[:mitad]
    derecha = lista_pac[mitad:]

    # llamadas recursivas a ordenar_pacientes en las dos mitades
    izquierda_ordenada = sort_prior_tiempo(izquierda)
    derecha_ordenada = sort_prior_tiempo(derecha)

    # combinar mitades ordenadas
    pacientes_ordenados = fusionar(izquierda_ordenada, derecha_ordenada)

    return pacientes_ordenados

def red_tiempo(lista_pac): #se produce cada vuelta y resta 1 al contador hasta que sea 0
    for i in range(0, len(lista_pac)):
        if lista_pac[i].tiempo != 0:
            lista_pac[i].tiempo = lista_pac[i].tiempo - 1

def min_a_hora(hora, min):
    if min == 0:
        hora = 0
        min = 0
    elif min % 60 == 0:
        hora = hora + 1
    if hora == 24:
        hora = 0


    return hora

def medicos(lista_pac):
    ran_cant = random.randint(0, 100)
    cant = 0 # por si falla la asignacion lo dejo en 0 predeterminado
    if ran_cant < 56:
        cant = 0
    elif 55 < ran_cant < 76:
        cant = 2
    elif 77 < ran_cant < 101:
        cant = 1
    lista_pac_nueva = lista_pac[cant:]
    return lista_pac_nueva

def emergencias_llegados(lista_llegados): # existe la probabilidad de que uno de los llegados tenga una emergencia urgente y se lo lleve al principio de la fila
    for i in range(0, len(lista_llegados)):
        ran_prob = random.randrange(0, 1000)
        if ran_prob < 50 and lista_llegados[i].color != Color.white:
            pac = lista_llegados.pop(i)  # se lo extrae de su posicion con pop
            lista_llegados.insert(0, pac)  # se lo mueve automaticamente a la primera posicion para ser ingresado en la primera ventana disponible

def emergencia_lobby(lista_pac):
    for i in range(0, len(lista_pac)):
        ran_prob = random.randrange(0, 1000)
        if ran_prob < 25 and lista_pac[i].color != Color.white: #el paciente sufrio una emergencia repentina y se lo ha movido al principio de la prioridad, es mejorable.
            lista_pac[i].tiempo = 0
            lista_pac[i].color = Color.red
        if 49 < ran_prob < 60 and lista_pac[i].tiempo == 0 and lista_pac[i].color != Color.white: # si el paciente ya era critico y sufre una emergencia, fallece.
            lista_pac[i].remove()                           # la probabilidad es realmente baja, 1% * prob(rojo) tiende a 0




def simulacion():

    app = QApplication(sys.argv)
    ventana1 = AlmacenarNumero()
    ventana1.show()
    global lastid
    aux_num = None  # Variable para almacenar el número
    def iniciar_simulacion(numero):
        nonlocal aux_num  # Acceder a la variable 'aux_num' externa
        aux_num = numero
    # Conecta la señal 'numero_guardado' al inicio de la simulación
    ventana1.numero_guardado.connect(iniciar_simulacion)
    app.exec()  # Ejecuta la aplicación para interactuar con la interfaz gráfica

    lista_llegados = []
    lista_pac=[]



    hora = 0
    min=int
    for min in range(0, int(aux_num) * 60):
        hora = min_a_hora(hora, min) # transforma los minutos que no poseen limite, a horas de 0 a 24
        salas_libres = sist_salas_libres(hora) # en funcion del horario ajusta el numero de salas-enfermeros/as
        pool_proc = []
        print("Minuto: ", str(min))
        time.sleep(1)  # pausa ajustable a gusto
        cant = num_llegados()  # defino numero de llegados, funcion ajustable a gusto
        prepool = generador_pac(cant)  # se cargan del generador a un prepool
        for i in range(0, cant):  # con un for para que no se metan listas como elementos individuales
            if len(prepool) != 0:
                lista_llegados.append(prepool.pop(0))  # llegan a la puerta del hospital y se agregan al final
        pool = []  # aca se meten los recien llegados de a uno
        if min % 3 == 0: # hago que las salas tarden 3 minutos por cada paciente, a fines de la simulacion cualquier acercamiento es igual de inorganico.
            for i in range(0, salas_libres):  # mete al pool n elementos segun haya n salas libres
                if len(lista_llegados) != 0:
                    pool.append(lista_llegados.pop(0))
            if len(pool) != 0:
                pool_proc = sistema_salas(pool, salas_libres)  # entran en cant = x segun el horario, tambien dura 3 tiempos
        lista_pac = sort_prior_llegados(lista_pac, pool_proc)   # se ordena por color los que llegan
        ventana2 = ActualizarLista(lista_pac, lista_llegados, salas_libres,hora)
        ventana2.show()

        app.exec()

       # ventana2 = ActualizarLista(lista_pac)
        #ventana2.show()
                                                                # y despues los criticos al principio, se les resta 1 tiempo
        lista_pac = medicos(lista_pac)  # rebano n posiciones iniciales, simulando que el medico los llamó a ser atendidos.
        red_tiempo(lista_pac) # reduzco tiempo y simulo detalles extra
        lista_pac = sort_prior_tiempo(lista_pac) #ordeno por tiempo, si tiene tiempo 0 va al final de la sublista de tiempos 0

    '''if len(lista_pac) != 0:
        for i in range(len(lista_pac)):
            print("ID: ", lista_pac[i].id)
            print("Nombre: ", lista_pac[i].nombre)
            print("Edad: ", lista_pac[i].edad)
            print("Color: ", lista_pac[i].color)
            print("Tiempo restante: ", lista_pac[i].tiempo)
            print("\n")
    print("La simulacion ha finalizado")'''

    #sys.exit(app.exec())

#enregion funciones
