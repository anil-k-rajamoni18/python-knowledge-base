from flask import Flask
from flask import request, render_template
from auth.routes import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/hello")
def hello():
    return "Hi!"

@app.route("/user/<username>")
def user(username):
    return render_template("index.html", name=username)

@app.route("/product/<int:id>")
def product(id:int):
    return f"Product ID = {id}"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "Logged in"
    return "Login page"

if __name__ == "__main__":
    app.run(debug=True)