import psycopg2 as dbapi2

def initdb(string):
    with dbapi2.connect(string) as connection:
        with connection.cursor() as cursor:
            statement = """CREATE TABLE company (
                        company_name varchar(10),
                        number_of_employee integer
                        );"""
            cursor.execute(statement)