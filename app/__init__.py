from app.db import PromptRepository, get_db

# Initialize the database.
repo = PromptRepository(get_db())
repo.create_tables()
