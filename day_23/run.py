from coinapp import __call__,db
from coinapp.extensions import migrate
from coinapp.models import User,Wallet
import os

app = __call__('default' or os.getenv('FLASK_CONFIG'))
migrate.init_app(app,db)

@app.shell_context_processor
def make_shell_context():
    return dict(user=User,wallet=Wallet)