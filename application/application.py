"""
This module runs the flask application when the __name__ variable is set to '__main__'.
If the source file is executed as the main program, the interpreter sets the __name__
variable as '__main__'. If this file is being imported from another module, __name__
will be set to the modules name.
"""

from app import app, db
from app.models import Character, User


@app.shell_context_processor
def create_shell_context():
    """ This function opens an interactive shell with 'flask shell'. """
    return {"db": db, "User": User, "Character": Character}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
