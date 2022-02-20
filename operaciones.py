import matplotlib.pyplot as plt
import pandas as pd

data=pd.read_csv("integración.csv")
data.drop("#",axis=1,inplace=True)

def datos_esc():
    datos_esc= data.pivot_table(index = ['Escuela'], aggfunc ='size')
    escuelas_unicas=[]

    for i in range(0,len(datos_esc)):
        escuelas_unicas.append(datos_esc.index.values[i])
    
    return escuelas_unicas

def graficame(escuela):
    img_por_masa=["static/img/graf_masa.png"]
    selector=data[(data.Escuela==escuela)]
    por_masa=pd.crosstab(selector["indice de Masa Corporal"],selector["SEXO"])
    graf_masa=por_masa.plot(kind="bar",figsize=(6,4),title="Índice de masa corporal por sexo")
    fig = graf_masa.get_figure()
    fig.savefig(img_por_masa[0])
    
    return img_por_masa