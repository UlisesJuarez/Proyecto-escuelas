import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("integración.csv")
data.drop("#", axis=1, inplace=True)
colores = ["#ADD5FA", "#60D394", "#5086C1"]
imagenes_graficas = []


def datos_esc():
    datos_esc = data.pivot_table(index=['Escuela'], aggfunc='size')
    escuelas_unicas = []

    for i in range(0, len(datos_esc)):
        escuelas_unicas.append(datos_esc.index.values[i])

    return escuelas_unicas


def graficame(escuela):
    img1=por_masa(escuela)
    img2=por_talla(escuela)
    if img1 not in imagenes_graficas:
        imagenes_graficas.append(img1)
    if img2 not in imagenes_graficas:
        imagenes_graficas.append(img2)

    return imagenes_graficas

def por_masa(escuela):
    ruta="static/img/graf_masa.png"
    selector = data[(data.Escuela == escuela)]

    # Para la grafica indice de masa corporal por sexo
    por_masa = pd.crosstab(
        selector["indice de Masa Corporal"], selector["SEXO"])
    fig = por_masa.plot(kind="bar",figsize=(6,4),title="Índice de masa corporal por sexo",cmap="winter").get_figure()
    fig.autofmt_xdate(rotation=0)
    fig.savefig(ruta)

    return ruta

def por_talla(escuela):
    ruta="static/img/graf_talla.png"
    selector = data[(data.Escuela == escuela)]
    # Para la grafica talla para la edad
    por_talla = selector.groupby("Talla para la edad").count()
    x = por_talla["Edad en anos"].values
    y= por_talla["Edad en anos"].keys().values
    #desfase = (0.1, 0.1, 0.1)
    plt.figure(figsize=(6,5))
    plt.title("Talla para la edad",fontdict={'family': 'serif',
                    'color': 'royalblue'})
    plt.pie(x, labels=y, autopct="%0.1f%%", colors=colores)
    plt.axis("equal")
    plt.savefig(ruta)

    return ruta
