from app import create_app, db
from app.models import User, Post, Task, Manga, Message


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Task': Task, 'Manga': Manga, 'Message': Message}