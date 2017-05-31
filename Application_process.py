from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/", methods=['GET'])
def show_menu():
    '''Renders the Query Menu'''
    menu_list = ['the name of the mentors plus the name and country of the school',
                 'the name of the mentors plus the name and country of the school included all school',
                 'the number of the mentors per country',
                 'the name of the school plus the name of contact person at the school',
                 'the first name and the code of the applicants plus the creation date of the application',
                 'the first name and the code of the applicants plus the name of the assigned mentor',
                 ]
    url_list = [url_for('mentors'),
                url_for('all_school'),
                url_for('mentors_by_country'),
                url_for('contacts'),
                url_for('applicants'),
                url_for('appliciants_and_mentors'),
                ]
    print(menu_list)
    print('0000000000000000000000')
    print(url_list)
    return render_template('index.html',
                           menu_list=menu_list,
                           url_list=url_list,)


@app.route("/mentors/", methods=['GET'])
def mentors():
    '''Renders the query result with:
        - name of the mentors
        - name and country of schools'''
    return 'Mentors'


@app.route("/all-school/", methods=['GET'])
def all_school():
    '''Renders the query result with:
        - name of the mentors
        - name and country of schools extended'''
    return 'All School'


@app.route("/mentors-by-country/", methods=['GET'])
def mentors_by_country():
    '''Renders the query result with:
        - country
        - number of mentors'''
    return 'Mentors by Country'


@app.route("/contacts/", methods=['GET'])
def contacts():
    '''Renders the query result with:
        - country
        - number of mentors'''
    return 'Contacts'


@app.route("/applicants/", methods=['GET'])
def applicants():
    '''Renders the query result with:
        - name of appliciants
        - name of assigned mentors'''
    return 'Applicants'


@app.route("/applicants-and-mentors/", methods=['GET'])
def appliciants_and_mentors():
    return 'Appliciants and Mentors'


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
