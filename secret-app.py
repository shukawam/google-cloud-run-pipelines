import json, logging, os
from flask import Flask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route("/secret/file")
def greet_secret_file():
    try:
        with open('/secret/secret.json', mode='r', encoding='utf-8') as f:
            content = json.load(f)
            return content
    except FileNotFoundError:
        logger.error("File not found.")
        return "File not found."

@app.route("/secret/env")
def greet_secret_env():
    secret = os.getenv("SECRET")
    if secret is None:
        logger.error("SECRET not found.")
        return "SECRET not found."
    return secret


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
