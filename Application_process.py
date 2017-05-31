from flask import Flask

app = Flask(__name__)


@app.route("/")
def show_menu():
    '''Renders the SQL Query Menu'''
    pass

if __name__ == '__main__':
    app.run(debug=True)
