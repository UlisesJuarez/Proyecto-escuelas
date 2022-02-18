from flask import Flask,redirect,url_for,render_template,request
import operaciones as op
app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    escuelas=op.datos_esc()
    return render_template('index.html',escuelas=escuelas)

if __name__ == '__main__':
    app.run(port=5000,debug=True)