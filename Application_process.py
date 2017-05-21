import psycopg2
import os
import sys


def get_max_lengths(query_result):
    max_lengths = []
    for i in range(len(query_result[0])):
        max_length = max([len(str(item[i])) for item in query_result])
        max_lengths.append(max_length)
    return max_lengths


def print_table(query_result):
    query_result_fullname = []
    for i in query_result:
        temp_query_result = list(i[3:])
        temp_query_result.insert(0, " ".join(i[1:3]))
        query_result_fullname.append(tuple(temp_query_result))
    table_titles = ("Full name:", "Phone number:", "E-mail address:", "Application code:")
    query_result_fullname.insert(0, table_titles)
    lengths = get_max_lengths(query_result_fullname)
    sum_length = sum(lengths)+(2+3*3+2)
    print(sum_length*'-')
    for i, record in enumerate(query_result_fullname):
        if i == 0:
            print('| {:^{width_name}} | {:^{width_phone}} | {:^{width_email}} | {:^{width_app_code}} |'
                  .format(record[0],
                          record[1],
                          record[2],
                          record[3],
                          width_name=lengths[0],
                          width_phone=lengths[1],
                          width_email=lengths[2],
                          width_app_code=lengths[3],
                          ))
            print(sum_length*'-')
        if i > 0:
            print('| {:<{width_name}} | {:>{width_phone}} | {:<{width_email}} | {:^{width_app_code}} |'
                  .format(record[0],
                          record[1],
                          record[2],
                          record[3],
                          width_name=lengths[0],
                          width_phone=lengths[1],
                          width_email=lengths[2],
                          width_app_code=lengths[3],
                          ))
    print(sum_length*'-')
    return


def sql_get(sql_query, get_data=None):
    conn = psycopg2.connect("dbname=peter user=peter password=database")
    if get_data:
        with conn:
            with conn.cursor() as curs:
                curs.execute(sql_query, get_data)
                result_table = curs.fetchall()
        conn.close()
        return result_table
    else:
        with conn:
            with conn.cursor() as curs:
                curs.execute(sql_query)
                result_table = curs.fetchall()
        conn.close()
        return result_table


def sql_post(sql_post_query, input_data=None):
    conn = psycopg2.connect("dbname=peter user=peter password=database")
    if input_data:
        with conn:
            with conn.cursor() as curs:
                curs.execute(sql_post_query, input_data)
        conn.close()
    else:
        with conn:
            with conn.cursor() as curs:
                curs.execute(sql_post_query)
        conn.close()


def fullname_mentors():
    print("FULL NAME of MENTORS:\n")

    sql_query = """
                SELECT first_name, last_name
                FROM mentors;
                """
    query_result = sql_get(sql_query)
    for record in query_result:
        print("{} {}".format(record[0], record[1]))
    print("\n")
    input("\nPress Enter for Main Menu:")
    main()


def nickname_mentors_miskolc():
    print("NICKNAME of MENTORS at MISKOLC:\n")

    sql_query = """
                SELECT nick_name
                FROM mentors
                WHERE city = 'Miskolc';
                """

    query_result = sql_get(sql_query)
    for record in query_result:
        print("{}".format(record[0]))
    print("\n")
    input("\nPress Enter for Main Menu:")
    main()


def fullname_phone_carol():
    print("FULL NAME and PHONE NUMBER of 'CAROL':\n")

    sql_query = """
                SELECT first_name, last_name, phone_number
                FROM applicants
                WHERE first_name='Carol';
                """

    query_result = sql_get(sql_query)
    for record in query_result:
        print("{} {} -> {}".format(record[0], record[1], record[2]))
    print("\n")
    input("\nPress Enter for Main Menu:")
    main()


def fullname_phone_by_emaildomain():
    print("FULL NAME and PHONE NUMBER of applicants with email ending '@adipiscingenimmi.edu':\n")

    sql_query = """
                SELECT first_name, last_name, phone_number
                FROM applicants
                WHERE email LIKE '%@adipiscingenimmi.edu';
                """

    query_result = sql_get(sql_query)
    for record in query_result:
        print("{} {} -> {}".format(record[0], record[1], record[2]))
    print("\n")
    input("\nPress Enter for Main Menu:")
    main()


def add_new_record_markus():
    print("Add 'Markus Schaffarzyk' as a new applicant:\n")

    sql_post_query = """
                      INSERT INTO applicants (first_name, last_name, phone_number, email, application_code)
                      VALUES (%(first_name)s, %(last_name)s, %(phone_number)s, %(email)s, %(application_code)s);
                      """
    input_data = {'first_name': 'Markus',
                  'last_name': 'Schaffarzyk',
                  'phone_number': '003620/725-2666',
                  'email': 'djnovus@groovecoverage.com',
                  'application_code': '54823',
                  }
    sql_post(sql_post_query, input_data)
    sql_query = """
                SELECT *
                FROM applicants
                WHERE application_code = (%s);
                """
    get_data = (str(input_data['application_code']),)
    query_result = sql_get(sql_query, get_data)
    record = query_result[0]
    print("Full name:        {} {}".format(record[1], record[2]))
    print("Phone number:     {}".format(record[3]))
    print("E-mail address:   {}".format(record[4]))
    print("Application code: {}".format(record[5]))
    print("\n")
    input("\nPress Enter for Main Menu:")
    main()


def update_phone_jemima():
    print("Update the PHONE NUMBER of 'Jemima Foreman':\n")

    sql_query = """
                SELECT phone_number
                FROM applicants
                WHERE first_name = 'Jemima' AND last_name = 'Foreman';
                """
    query_result = sql_get(sql_query)
    record = query_result[0]
    print("OLD phone number: {}\n".format(record[0]))

    sql_post_query = """
                     UPDATE applicants
                     SET phone_number = '003670/223-7459'
                     WHERE first_name = 'Jemima' AND last_name = 'Foreman';
                     """
    sql_post(sql_post_query)

    sql_query = """
                SELECT phone_number
                FROM applicants
                WHERE first_name = 'Jemima' AND last_name = 'Foreman';
                """
    query_result = sql_get(sql_query)
    record = query_result[0]
    print("NEW phone number: {}".format(record[0]))
    print("\n")
    input("\nPress Enter for Main Menu:")
    main()


def delete_by_emaildomain():
    print("All the applicant has been deleted with e-mail for domain 'mauriseu.net':\n")
    sql_post_query = """
                     DELETE FROM applicants
                     WHERE email LIKE '%@mauriseu.net';
                     """
    sql_post(sql_post_query)

    sql_query = """
                SELECT *
                FROM applicants
                ORDER BY first_name ASC;
                """
    query_result = sql_get(sql_query)
    print("\n")
    input("\nPress Enter for Main Menu:")
    main()


def add_new_record():
    print("Add new applicant:\n")
    sql_post_query = """
                      INSERT INTO applicants (first_name, last_name, phone_number, email, application_code)
                      VALUES (%(first_name)s, %(last_name)s, %(phone_number)s, %(email)s, %(application_code)s);
                      """
    input_data = {'first_name': '',
                  'last_name': '',
                  'phone_number': '',
                  'email': '',
                  'application_code': '',
                  }
    input_data['first_name'] = input('First name: ')
    input_data['last_name'] = input('Last name: ')
    input_data['phone_number'] = input('Phone number: ')
    input_data['email'] = input('E-mail address: ')
    input_data['application_code'] = input('Application code: ')
    sql_post(sql_post_query, input_data)
    print("\n")
    input("\nPress Enter for Main Menu:")
    main()


def show_applicant_table():
    print("Applicants table:\n")
    sql_query = """
                SELECT *
                FROM applicants
                ORDER BY first_name ASC;
                """
    query_result = sql_get(sql_query)
    print_table(query_result)
    print("\n")
    input("\nPress Enter for Main Menu:")
    main()


def exit():
    sys.exit()


def function_handler(option):
    main_menu_functions = {1: fullname_mentors,
                           2: nickname_mentors_miskolc,
                           3: fullname_phone_carol,
                           4: fullname_phone_by_emaildomain,
                           5: add_new_record_markus,
                           6: update_phone_jemima,
                           7: delete_by_emaildomain,
                           11: add_new_record,
                           12: show_applicant_table,
                           0: exit,
                           }
    main_menu_functions[int(option)]()


def main():
    main_menu_titles = ["Get full name of mentors",
                        "Get nickname of mentors at Miskolc",
                        "Get full name and phone number of 'Carol'",
                        "Get full name and phone number of applicants with email '*@adipiscingenimmi.edu'",
                        "Add 'Markus Schaffarzyk' as a new applicant",
                        "Update phone number of 'Jemima Foreman'",
                        "Delete all applicants with email for domain 'mauriseu.net'",
                        "Add new applicant",
                        "View 'Applicant' table",
                        "Exit"
                        ]
    os.system('clear')
    print ("MAIN MENU", end='\n')
    print(9 * "-", end='\n')
    print()
    for title in main_menu_titles[:7]:
        print("{}. {}".format(main_menu_titles[:7].index(title) + 1, title), end='\n')
    print()
    for title in main_menu_titles[7:-1]:
        print("1{}. {}".format(main_menu_titles[7:-1].index(title) + 1, title), end='\n')
    print("\n0. {}".format(main_menu_titles[-1]))
    print("\n")
    option = input("Enter a number: ")
    os.system('clear')
    function_handler(option)


if __name__ == "__main__":
    main()
