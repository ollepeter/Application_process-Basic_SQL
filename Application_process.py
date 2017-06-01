from flask import Flask, render_template, url_for
import functions


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
    return render_template('index.html',
                           menu_list=menu_list,
                           url_list=url_list,)


@app.route("/mentors/", methods=['GET'])
def mentors():
    '''Renders the query result with:
        - name of the mentors
        - name and country of schools'''
    query = """
            SELECT mentors.id, mentors.first_name, mentors.last_name, schools.name, schools.city
            FROM mentors
            INNER JOIN schools
            ON mentors.city = schools.city
            ORDER BY mentors.id;
            """
    query_result = functions.database_query(query)
    return render_template('query_result.html',
                           query_result=query_result,)


@app.route("/all-school/", methods=['GET'])
def all_school():
    '''Renders the query result with:
        - name of the mentors
        - name and country of schools extended'''
    query = """
            SELECT mentors.id, mentors.first_name, mentors.last_name, schools.name, schools.city
            FROM mentors
            RIGHT JOIN schools
            ON mentors.city = schools.city
            ORDER BY mentors.id;
            """
    query_result = functions.database_query(query)
    return render_template('query_result.html',
                           query_result=query_result,)


@app.route("/mentors-by-country/", methods=['GET'])
def mentors_by_country():
    '''Renders the query result with:
        - country
        - number of mentors'''
    query = """
            SELECT  schools.country AS "Country", COUNT(mentors.id) AS "Number of Mentors"
            FROM mentors
            FULL JOIN schools
            ON mentors.city = schools.city
            GROUP BY country
            ORDER BY country;
            """
    query_result = functions.database_query(query)
    return render_template('query_result.html',
                           query_result=query_result,)


@app.route("/contacts/", methods=['GET'])
def contacts():
    '''Renders the query result with:
        - country
        - number of mentors'''
    query = """
            SELECT  schools.name AS "School", mentors.first_name AS "Contact First Name", mentors.last_name "Contact Last Name"
            FROM mentors
            INNER JOIN schools
            ON mentors.id = schools.contact_person
            ORDER BY name ASC;
            """
    query_result = functions.database_query(query)
    return render_template('query_result.html',
                           query_result=query_result,)


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
