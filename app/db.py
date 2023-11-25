import functools
import sqlite3


con = sqlite3.connect("prompt.db", check_same_thread=False)


def get_db():
    return con


class PromptRepository:
    def __init__(self, con):
        self._con = con

    def create_tables(self):
        cur = self._con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT,
                prompt TEXT,
                completion TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self._con.commit()

    def insert(self, model, prompt, completion):
        cur = self._con.cursor()
        cur.execute(
            """
            INSERT INTO prompts (model, prompt, completion)
            VALUES (?, ?, ?)
            """,
            (model, prompt, completion),
        )
        self._con.commit()

    def get_all(self):
        cur = self._con.cursor()
        cur.execute("SELECT * FROM prompts")
        return cur.fetchall()

    def get_by_id(self, id):
        cur = self._con.cursor()
        cur.execute("SELECT * FROM prompts WHERE id = ?", (id,))
        return cur.fetchone()


def persist(model=None, db=None):
    """Decorator to persist the prompt and completion to a database."""
    if not db:
        raise ValueError("db must be provided")
    repo = PromptRepository(db)
    if not model:
        raise ValueError("model must be provided")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            prompt = args[0]
            completion = func(*args, **kwargs)

            repo.insert(model, prompt, completion)

            return completion

        return wrapper

    return decorator
