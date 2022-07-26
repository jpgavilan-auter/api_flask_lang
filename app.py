from flask import Flask, jsonify,request
from models import db,Lenguajes
import json
from flask_jwt_extended import set_access_cookies, create_access_token, get_jwt_identity, jwt_required,get_jwt, get_jwt_identity, JWTManager
from datetime import timedelta, datetime, timezone

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.config["JWT_SECRET_KEY"] = 'super-secret'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)



@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username,additional_claims={"isAdmin":True,"id":4})
    return jsonify(access_token=access_token)


@app.route("/")
@jwt_required()
def index():
    return "<h1>Bienvenido de nuevo</h1>"

@app.route("/api/lenguaje", methods=["GET"])
def getLanguaje():
    try:
        id = request.args["id"]        
        languaje = Lenguajes.query.filter_by(id=id).first_or_404()     
        return jsonify(languaje.serialize()),200
    except Exception as ex:
        print(ex)
        return jsonify({"msg":"Lo sentimos a ocurrido un error"}),500

@app.route("/api/lenguaje/<int:id>", methods=["GET"])
def getLanguajeById(id):
    print(type(id))
    try:        
        languaje = Lenguajes.query.get(id)     
        print(languaje)
        return jsonify(languaje.serialize()),200
    except Exception as ex:
        print(ex)
        return jsonify({"msg":"Lo sentimos a ocurrido un error"}),500

@app.route("/api/lenguaje/<name>", methods=["GET"])
def getLanguajeByName(name):    
    try:        
        languajes = Lenguajes.query.filter(Lenguajes.nombre.like('%'+name+'%')).all()
        print(languajes)
        toReturn = [l.serialize() for l in languajes]
        return jsonify(toReturn),200
    except Exception as ex:
        print(ex)
        return jsonify({"msg":"Lo sentimos a ocurrido un error"}),500

@app.route("/api/lenguajes", methods=["GET"])
def getLanguajes():
    try:
        languajes = Lenguajes.query.order_by(Lenguajes.id.desc()).limit(10).all()
        toReturn = [l.serialize() for l in languajes]
        return jsonify(toReturn),200
    except Exception as ex:
        print(ex)
        return jsonify({"msg":"Lo sentimos a ocurrido un error"}),500




@app.route("/api/lenguaje", methods=["POST"])
def add_languaje():
    try:
        request_data = request.get_json()
        print(request_data)
        lang = Lenguajes()
        lang.nombre = request_data["nombre"]
        lang.ultima_version = request_data["ultima_version"]
        lang.compilado = request_data["compilado"]
        lang.lanzamiento = request_data["lanzamiento"]
        db.session.add(lang)
        db.session.commit()
        return jsonify({"msg":lang.serialize()}),200
    except Exception as ex:
        print(ex)
        return jsonify({"msg":"Ocurrio un error agregando el lenguaje"}),500

@app.route("/api/lenguaje", methods=["PUT"])
def update_languaje():
    try:
        request_data = request.get_json()
        print(request_data)
        dictt = json.loads(request.get_data())
        lang = Lenguajes()        
        lang.id = request_data["id"]
        lang.nombre = request_data["nombre"]
        lang.ultima_version = request_data["ultima_version"]
        lang.compilado = request_data["compilado"]
        lang.lanzamiento = request_data["lanzamiento"]
        Lenguajes.query.filter_by(id=lang.id).update(dictt)
        db.session.commit()
        return jsonify({"msg":lang.serialize()}),200
    except Exception as ex:
        print(ex)
        return jsonify({"msg":"Ocurrio un error actualizando el lenguaje"}),500

@app.route("/api/delete/lenguaje", methods=["DELETE","POST"])
def delete_lenguaje():
    try:
        #id = request.args["id"]
        #print(id)
        request_data = request.get_json()
        #print(request_data)
        lenguaje = Lenguajes.query.filter_by(id=request_data["id"]).first()
        #lenguaje = Lenguajes.query.filter_by(id=id).first()
        db.session.delete(lenguaje)
        db.session.commit()
        return jsonify({"msg":"Lenguaje eliminado correctamente"}),200
    except Exception as ex:
        print(ex)
        return jsonify({"msg":"Error al eliminar"}),500
if __name__ == "__main__":
    app.run(debug=True,port=4000,host='0.0.0.0')