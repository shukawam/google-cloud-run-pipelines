from flask import Flask

app = Flask(__name__)

@app.route("/greet")
def greet():
    return "Hello world - demo"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
