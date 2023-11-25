include .env
export

# Make sure to run `$ poetry shell` first.
server:
	@streamlit run app.py
