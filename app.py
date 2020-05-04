import os

from citizens.app import create_app
from db import create_engine
from db.models import Base


if __name__ == '__main__':
    app = create_app()

    # export DATABASE_URL=postgresql://me:hackme@0.0.0.0/citizens
    db_url = os.environ['DATABASE_URL']
    print('DB_URL', db_url)
    engine = create_engine()
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    app.run(host='0.0.0.0', port=8080)
