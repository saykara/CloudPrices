from flask import Flask, render_template, request
from database import DatabaseOperations
app = Flask(__name__)


@app.route('/',  methods=['GET', 'POST'])
def main_page():
    if request.method == "GET":
        db = DatabaseOperations()
        db.create_tables()
        return render_template("index.html")
    else:
        return render_template("index.html")



if __name__ == '__main__':
    port = app.config.get("PORT", 5000)
    debug = True
    app.run(host='0.0.0.0', port=port, debug=debug)