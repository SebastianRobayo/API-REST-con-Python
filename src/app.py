from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)

conexion = MySQL(app)

# Controlador para listar varios
@app.route('/cursos', methods=['GET'])
def listarCursos():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT codigo, nombre, creditos FROM curso"
        cursor.execute(sql)
        datos=cursor.fetchall()
        cursos=[]
        for fila in datos:
            curso={'codigo':fila[0], 'nombre':fila[1], 'creditos':fila[2]}
            cursos.append(curso)            
        return jsonify({'cursos':cursos, 'mensaje':"Cursos listados"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

# Controlador para lista uno
@app.route('/cursos/<codigo>', methods=['GET'])
def leerCurso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT codigo, nombre, creditos FROM curso WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None: 
            curso={'codigo':datos[0], 'nombre':datos[1], 'creditos':datos[2]}
            return jsonify({'cursos':curso, 'mensaje':"Curso encontrado"})
        else:
            return jsonify({'mensaje':"Curso no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

# Controlador para registrar
@app.route('/cursos', methods=['POST'])
def registrarCurso():
    try:
        cursor=conexion.connection.cursor()
        sql="""INSERT INTO curso (codigo, nombre, creditos) 
        VALUES ('{0}', '{1}', {2})""".format(request.json['codigo'], request.json['nombre'], request.json['creditos'])
        cursor.execute(sql)
        conexion.connection.commit() # Confirma la acción de inserción
        return jsonify({'mensaje':"Curso registrado"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

# Controlador para eliminar
@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminarCurso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql="DELETE FROM curso WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        conexion.connection.commit() # Confirma la acción de inserción
        return jsonify({'mensaje':"Curso eliminado"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

# Controlador para editar
@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizarCurso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql="""UPDATE curso SET nombre = '{0}', creditos = '{1}' WHERE codigo = '{2}'""".format(request.json['nombre'], request.json['creditos'], codigo)
        cursor.execute(sql)
        conexion.connection.commit() # Confirma la acción de inserción
        return jsonify({'mensaje':"Curso actualizado"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

# Función para paginas no encontradas
def pagina_no_encontrada(error):
    return "<h1>La página que intentas buscar no existe...</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()