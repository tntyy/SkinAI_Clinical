from app import create_app
from app.database.seed import seed_all

app = create_app()

with app.app_context():
    seed_all()