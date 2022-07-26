from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Lenguajes(db.Model):
    id = db.Column(db.Integer, nullable = True, primary_key = True)
    nombre = db.Column(db.String(200), unique=True, nullable=False)
    ultima_version = db.Column(db.String(10), nullable=False)
    compilado = db.Column(db.Float, nullable=False)
    lanzamiento = db.Column(db.String(100), nullable=False)

    def __str__(self):
        if self.compilado==0:
            compilado = "No"
        else:
            compilado = "Si"
        return "Còdigo : {} \nNombre : {} \nÙltima versiòn : {} \nCompilado : {} \nLanzamiento : {}".format(
            self.id, self.nombre, self.ultima_version,compilado, self.lanzamiento)
    
    def serialize(self):
        if self.compilado==0:
            compilado = "No"
        else:
            compilado = "Si"
        return {
            "id":self.id,
            "nombre":self.nombre,
            "ultima_version":self.ultima_version,
            "compilado":compilado,
            "lanzamiento":self.lanzamiento
        }
