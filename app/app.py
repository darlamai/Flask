#detrás de la página o backend
from flask import Flask, render_template, request
import pickle


##creación de aplicación
app=Flask(__name__)
model= pickle.load(open('model.pkl','rb'))


@app.route('/') #@=modifica el comportamiento de una función, da el url / (página raíz) que desata la función
def home():
    return render_template('index.html')

@app.route("/predecir", methods=['POST']) #POST ENVIAR DATA
def predecir():
    puertas=float(request.form['# puertas'])
    tonelaje=float(request.form['tonelaje'])
    desplazamiento=float(request.form['desplazamiento'])
    capacidad=float(request.form['capacidad de pasajeros'])
    prediccion=model.predict([[puertas, tonelaje, desplazamiento,capacidad]]) 
    output= round(prediccion[0],2)
    return render_template('index.html', 
                           prediccion_texto=f'El vehículo con {puertas} puertas, {desplazamiento} metros de desplazamiento, {tonelaje} toneladas, {capacidad} pasajeros tiene kilometraje de {output} km')



if __name__=='__main__':
    app.run(debug=True) #modo de depuración

