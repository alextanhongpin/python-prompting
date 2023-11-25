import google.generativeai as palm
import os
import app.db as db

palm.configure(api_key=os.environ["PALM_API_KEY"])

# The documentation can be found here:
# https://developers.generativeai.google/api/python/google/generativeai
model = palm.get_model("models/text-bison-001")


@db.persist(model="palm", db=db.get_db())
def generate_text(prompt):
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        max_output_tokens=8096,
    )

    return completion.result
