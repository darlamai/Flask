#detrás de la página o backend
from flask import Flask, render_template, request
import pickle
from flask import jsonify 


##creación de aplicación
app=Flask(__name__)
print(__name__)
model= pickle.load(open('model.pkl','rb'))

#definir una ruta
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

@app.route('/app/v1/users', methods=['GET','POST'])
def users_action():
    print(request.form)
    print(request.method)
    if(request.method=="POST"):
        return "guardame en la base"
    else:
        return "no guardes"
    

allUser=[{"id":0, "nombre":"damian"},
         {"id":1, "nombre":"pepe"}]

@app.route('/app/v2/users/<id>', methods=["GET","POST"])
def user(id):
    return jsonify(allUser[int(id)])

if __name__=='__main__':
    app.run(debug=True) #modo de depuración

