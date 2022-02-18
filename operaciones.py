import matplotlib.pyplot as plt
import pandas as pd

data=pd.read_csv("integración.csv")

def datos_esc():
    datos_esc= data.pivot_table(index = ['Escuela'], aggfunc ='size')
    escuelas_unicas=[]

    for i in range(0,len(datos_esc)):
        escuelas_unicas.append(datos_esc.index.values[i])
    
    return escuelas_unicas