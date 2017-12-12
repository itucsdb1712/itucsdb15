import psycopg2 as dbapi2
from psycopg2.psycopg1 import connection

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

        statement = """CREATE TABLE IF NOT EXISTS project (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(20),
                            company INTEGER REFERENCES company ON DELETE CASCADE)"""
        cursor.execute(statement)

        statement = """CREATE TABLE IF NOT EXISTS task (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(20),
                            priority INTEGER,
                            project INTEGER REFERENCES project ON DELETE CASCADE)"""
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
                    user_type INTEGER REFERENCES user_role ON DELETE CASCADE,
                    PRIMARY KEY (id))"""
        cursor.execute(statement)
        statement = """CREATE TABLE IF NOT EXISTS employee (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(20),
                    surname VARCHAR(20),
                    company INTEGER REFERENCES company ON DELETE CASCADE)"""
        try:
            cursor.execute(statement)
        except: 
            print("employee table cannot be created.")
        finally:
            connection.commit()
        
        statement = """CREATE TABLE IF NOT EXISTS project_of_employee (
                    employee_id INTEGER REFERENCES employee ON DELETE CASCADE,
                    project_id INTEGER REFERENCES project ON DELETE CASCADE,
                    PRIMARY KEY(employee_id, project_id))"""
        try:
            cursor.execute(statement)
        except: 
            print("project_of_employee table cannot be created.")
        finally:
            connection.commit()
        
        statement = """CREATE TABLE IF NOT EXISTS task_of_employee (
                    task_id INTEGER REFERENCES task ON DELETE CASCADE,
                    employee_id INTEGER REFERENCES employee ON DELETE CASCADE,
                    PRIMARY KEY(task_id, employee_id))"""
        try:
            cursor.execute(statement)
        except: 
            print("task_of_employee table cannot be created.")
        finally:
            connection.commit()
        connection.commit()
    except:
        print("Failed to create cursor.")
        connection.commit()
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

def returnAllProjects(company_id):
    try:
        cursor = connection.cursor()
        statement = """SELECT id, name FROM project
                    WHERE %s = company"""
        cursor.execute(statement, [company_id])
        information = cursor.fetchall()
        return information
    except:
        print("returnAllCompanies: Failed to create cursor or wrong SQL Statement")
        connection.commit()
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
        statement = """SELECT password, user_type FROM system_user WHERE username = %s"""
        cursor.execute(statement, [username])
        hash = cursor.fetchone()
        return hash
    except:
        print("getUserPwHash: Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()



def addTaskToDb(name, priority, project):
    try:
        cursor = connection.cursor()
        statement = """INSERT INTO task (name, priority, project) VALUES ( %s, %s, %s );"""
        cursor.execute(statement, [name, priority, project])
        connection.commit()
    except:
        print("addTaskToDb: Failed to create cursor or wrong SQL Statement")
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()

def getTasksFromDb(company_number):
    try:
        cursor = connection.cursor()
        statement = """SELECT task.id, task.name, priority, task.project
                    FROM task, project
                    WHERE task.project = project.id AND project.company = %s"""
        cursor.execute(statement, [company_number])
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
            connection.commit()
            cursor = None
        finally:
            if cursor is not None:
                cursor.close()

def updateTaskInDb(id, name, priority, project):
    try:
        cursor = connection.cursor()
        statement = """UPDATE task SET name=%s, priority=%s, project=%s WHERE (id = %s)"""
        cursor.execute(statement, [name, priority, project, id])
        connection.commit()
    except:
        print("updateTaskInDb: Failed to create cursor or wrong SQL Statement")
        connection.commit()
        cursor = None
    finally:
        if cursor is not None:
            cursor.close()

def getProjectsFromDb(company_id):
    try:
        cursor = connection.cursor()
    except:
        print('getProjectsFromDb: cursor creation has failed.')
        return
    statement = """SELECT * FROM project
                WHERE company = %s"""
    try:
        cursor.execute(statement, [company_id])
        information = cursor.fetchall()
    except:
        print('getProjectsFromDb: SQL command failed.')
    finally:
        connection.commit()
        cursor.close()
    return information

def deleteProjectFromDb(project_id):
    try:
        cursor = connection.cursor()
    except:
        print('deleteProjectFromDb: cursor creation has failed.')
        return
    statement = """DELETE FROM project
                WHERE id = %s"""
    try:
        cursor.execute(statement, [project_id])
    except:
        print('deleteProjectFromDb: SQL command failed.')
    finally:
        connection.commit()
        cursor.close()
        
def updateProjectInDb(name, project_id):
    try:
        cursor = connection.cursor()
    except:
        print('updateProjectInDb: cursor creation has failed.')
        return
    statement = """UPDATE project SET name=%s
                   WHERE (id = %s)"""
    try:
        cursor.execute(statement, [name, project_id])
    except:
        print('updateProjectInDb: SQL command failed.')
    finally:
        connection.commit()
        cursor.close()
        
def addProjectToDb(name, company_number):
    try:
        cursor = connection.cursor()
    except:
        print('addProjectToDp: cursor creation has failed.')
        return
    statement = """INSERT INTO project (name, company) VALUES (%s, %s )"""
    try:
        cursor.execute(statement, [name, company_number])
    except:
        print('addProjectToDp: SQL command failed.')
    finally:
        connection.commit()
        cursor.close()
        
def addEmployeeToDb(name, surname, company_id):
    try:
        cursor = connection.cursor()
    except:
        print('addEmployeeToDb: cursor creation has failed.')
        return
    statement = """INSERT INTO employee (name, surname, company) 
                   VALUES (%s, %s, %s )"""
    try:
        cursor.execute(statement, [name, surname, company_id])
    except:
        print('addEmployeeToDb: SQL command failed.')
    finally:
        connection.commit()
        cursor.close()
        
def getEmployeeFromDb(company_id):
    try:
        cursor = connection.cursor()
    except:
        print('getEmployeeFromDb: cursor creation has failed.')
        return
    statement = """SELECT * FROM employee 
                WHERE company = %s"""
    try:
        cursor.execute(statement, [company_id])
        information = cursor.fetchall()
    except:
        print('getEmployeeFromDb: SQL command failed.')
    finally:
        connection.commit()
        cursor.close()
    return information

def deleteEmployeeFromDb(employee_id):
    try:
        cursor = connection.cursor()
    except:
        print('deleteEmployeeFromDb: cursor creation has failed.')
        return
    statement = """DELETE FROM employee
                WHERE id = %s"""
    try:
        cursor.execute(statement, [employee_id])
    except:
        print('deleteEmployeeFromDb: SQL command failed.')
    finally:
        connection.commit()
        cursor.close()

def updateEmployeeInDb(name, surname, employee_id):
    try:
        cursor = connection.cursor()
    except:
        print('updateEmployeeInDb: cursor creation has failed.')
        return
    statement = """UPDATE employee SET name=%s, surname=%s
                   WHERE (id = %s)"""
    try:
        cursor.execute(statement, [name, surname, employee_id])
    except:
        print('updateEmployeeInDb: SQL command failed.')
    finally:
        connection.commit()
        cursor.close()

def returnEmployeeId(name):
    try:
        cursor = connection.cursor()
    except:
        print('returnEmployeeId: cursor creation has failed.')
        return
    statement = """SELECT id FROM employee
                WHERE name = %s"""
    try:
        cursor.execute(statement, [name])
        information = cursor.fetchone()
        return information
    except:
        print('returnEmployeeId: SQL command failed.')
    finally:
        connection.commit()
        cursor.close()

def createProjectEmployeeRelation(employee_id, project):
    try:
        cursor = connection.cursor()
    except:
        print('createProjectEmployeeRelation: cursor creation has failed.')
        return
    statement = """INSERT INTO project_of_employee VALUES (%s, %s)"""
    try:
        cursor.execute(statement, [employee_id, project])
    except:
        print('createProjectEmployeeRelation: SQL command failed. or passed')
    finally:
        connection.commit()
        cursor.close()
        
def returnAllTasks(name):
    try:
        cursor = connection.cursor()
    except:
        print('returnAllTasks: cursor creation has failed.')
        return
    statement = """SELECT DISTINCT ON (task.name) task.name, task.priority, project.name
                   FROM task, project_of_employee, project, employee
                   WHERE %s = employee.name AND employee.id = project_of_employee.employee_id
                   AND project_of_employee.project_id = project.id"""
    try:
        print(name)
        cursor.execute(statement, [name])
        information = cursor.fetchall()
        return information
    except:
        print('returnAllTasks: SQL command failed. or passed')
    finally:
        connection.commit()
        cursor.close()







