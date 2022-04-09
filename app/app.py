############################################################################
#                >IMPORTS
import math
import numpy as np
import pandas as pd

from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

from flask import Flask, redirect, render_template, request,send_file, url_for
import pdfkit


app = Flask(__name__)


df = pd.read_csv('./data/escuelas_data.csv')


# datos anteriores y actuales
data = pd.read_csv("escuelas_data.csv")
data2 = pd.read_csv("escuelas_data2.csv")
permiso=False

############################################################################
#                       > CONSTANT VALUES
palette = ['#4D77FF',"#488FB1", '#39AEA9', '#557B83', '#05595B',"#062C30","#488FB1"]

chart_font = 'Helvetica'
chart_title_font_size = '16pt'
chart_title_alignment = 'center'
axis_label_size = '14pt'
axis_ticks_size = '12pt'
default_padding = 30
chart_inner_left_padding = 0.015
chart_font_style_title = 'bold italic'

##############################################################
# Formato del informe

encabezado = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reporte</title>
  <link rel='stylesheet' type='text/css' href='../static/css/report.css'/>
</head>
<body>
    

'''

pie = '''
</body>
</html>
'''
################################################################
# Funciones para el reporte
def print_data(df, filename='', title=''):
    contenido = ''
    if title != '':
        contenido += '<h2> %s </h2>\n' % title
    contenido += df.to_html(classes='wide', escape=False)

    with open(filename, 'w') as f:
        f.write(encabezado + contenido + pie)

############################################################################
#                       > HELPER FUNCTIONS


def palette_generator(length, palette):
    int_div = length // len(palette)
    remainder = length % len(palette)
    return (palette * int_div) + palette[:remainder]


def plot_styler(p):
    p.title.text_font_size = chart_title_font_size
    p.title.text_font = chart_font
    p.title.align = chart_title_alignment
    p.title.text_font_style = chart_font_style_title
    p.y_range.start = 0
    p.x_range.range_padding = chart_inner_left_padding
    p.xaxis.axis_label_text_font = chart_font
    p.xaxis.major_label_text_font = chart_font
    p.xaxis.axis_label_standoff = default_padding
    p.xaxis.axis_label_text_font_size = axis_label_size
    p.xaxis.major_label_text_font_size = axis_ticks_size
    p.yaxis.axis_label_text_font = chart_font
    p.yaxis.major_label_text_font = chart_font
    p.yaxis.axis_label_text_font_size = axis_label_size
    p.yaxis.major_label_text_font_size = axis_ticks_size
    p.yaxis.axis_label_standoff = default_padding
    p.toolbar.logo = None
    p.toolbar_location = None


def redraw(p_class):
    talla_chart = talla_bar_chart(df, p_class)
    long_pierna_chart = long_pierna_bar_chart(df, p_class)
    masa_corporal_chart = masa_corporal_bar_chart(df, p_class)
    variedad_sae_chart = variedad_sae_bar_chart(df, p_class)
    cambra_chart = cambra_bar_chart(df, p_class)
    higiene_chart = higiene_bar_chart(df, p_class)
    cariogenico_chart = cariogenico_bar_chart(df, p_class)
    ecotecnias_chart = ecotecnias_bar_chart(df, p_class)

    return (
        talla_chart,
        long_pierna_chart,
        masa_corporal_chart,
        variedad_sae_chart,
        cambra_chart,
        higiene_chart,
        cariogenico_chart,
        ecotecnias_chart
    )


##########################################################################################
#                          > MAIN ROUTE



@app.route('/', methods=['GET', 'POST'])
def chart():
    selected_class = request.form.get('dropdown-select')

    if selected_class == 0 or selected_class == None:
        talla_chart, long_pierna_chart, masa_corporal_chart, variedad_sae_chart, cambra_chart, higiene_chart, cariogenico_chart, ecotecnias_chart = redraw(
            0)
    else:
        talla_chart, long_pierna_chart, masa_corporal_chart, variedad_sae_chart, cambra_chart, higiene_chart, cariogenico_chart, ecotecnias_chart = redraw(
            selected_class)

    script_talla_chart, div_talla_chart = components(talla_chart)
    script_long_pierna_chart, div_long_pierna_chart = components(
        long_pierna_chart)
    script_masa_corporal_chart, div_masa_corporal_chart = components(
        masa_corporal_chart)
    script_variedad_sae_chart, div_variedad_sae_chart = components(
        variedad_sae_chart)
    script_cambra_chart, div_cambra_chart = components(cambra_chart)
    script_higiene_chart, div_higiene_chart = components(higiene_chart)
    script_cariogenico_chart, div_cariogenico_chart = components(
        cariogenico_chart)
    script_ecotecnias_chart, div_ecotecnias_chart = components(
        ecotecnias_chart)

    return render_template(
        'index.html',
        div_talla_chart=div_talla_chart,
        script_talla_chart=script_talla_chart,
        div_long_pierna_chart=div_long_pierna_chart,
        script_long_pierna_chart=script_long_pierna_chart,
        div_masa_corporal_chart=div_masa_corporal_chart,
        script_masa_corporal_chart=script_masa_corporal_chart,
        div_variedad_sae_chart=div_variedad_sae_chart,
        script_variedad_sae_chart=script_variedad_sae_chart,
        div_cambra_chart=div_cambra_chart,
        script_cambra_chart=script_cambra_chart,
        div_higiene_chart=div_higiene_chart,
        script_higiene_chart=script_higiene_chart,
        div_cariogenico_chart=div_cariogenico_chart,
        script_cariogenico_chart=script_cariogenico_chart,
        div_ecotecnias_chart=div_ecotecnias_chart,
        script_ecotecnias_chart=script_ecotecnias_chart,
        selected_class=selected_class
    )
############################################################################
#                           > CHART GENERATION


def talla_bar_chart(dataset, pass_class, cpalette=palette):
    talla_data = dataset[dataset['escuela'] == int(pass_class)]
    talla_posibilidades = list(talla_data['talla_edad'].value_counts().index)
    talla_valores = list(talla_data['talla_edad'].value_counts().values)
    int_posibilidades = np.arange(len(talla_posibilidades))
    source = ColumnDataSource(data={
        'posibilidades': talla_posibilidades,
        'talla_int': int_posibilidades,
        'valores': talla_valores
    })

    hover_tool = HoverTool(
        tooltips=[('Talla', '@posibilidades'), ('Numero', '@valores')]
    )
    chart_labels = {}
    for val1, val2 in zip(source.data['talla_int'], source.data['posibilidades']):
        chart_labels.update({int(val1): str(val2)})

    p = figure(tools=[hover_tool], plot_height=400, title='Talla para la edad')
    p.vbar(x='talla_int', top='valores', source=source, width=0.9,
        fill_color=factor_cmap('posibilidades', palette=palette_generator(len(source.data['posibilidades']), cpalette), factors=source.data['posibilidades']))

    plot_styler(p)
    p.xaxis.ticker = source.data['talla_int']
    p.xaxis.major_label_overrides = chart_labels
    p.xaxis.major_label_orientation = math.pi / 4
    p.sizing_mode = 'scale_width'

    return p


def long_pierna_bar_chart(dataset, pass_class, cpalette=palette[1:4]):
    long_pierna_data = dataset[dataset['escuela'] == int(pass_class)]
    long_pierna_posibilidades = list(
        long_pierna_data['long_pierna'].value_counts().index)
    long_pierna_valores = list(
        long_pierna_data['long_pierna'].value_counts().values)
    int_posibilidades = np.arange(len(long_pierna_posibilidades))
    source = ColumnDataSource(data={
        'posibilidades': long_pierna_posibilidades,
        'long_pierna_int': int_posibilidades,
        'valores': long_pierna_valores
    })
    hover_tool = HoverTool(
        tooltips=[('Longitud', '@posibilidades'), ('Numero', '@valores')]
    )
    chart_labels = {}
    for val1, val2 in zip(source.data['long_pierna_int'], source.data['posibilidades']):
        chart_labels.update({int(val1): str(val2)})

    p = figure(tools=[hover_tool], plot_height=400, title='Longitud pierna')
    p.vbar(x='long_pierna_int', top='valores', source=source, width=0.9,
        fill_color=factor_cmap('posibilidades', palette=palette_generator(len(source.data['posibilidades']), cpalette), factors=source.data['posibilidades']))

    plot_styler(p)
    p.xaxis.ticker = source.data['long_pierna_int']
    p.xaxis.major_label_overrides = chart_labels
    p.xaxis.major_label_orientation = math.pi / 4
    p.sizing_mode = 'scale_width'

    return p


def masa_corporal_bar_chart(dataset, pass_class, cpalette=palette[1:4]):
    masa_corporal_data = dataset[dataset['escuela'] == int(pass_class)]
    masa_corporal_posibilidades = list(
        masa_corporal_data['masa_corporal'].value_counts().index)
    masa_corporal_valores = list(
        masa_corporal_data['masa_corporal'].value_counts().values)
    int_posibilidades = np.arange(len(masa_corporal_posibilidades))
    source = ColumnDataSource(data={
        'posibilidades': masa_corporal_posibilidades,
        'masa_corporal_int': int_posibilidades,
        'valores': masa_corporal_valores
    })
    hover_tool = HoverTool(
        tooltips=[('Masa corporal', '@posibilidades'), ('Numero', '@valores')]
    )
    chart_labels = {}
    for val1, val2 in zip(source.data['masa_corporal_int'], source.data['posibilidades']):
        chart_labels.update({int(val1): str(val2)})

    p = figure(tools=[hover_tool], plot_height=400, title='Masa Corporal')
    p.vbar(x='masa_corporal_int', top='valores', source=source, width=0.9,
        fill_color=factor_cmap('posibilidades', palette=palette_generator(len(source.data['posibilidades']), cpalette), factors=source.data['posibilidades']))

    plot_styler(p)
    p.xaxis.ticker = source.data['masa_corporal_int']
    p.xaxis.major_label_overrides = chart_labels
    p.xaxis.major_label_orientation = math.pi / 4
    p.sizing_mode = 'scale_width'

    return p


def variedad_sae_bar_chart(dataset, pass_class, cpalette=palette[1:4]):
    variedad_sae_data = dataset[dataset['escuela'] == int(pass_class)]
    variedad_sae_posibilidades = list(
        variedad_sae_data['variedad_sae'].value_counts().index)
    variedad_sae_valores = list(
        variedad_sae_data['variedad_sae'].value_counts().values)
    int_posibilidades = np.arange(len(variedad_sae_posibilidades))
    source = ColumnDataSource(data={
        'posibilidades': variedad_sae_posibilidades,
        'variedad_sae_int': int_posibilidades,
        'valores': variedad_sae_valores
    })
    hover_tool = HoverTool(
        tooltips=[('Variedad menu SAE', '@posibilidades'),
                ('Numero', '@valores')]
    )
    chart_labels = {}
    for val1, val2 in zip(source.data['variedad_sae_int'], source.data['posibilidades']):
        chart_labels.update({int(val1): str(val2)})

    p = figure(tools=[hover_tool], plot_height=400,
            title='Variedad del menu SAE')
    p.vbar(x='variedad_sae_int', top='valores', source=source, width=0.9,
        fill_color=factor_cmap('posibilidades', palette=palette_generator(len(source.data['posibilidades']), cpalette), factors=source.data['posibilidades']))

    plot_styler(p)
    p.xaxis.ticker = source.data['variedad_sae_int']
    p.xaxis.major_label_overrides = chart_labels
    p.xaxis.major_label_orientation = math.pi / 4
    p.sizing_mode = 'scale_width'

    return p


def cambra_bar_chart(dataset, pass_class, cpalette=palette):
    cambra_data = dataset[dataset['escuela'] == int(pass_class)]
    cambra_posibilidades = list(cambra_data['cambra'].value_counts().index)
    cambra_valores = list(cambra_data['cambra'].value_counts().values)
    int_posibilidades = np.arange(len(cambra_posibilidades))
    source = ColumnDataSource(data={
        'posibilidades': cambra_posibilidades,
        'cambra_int': int_posibilidades,
        'valores': cambra_valores
    })
    hover_tool = HoverTool(
        tooltips=[('Riesgo Cambra', '@posibilidades'), ('Numero', '@valores')]
    )
    chart_labels = {}
    for val1, val2 in zip(source.data['cambra_int'], source.data['posibilidades']):
        chart_labels.update({int(val1): str(val2)})

    p = figure(tools=[hover_tool], plot_height=400, title='Riesgo Cambra')
    p.vbar(x='cambra_int', top='valores', source=source, width=0.9,
        fill_color=factor_cmap('posibilidades', palette=palette_generator(len(source.data['posibilidades']), cpalette), factors=source.data['posibilidades']))

    plot_styler(p)
    p.xaxis.ticker = source.data['cambra_int']
    p.xaxis.major_label_overrides = chart_labels
    p.xaxis.major_label_orientation = math.pi / 4
    p.sizing_mode = 'scale_width'

    return p


def cariogenico_bar_chart(dataset, pass_class, cpalette=palette):
    cariogenico_data = dataset[dataset['escuela'] == int(pass_class)]
    cariogenico_posibilidades = list(
        cariogenico_data['cariogenico'].value_counts().index)
    cariogenico_valores = list(
        cariogenico_data['cariogenico'].value_counts().values)
    int_posibilidades = np.arange(len(cariogenico_posibilidades))
    source = ColumnDataSource(data={
        'posibilidades': cariogenico_posibilidades,
        'cariogenico_int': int_posibilidades,
        'valores': cariogenico_valores
    })
    hover_tool = HoverTool(
        tooltips=[('Riesgo Cariogenico', '@posibilidades'),
                ('Numero', '@valores')]
    )
    chart_labels = {}
    for val1, val2 in zip(source.data['cariogenico_int'], source.data['posibilidades']):
        chart_labels.update({int(val1): str(val2)})

    p = figure(tools=[hover_tool], plot_height=400, title='Riesgo Cariogenico')
    p.vbar(x='cariogenico_int', top='valores', source=source, width=0.9,
        fill_color=factor_cmap('posibilidades', palette=palette_generator(len(source.data['posibilidades']), cpalette), factors=source.data['posibilidades']))

    plot_styler(p)
    p.xaxis.ticker = source.data['cariogenico_int']
    p.xaxis.major_label_overrides = chart_labels
    p.xaxis.major_label_orientation = math.pi / 4
    p.sizing_mode = 'scale_width'

    return p


def higiene_bar_chart(dataset, pass_class, cpalette=palette):
    higiene_data = dataset[dataset['escuela'] == int(pass_class)]
    higiene_posibilidades = list(higiene_data['higiene'].value_counts().index)
    higiene_valores = list(higiene_data['higiene'].value_counts().values)
    int_posibilidades = np.arange(len(higiene_posibilidades))
    source = ColumnDataSource(data={
        'posibilidades': higiene_posibilidades,
        'higiene_int': int_posibilidades,
        'valores': higiene_valores
    })
    hover_tool = HoverTool(
        tooltips=[('Higiene', '@posibilidades'), ('Numero', '@valores')]
    )
    chart_labels = {}
    for val1, val2 in zip(source.data['higiene_int'], source.data['posibilidades']):
        chart_labels.update({int(val1): str(val2)})

    p = figure(tools=[hover_tool], plot_height=400,
            title='Condicion de higiene')
    p.vbar(x='higiene_int', top='valores', source=source, width=0.9,
        fill_color=factor_cmap('posibilidades', palette=palette_generator(len(source.data['posibilidades']), cpalette), factors=source.data['posibilidades']))

    plot_styler(p)
    p.xaxis.ticker = source.data['higiene_int']
    p.xaxis.major_label_overrides = chart_labels
    p.xaxis.major_label_orientation = math.pi / 4
    p.sizing_mode = 'scale_width'

    return p


def ecotecnias_bar_chart(dataset, pass_class, cpalette=palette):
    ecotecnias_data = dataset[dataset['escuela'] == int(pass_class)]
    ecotecnias_posibilidades = list(
        ecotecnias_data['ecotecnias'].value_counts().index)
    ecotecnias_valores = list(
        ecotecnias_data['ecotecnias'].value_counts().values)
    int_posibilidades = np.arange(len(ecotecnias_posibilidades))
    source = ColumnDataSource(data={
        'posibilidades': ecotecnias_posibilidades,
        'ecotecnias_int': int_posibilidades,
        'valores': ecotecnias_valores
    })
    hover_tool = HoverTool(
        tooltips=[('Ecotecnia', '@posibilidades'), ('Numero', '@valores')]
    )
    chart_labels = {}
    for val1, val2 in zip(source.data['ecotecnias_int'], source.data['posibilidades']):
        chart_labels.update({int(val1): str(val2)})

    p = figure(tools=[hover_tool], plot_height=400,
        title='Implementacion de ecotecnias')
    p.vbar(x='ecotecnias_int', top='valores', source=source, width=0.9,
        fill_color=factor_cmap('posibilidades', palette=palette_generator(len(source.data['posibilidades']), cpalette), factors=source.data['posibilidades']))

    plot_styler(p)
    p.xaxis.ticker = source.data['ecotecnias_int']
    p.xaxis.major_label_overrides = chart_labels
    p.xaxis.major_label_orientation = math.pi / 4
    p.sizing_mode = 'scale_width'

    return p
################################################################################
#                    - END OF CHART GENERATION FUNCTIONS -                     #
################################################################################

@app.route("/login_reportes",methods=["GET","POST"])
def login_reportes():
    if request.method=="POST":
        if request.form.get("password")=="clave123":
            global permiso
            permiso=True
            return redirect(url_for("reporte"))
        else:
            return redirect(url_for("chart"))

@app.route("/reporte",methods=["GET","POST"])
def reporte():
    global permiso
    if permiso:
        permiso=False
        return render_template("reportes.html")
    else: 
        return redirect(url_for("chart"))
############################################################################
# Generando el reporte
@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if request.method == 'POST':
        try:
            id = int(request.form.get("id"))
            if id:
                datos_anteriores = data[data["id"] == id]
                datos_nuevos = data2[data2["id"] == id]

                # datos para la tabla del informe
                datos = {"Talla para la edad": [datos_anteriores["talla_edad"].values[0],
                            datos_nuevos["talla_edad"].values[0]],
                            "Longitud relativa de pierna": [datos_anteriores["long_pierna"].values[0], 
                            datos_nuevos["long_pierna"].values[0]],
                            "Indice de masa corporal": [datos_anteriores["masa_corporal"].values[0],
                            datos_nuevos["masa_corporal"].values[0]],
                            "Riesgo Cambra": [datos_anteriores["cambra"].values[0],
                            datos_nuevos["cambra"].values[0]],
                            "Riesgo cariogenico": [datos_anteriores["cariogenico"].values[0],
                            datos_nuevos["cariogenico"].values[0]],
                            "Condicion de higiene": [datos_anteriores["higiene"].values[0],
                            datos_nuevos["higiene"].values[0]],
                            "Valoracion de lengua": [datos_anteriores["lengua_val"].values[0],
                            datos_nuevos["lengua_val"].values[0]],
                            "El alumno es": [datos_anteriores["alumno_es"].values[0], 
                            datos_nuevos["alumno_es"].values[0]],
                            "Preferencia de clima": [datos_anteriores["clima_preferido"].values[0], 
                            datos_nuevos["clima_preferido"].values[0]],
                            "Preferencia liquidos": [datos_anteriores["liquidos_pref"].values[0], 
                            datos_nuevos["liquidos_pref"].values[0]],
                            "Padecimiento frecuente": [datos_anteriores["padecimiento"].values[0], 
                            datos_nuevos["padecimiento"].values[0]],
                            "Tiende a tener": [datos_anteriores["tendencia"].values[0], 
                            datos_nuevos["tendencia"].values[0]],
                            "Apetitos mas comunes": [datos_anteriores["apetito"].values[0], 
                            datos_nuevos["apetito"].values[0]]}

                df = pd.DataFrame(datos)

                ## ahora generamos el html
                print_data(df,'./templates/report.html',f'Datos alumno con id {id}')

                #esto hace el reporte
                pdfkit.from_url('http://127.0.0.1:5000/ver_reporte', 'reporte.pdf',
                options={'page-size': 'Letter','orientation':'landscape'})
                return render_template("reportes.html",generado=True)
        except ValueError:
            return render_template("reportes.html",error=request.form.get("id"))

@app.route("/ver_reporte")
def ver_reporte():
    return render_template("report.html")

@app.route('/descarga')
def descarga():
    return send_file("reporte.pdf",download_name='reporte.pdf')

if __name__ == '__main__':
    app.run(debug=True)
