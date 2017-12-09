import psycopg2 as dbapi2

def initdb(dsn):
    try:
        global connection 
        connection = dbapi2.connect(dsn)
        print("Connected to database.")
    except:
        print("Database connection failed.")
    try:
        cursor = connection.cursor()
        statement = """CREATE TABLE IF NOT EXISTS company (
                    id SERIAL,
                    name VARCHAR(20),
                    number_of_employees INTEGER)"""
        cursor.execute(statement)
        statement = """CREATE TABLE IF NOT EXISTS users (
                    id SERIAL,
                    username VARCHAR(20),
                    password VARCHAR(100))"""
        cursor.execute(statement)
        connection.commit()
    except:
        print("Failed to create cursor.")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()

def addCompanyToDb(company_name, number_of_employees):
    try:
        cursor = connection.cursor()
        statement = """INSERT INTO company (name, number_of_employees)
                    VALUES (%s, %s)"""
        cursor.execute(statement, [company_name, number_of_employees])
        connection.commit()
    except:
        print("Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()

def listCompanies():
    try:
        cursor = connection.cursor()
        statement = """SELECT name, number_of_employees FROM company"""
        cursor.execute(statement)
        information = cursor.fetchall()
        return information
    except:
        print("Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()

def returnCompany(company_name):
    try:
        cursor = connection.cursor()
        statement = """SELECT * FROM company
                    WHERE name = %s"""
        cursor.execute(statement, [company_name])
        information = cursor.fetchall()
        return information
    except:
        print("Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()

def updateCompany(company_id, name, number_of_employees):
    try:
        cursor = connection.cursor()
        statement = """UPDATE company SET name = %s, number_of_employees = %s
                    WHERE (%s = id)"""
        cursor.execute(statement, [name, number_of_employees, company_id])
        connection.commit()
    except:
        print("Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()

def deleteCompany(company_id):
    try:
        cursor = connection.cursor()
        statement = """DELETE FROM company
                    WHERE (%s = id)"""
        cursor.execute(statement, [company_id])
        connection.commit()
    except:
        print("Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()

def getUserPwHash(username):
    try:
        cursor = connection.cursor()
        statement = """SELECT password FROM users
                    WHERE username = %s"""
        cursor.execute(statement, [username])
        hash = cursor.fetchall()
        return hash
    except:
        print("Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()


