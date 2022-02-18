from flask import Flask,redirect,url_for,render_template,request
import operaciones as op
app=Flask(__name__)


@app.route('/',methods=['GET','POST'])
def home():
    escuelas=op.datos_esc()
    return render_template('index.html',escuelas=escuelas)

@app.route("/obtener_graficas",methods=['GET','POST'])
def obtener_graficas():
    if request.method=="POST":
        grafica = request.form.get('graficame')
        escuelas=op.datos_esc()
        return render_template('index.html',escuelas=escuelas,defecto=grafica)

if __name__ == '__main__':
    app.run(port=5000,debug=True)