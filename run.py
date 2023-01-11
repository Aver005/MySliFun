from os import getenv
from app import app

if __name__ == "__main__":
    app.run(port=int(getenv("PORT", 12345)))
