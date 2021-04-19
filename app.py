from flask import Flask, render_template, redirect, url_for
from dash_application import create_dash_application

app = Flask(__name__)

create_dash_application(app)

@app.route("/")
def index():
    return render_template("index.html")
    
    
if __name__ == "__main__":
    app.run(debug=True)