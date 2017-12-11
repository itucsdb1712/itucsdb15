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
                    number_of_employees INTEGER,
                    PRIMARY KEY (id))"""
        cursor.execute(statement)
        statement = """CREATE TABLE IF NOT EXISTS task (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(20),
                            priority INTEGER)"""
        cursor.execute(statement)
        statement = """CREATE TABLE IF NOT EXISTS user_role (
                    id SERIAL,
                    role VARCHAR(10),
                    PRIMARY KEY(id))"""
        cursor.execute(statement)
        statement = """CREATE TABLE IF NOT EXISTS system_user (
                    id SERIAL,
                    username VARCHAR(20),
                    password VARCHAR(100),
                    user_type INTEGER REFERENCES user_role,
                    PRIMARY KEY (id))"""
        cursor.execute(statement)

        connection.commit()
    except:
        print("Failed to create cursor.")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()

    try:
        cursor = connection.cursor()

        statement = """INSERT INTO user_role (id, role)
                    VALUES (1, 'admin')"""
        cursor.execute(statement)

        statement = """INSERT INTO user_role (id, role)
                    VALUES (2, 'company')"""
        cursor.execute(statement)

        statement = """INSERT INTO user_role (id, role)
                    VALUES (3, 'employee')"""
        cursor.execute(statement)

        statement = """INSERT INTO system_user (username, password, user_type)
                            VALUES ('admin', 'itucsdb1712', 1)"""
        cursor.execute(statement)

        connection.commit()
    except:
        print("User Roles already exists. Skip this stage")
        connection.commit()
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

def addUserToDb (username, password, user_type):
    try:
        cursor = connection.cursor()
        statement = """INSERT INTO system_user (username, password, user_type)
                    VALUES (%s, %s, %s)"""
        cursor.execute(statement, [username, password, user_type])
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
        print("returnCompany: Failed to create cursor or wrong SQL Statement")
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
        print("updateCompany: Failed to create cursor or wrong SQL Statement")
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
        print("deleteCompany: Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()
def deleteUser(username):
    try:
        cursor = connection.cursor()
        statement = """DELETE FROM system_user
                    WHERE (%s = username)"""
        cursor.execute(statement, [username])
        connection.commit()
    except:
        print("deleteCompany: Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()
    
def getUserPwHash(username):
    try:
        cursor = connection.cursor()
        statement = """SELECT password FROM system_user WHERE username = %s"""
        cursor.execute(statement, [username])
        hash = cursor.fetchone()
        return hash
    except:
        print("getUserPwHash: Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()



def addTaskToDb(name, priority):
    try:
        cursor = connection.cursor()
        statement = """INSERT INTO task (name, priority) VALUES ( %s, %s );"""
        cursor.execute(statement, [name, priority])
        connection.commit()
    except:
        print("addTaskToDb: Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()

def getTasksFromDb():
    try:
        cursor = connection.cursor()
        statement = """SELECT * FROM task"""
        cursor.execute(statement)
        tasks = cursor.fetchall()
        return tasks
    except:
        print("getTasksFromDb: Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()

def deleteTaskFromDb(id):
    try:
        cursor = connection.cursor()
        statement = """DELETE FROM task
                    WHERE (id = %s)"""
        cursor.execute(statement, [id])

        connection.commit()
    except:
        print("deleteTaskFromDb: Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()

