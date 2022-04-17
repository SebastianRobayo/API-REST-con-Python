from flask import Flask
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)

conexion = MySQL(app)

@app.route('/cursos')
def listarCursos():
    try:
        return "OK"
    except Exception as ex:
        return "Error"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()