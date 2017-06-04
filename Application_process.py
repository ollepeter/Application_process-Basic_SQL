from flask import Flask, render_template, url_for
import functions


app = Flask(__name__)


@app.route("/", methods=['GET'])
def show_menu():
    '''Renders the Query Menu'''
    menu_list = ['Mentors and schools',
                 'All school',
                 'Mentors by country',
                 'Contacts',
                 'Applicants',
                 'Applicants and mentors',
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
    '''Renders the query result with the following data:
        - name of mentor
        - name of school
        - country of school

        Oredered by "mentors.id"'''

    query = """
            SELECT  mentors.first_name AS "Mentor First Name",
                    mentors.last_name AS "Mentor Last Name",
                    schools.name AS "School",
                    schools.city AS "City"
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
    '''Renders the query result with the following data:
        - name of mentor
        - name of school
        - country of school

        Included schools without mentor

        Oredered by "mentors.id"'''

    query = """
            SELECT  mentors.first_name AS "Mentor First Name",
                    mentors.last_name AS "Mentor Last Name",
                    schools.name AS "School",
                    schools.city AS "City"
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
    '''Renders the query result with the following data:
        - country
        - number of mentors (by country)

        Oredered by "schools.country"'''

    query = """
            SELECT  schools.country AS "Country",
                    COUNT(mentors.id) AS "Number of Mentors"
            FROM mentors
            FULL JOIN schools
            ON mentors.city = schools.city
            GROUP BY schools.country
            ORDER BY schools.country;
            """

    query_result = functions.database_query(query)
    return render_template('query_result.html',
                           query_result=query_result,)


@app.route("/contacts/", methods=['GET'])
def contacts():
    '''Renders the query result with the following data:
        - name of school
        - name of contact person

        Oredered by "schools.country"'''

    query = """
            SELECT  schools.name AS "School",
                    mentors.first_name AS "Contact First Name",
                    mentors.last_name "Contact Last Name"
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
    '''Renders the query result with the following data:
        - first name of applicant
        - application code of applicant
        - date of application creation

        Only for applications later than 2016-01-01

        Oredered by "applicants_mentors.creation_date" in descending'''

    query = """
            SELECT  applicants.first_name AS "Applicant First Name",
                    applicants.application_code AS "Applicant Code",
                    applicants_mentors.creation_date AS "Application Date"
            FROM applicants
            INNER JOIN applicants_mentors
            ON applicants.id = applicants_mentors.applicant_id
            WHERE creation_date > '2016-01-01' OR creation_date ISNULL
            ORDER BY applicants_mentors.creation_date DESC;
            """

    query_result = functions.database_query(query)
    return render_template('query_result.html',
                           query_result=query_result,)


@app.route("/applicants-and-mentors/", methods=['GET'])
def appliciants_and_mentors():
    '''Renders the query result with the following data:
        - first name of applicant
        - application code of applicant
        - name of assigned mentor

        Included applicants without assigned mentor

        Oredered by "applicants.id"'''

    query = """
            SELECT  applicants.first_name AS "Applicant First Name",
                    applicants.application_code AS "Apllicant Code",
                    mentors.first_name AS "Mentor First Name",
                    mentors.last_name AS "Mentor Last Name"
            FROM applicants
            FULL JOIN applicants_mentors
            ON applicants.id = applicants_mentors.applicant_id
            LEFT JOIN mentors
            ON applicants_mentors.mentor_id = mentors.id
            ORDER BY applicants.id ASC
            """

    query_result = functions.database_query(query)
    return render_template('query_result.html',
                           query_result=query_result,)


if __name__ == '__main__':
    app.run(debug=True)
