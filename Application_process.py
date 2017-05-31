from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def show_menu():
    '''Renders the Query Menu'''
    return render_template('index.html')


@app.route("/mentors")
def mentors():
    '''Renders the query result with:
        - name of the mentors
        - name and country of schools'''
    return 'Mentors'


@app.route("/all-school")
def all_school():
    '''Renders the query result with:
        - name of the mentors
        - name and country of schools extended'''
    return 'All School'


@app.route("/mentors-by-country")
def mentors_by_country():
    '''Renders the query result with:
        - country
        - number of mentors'''
    return 'Mentors by Country'


@app.route("/contacts")
def contacts():
    '''Renders the query result with:
        - country
        - number of mentors'''
    return 'Contacts'


@app.route("/applicants")
def applicants():
    '''Renders the query result with:
        - name of appliciants
        - name of assigned mentors'''
    return 'Applicants'


@app.route("/applicants-and-mentors")
def appliciants_and_mentors():
    return 'Appliciants and Mentors'


if __name__ == '__main__':
    app.run(debug=True)
