import matplotlib.pyplot as plt
import pandas as pd

data=pd.read_csv("integración.csv")

def datos_esc():
    datos_esc= data.pivot_table(index = ['Escuela'], aggfunc ='size')
    escuelas_unicas=[]

    for i in range(0,len(datos_esc)):
        escuelas_unicas.append(datos_esc.index.values[i])
    
    return escuelas_unicas

def graficame(escuela):
    selector=data[(data.Escuela==escuela)]
    """
    Aquí pones el codigo para hacer las graficas, haz la pruebas en el archivo jupyter y solo copia y pega
    el codigo aquí, exportas la ruta estatica de las imagenes las metes en un arreglo, las envias aqui con 
    el return, las envias en la template con el nombre que aparece en el index 'img_gra' y agregas la ruta
    estatica al src y listo solo le das estilo
    """

    print(selector)