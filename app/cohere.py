import cohere
import app.db as db
import os

co = cohere.Client(os.environ["COHERE_API_KEY"])


@db.persist(model="cohere", db=db.get_db())
def generate_text(prompt, **kwargs):
    # https://docs.cohere.com/reference/generate
    params = {
        "model": "command",
        "prompt": prompt,
        "temperature": 0,
    }
    params.update(kwargs)

    prediction = co.generate(**params)
    return prediction.generations[0].text
