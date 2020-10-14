from app import app, db
from app.models import Character, User


# Create shell context
@app.shell_context_processor
def create_shell_context():
    return {"db": db, "User": User, "Character": Character}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
