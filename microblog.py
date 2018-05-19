from megatutApp import db, cli, create_app
from megatutApp.models import User, Post, Message, Notification, Task

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
	return {"db": db, "User": User, "Post": Post, "Message": Message, "Notification": Notification, "Task": Task}
