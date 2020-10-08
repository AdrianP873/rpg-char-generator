from app import *
from app.models import User, Character

# Create a shell context to avoid having to add db in shell each time. Open in 'flask shell'.
@app.shell_context_processor
def create_shell_context():
    return {'db': db, 'User': User, 'Character': Character}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")

