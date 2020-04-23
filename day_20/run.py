from day20 import create_app,mongo
from day20.main import User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(mg=mongo,user=User)
