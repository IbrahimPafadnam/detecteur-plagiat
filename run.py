from app import create_app, db
from flask_migrate import Migrate

from config import Config

app = create_app(config=Config)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()