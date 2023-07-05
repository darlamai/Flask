import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import pickle
from sklearn import linear_model

conn_string='postgresql+psycopg2://postgres:newpassword@localhost:5433/Inspecciones'
db=create_engine(conn_string)
query=f"SELECT * FROM vehiculos"
df = pd.read_sql(query, db)
base=df[["number_of_doors","tonnage","displacement","passengers_capacity","mileage"]]

#número de puertas
base['number_of_doors'] = pd.to_numeric(base['number_of_doors'])

#tonelaje
# Definir la lista de subcadenas originales y la lista de subcadenas de reemplazo
subcadenas_originales1 = ['0 75',',','SD','1 5',". 75",". 35",". 375",". 4","2 6",". 74","0n75",". 99","0 376",". 5" ]
subcadenas_nuevas1 = ['0.75','.','0','1.5',"0.75","0.35","0.375","0.4","2.6","0.74","0.75","0.99","0.376","0.5"]
# Reemplazar las subcadenas en la columna
for i in range(len(subcadenas_originales1)):
    base['tonnage'] = base['tonnage'].str.replace(subcadenas_originales1[i], subcadenas_nuevas1[i])
base['tonnage'] = pd.to_numeric(base['tonnage'])

#desplazamiento
# Definir la lista de subcadenas originales y la lista de subcadenas de reemplazo
subcadenas_originales = ['CC', 'cc', 'Cc','C','.cc','cc .','CC.','.' ]
subcadenas_nuevas = ['','','','','','','','']
# Reemplazar las subcadenas en la columna
for i in range(len(subcadenas_originales)):
    base['displacement'] = base['displacement'].str.replace(subcadenas_originales[i], subcadenas_nuevas[i])

base['displacement'] = pd.to_numeric(base['displacement'])

#capacidad de pasajeros
base['passengers_capacity'] = pd.to_numeric(base['passengers_capacity'])

#kilometraje

base['mileage'] = pd.to_numeric(base['mileage'])

#nulos con mediana 
base = base.fillna(base.median())

############MODELO#################################3

# Variable dependiente 
y=base['mileage']

#Variable independiente
X=base[['number_of_doors','tonnage','displacement','passengers_capacity']]

lm=linear_model.LinearRegression()
lm.fit(X,y)
pickle.dump(lm, open('model.pkl','wb'))

print(lm.predict([[2,3.5,1000,50]]))
print(f'score:{lm.score(X,y)}')







