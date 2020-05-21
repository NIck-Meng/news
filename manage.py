from app import create_app,db
from flask_script import Manager, Shell, Server
from app.models import Feed
import sys


env="online" if sys.platform.startswith("linux") else "default"


app=create_app(env)


manager=Manager(app)
manager.add_command("runserver", Server(use_debugger=True))

def make_shell_context():
    return dict(app=app,db=db,Feed=Feed)
manager.add_command('shell',Shell(make_context=make_shell_context))


if __name__=='__main__':
    manager.run()