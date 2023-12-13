import pytest
from fuente.fuente import (Persona, Color, Paciente, sort_prior_tiempo, generador_pac, sort_prior_llegados, num_llegados, red_tiempo, sistema_salas, sist_salas_libres, min_a_hora, medicos)

def test_sort_prior_tiempo():
    pac1 = Paciente("Primero", 10, 1, Color, 0)
    pac2 = Paciente("Segundo", 10, 2, Color.blue, 15)
    pac3 = Paciente("Tercero", 10, 3, Color.orange, 0)
    pac4 = Paciente("Cuarto", 10, 4, Color.yellow, 50)
    lista_pac = [pac1, pac2, pac3, pac4]
    lista_pac = sort_prior_tiempo(lista_pac)
    assert lista_pac == [pac1, pac3, pac2, pac4]
def test_sort_prior_tiempo_2():
    pac1 = Paciente("Primero", 10, 1, Color.red, 10)
    pac2 = Paciente("Segundo", 10, 2, Color.blue, 0)
    pac3 = Paciente("Tercero", 10, 3, Color.orange, 50)
    pac4 = Paciente("Cuarto", 10, 4, Color.yellow, 0)
    lista_pac = [pac1, pac2, pac3, pac4]
    lista_pac = sort_prior_tiempo(lista_pac)
    assert lista_pac == [pac2, pac4, pac1, pac3]

def test_generador_pac_fallo():
    lista_pac = generador_pac("a")
    assert lista_pac == []
def test_generador_pac_fallo_2():
    lista_pac = generador_pac(-1)
    assert lista_pac == []

def test_sort_prior_llegados():
    pac1 = Paciente("Primero", 10, 1, Color.red, 0)
    pac2 = Paciente("Segundo", 10, 2, Color.orange, 5)
    pac3 = Paciente("Tercero", 10, 3, Color.orange, 12)
    pac4 = Paciente("Cuarto", 10, 4, Color.yellow, 25)
    pac5 = Paciente("Quinto", 10, 5, Color.blue, 12)
    pac6 = Paciente("Sexto", 10, 6, Color.green, 25)
    lista_pac = [pac1, pac2, pac3, pac4]
    pool = [pac5, pac6]
    lista_pac = sort_prior_llegados(lista_pac, pool)
    assert lista_pac == [pac1, pac2, pac3, pac4, pac6, pac5]
def test_sort_prior_llegados_2():
    pac1 = Paciente("Primero", 10, 1, Color.red, 0)
    pac2 = Paciente("Segundo", 10, 2, Color.orange, 5)
    pac3 = Paciente("Tercero", 10, 3, Color.orange, 12)
    pac4 = Paciente("Cuarto", 10, 4, Color.yellow, 25)
    pac5 = Paciente("Quinto", 10, 5, Color.red, 12)
    pac6 = Paciente("Sexto", 10, 6, Color.red, 25)
    lista_pac = [pac1, pac2, pac3, pac4]
    pool = [pac5, pac6]
    lista_pac = sort_prior_llegados(lista_pac, pool)
    assert lista_pac == [pac1, pac5, pac6, pac2, pac3, pac4]