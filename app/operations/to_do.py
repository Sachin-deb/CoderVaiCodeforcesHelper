import sys
sys.path.append('./')
from connection import db_session
from app.model.sql_model import Todo

def create_to_do(todo: str): 
    try:
        new_todo = Todo(title=todo)
        db_session.add(new_todo)
        db_session.commit()
        return {
            'status': 'success',
            'message': 'To do created successfully'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': 'To do was not created',
            'error': str(e)
        }

def get_to_do():
    try:
        to_do = db_session.query(Todo).all()
        return {
            'status': 'success',
            'data': to_do
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': 'Could not fetch to do',
            'error': str(e)
        }

def update_to_do(todo_id: int, new_title: str):
    try:
        to_do = db_session.query(Todo).filter(Todo.id == todo_id).first()
        to_do.title = new_title
        db_session.commit()
        return {
            'status': 'success',
            'message': 'To do updated successfully'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': 'Could not update to do',
            'error': str(e)
        }

def delete_to_do(todo_id: int):
    try:
        to_do = db_session.query(Todo).filter(Todo.id == todo_id).first()
        db_session.delete(to_do)
        db_session.commit()
        return {
            'status': 'success',
            'message': 'To do deleted successfully'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': 'Could not delete to do',
            'error': str(e)
        }

res = create_to_do('Learn SQLAlchemy')
print(res)