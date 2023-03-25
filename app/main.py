import sys
from app import app
from controllers import index
from config import *

if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else None
    print(SQLALCHEMY_DATABASE_URI)
    app.run(host=host)
