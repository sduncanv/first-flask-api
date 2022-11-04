
from flask import request, jsonify, Blueprint
from datetime import datetime

from database import tasks


tasks_bp = Blueprint('route-tasks', __name__)


@tasks_bp.route('/tasks', methods=['POST'])
def add_task():
    """
    Con esta función se podrá registrar una tarea.

    El json esperado para la creación de la tarea es:
    {
        "title": "tarea"
    }

    Para esto es importante tener en cuenta el método POST y la ruta '/tasks'
    """

    title = request.json['title']
    created_date = datetime.now().strftime('%x')

    data = (title, created_date)
    task_id = tasks.insert_task(data)

    if task_id:
        task = tasks.select_task_by_id(task_id)
        return jsonify({'task': task})
    return jsonify({'message': 'Internal Error'})


@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Con esta función se podrá leer todas las tareas y su estado actual.

    Para esto es importante tener en cuenta el método GET y la ruta '/tasks'
    """

    data = tasks.select_all_tasks()

    if data:
        return jsonify({'tasks': data})
    elif data == False:
        return jsonify({'message': 'Internal error'})
    else:
        return jsonify({'tasks': {}})


@tasks_bp.route('/tasks', methods=['PUT'])
def update_task():
    """
    Con esta función se podrá actualizar una tarea.

    El json esperado para la actualización de la tarea es:
    {
        "title": "tarea"
    }
    La información de este json recibido se utilizará para actualizar la noticia deseada. En el endpoint
    se enviará un parámetro 'id' tipo int para realizar la busqueda de la tarea en la base de datos.

    Para esto es importante tener en cuenta el método PUT y la ruta '/tasks?id=int'
    """

    title = request.json['title']
    id_arg = request.args.get('id')

    if tasks.update_task(id_arg, (title,)):
        task = tasks.select_task_by_id(id_arg)
        return jsonify(task)
    return jsonify({'message': 'Internal Error'})


@tasks_bp.route('/tasks', methods=['DELETE'])
def delete_task():
    """
    Con esta función se podrá eliminar una tarea.

    En el endpoint se enviará un parámetro 'id' tipo int para realizar la busqueda de la tarea en la base de datos.

    Para esto es importante tener en cuenta el método DELETE y la ruta '/tasks?id=int'
    """

    id_arg = request.args.get('id')

    if tasks.delete_task(id_arg):
        return jsonify({'task': 'Task deleted'})
    return jsonify({'message': 'Internal Error'})


@tasks_bp.route('/tasks/completed', methods=['PUT'])
def completed_task():
    """
    Con esta función se podrá cambiar el estado una tarea donde 0 es pendiente y 1 significa completada.

    En el endpoint se enviará un parámetro 'id' tipo int para realizar la busqueda de la tarea en la base de datos,
    adicinalmente se enviará otro parametro 'completed' con valor 1 para cambiar el estado.

    Para esto es importante tener en cuenta el método PUT y la ruta '/tasks/completed?id=1&completed=1'
    """
    id_arg = request.args.get('id')
    completed = request.args.get('completed')

    if tasks.complete_task(id_arg, completed):
        return jsonify({'task': 'Succesfully'})
    return jsonify({'message': 'Internal Error'})
