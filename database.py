#!/usr/bin/env python3
"""
DeviceManagement Database module.
Contains all interactions between the webapp and the queries to the database.
"""

import configparser
import json
from modules import pg8000

# ----------------- Changes from new skeleton code v3 -----------------
# import datetime
# import setup_vendor_path  # noqa
# -------------------------------------------------------------------------------------



################################################################################
#   Welcome to the database file, where all the query magic happens.
#   My biggest tip is look at the *week 9 lab*.
#   Important information:
#       - If you're getting issues and getting locked out of your database.
#           You may have reached the maximum number of connections.
#           Why? (You're not closing things!) Be careful!
#       - Check things *carefully*.
#       - There may be better ways to do things, this is just for example
#           purposes
#       - ORDERING MATTERS
#           - Unfortunately to make it easier for everyone, we have to ask that
#               your columns are in order. WATCH YOUR SELECTS!! :)
#   Good luck!
#       And remember to have some fun :D
################################################################################


#####################################################
#   Database Connect
#   (No need to touch
#       (unless the exception is potatoing))
#####################################################

def database_connect():
    """
    Connects to the database using the connection string.
    If 'None' was returned it means there was an issue connecting to
    the database. It would be wise to handle this ;)
    """
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'database' not in config['DATABASE']:
        config['DATABASE']['database'] = config['DATABASE']['user']

    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pg8000.connect(database=config['DATABASE']['database'],
                                    user=config['DATABASE']['user'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])
    except pg8000.OperationalError as operation_error:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(operation_error)
        return None

    # return the connection to use
    return connection


#####################################################
#   Query (a + a[i])
#   Login
#####################################################

def check_login(employee_id, password):
    """
    Check that the users information exists in the database.
        - True => return the user data
        - False => return None
    """

	# Note: this example system is not well-designed for security.
	# There are several serious problems. One is that the database
	# stores passwords directly; a better design would "salt" each password
	# and then hash the result, and store only the hash.
	# This is ok for a toy assignment, but do not use this code as a model when you are
	# writing a real system for a client or yourself.

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()

    try:
        sql = """SELECT empid, name, homeAddress, dateOfBirth FROM Employee
        WHERE empID = %s and password = %s"""
        cur.execute(sql, (employee_id, password))
        r = cur.fetchone()
        if r is None:
            return None
        cur.close()
        conn.close()
        employee_info = r
        tuples = {
            'empid': employee_info[0],
            'name': employee_info[1],
            'homeAddress': employee_info[2],
            'dateOfBirth': employee_info[3],
        }

        return tuples
    except:
        print("Error Invalid Login")
    cur.close()
    conn.close()
    return None

#####################################################
#   Query (f[i])
#   Is Manager?
#####################################################

def is_manager(employee_id):
    """
    Check if the employee is a manager of a department.
        - True => Get the departments as a list.
        - False => Return None

     Get the department the employee is a manager of, if any.
    # Returns None if the employee doesn't manage a department.
    """

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()

    try:
        sql = """SELECT name FROM Department
        WHERE manager = %s;"""
        cur.execute(sql, (employee_id,))
        r = cur.fetchall()
        cur.close()
        conn.close()
        manager_of = r
        if len(r) == 0:
            return None
        tuples = {
            'departments': manager_of
        }

        return tuples
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return None

    #manager_of = ['RND', 'Accounting']

    #tuples = {
    #    'departments': manager_of
    #}

    #return tuples


#####################################################
#   Query (a[ii])
#   Get My Used Devices
#####################################################

def get_devices_used_by(employee_id):
    """
    Get all devices issued to the user.
        - Return a list of all devices to the user.
    Get a list of all the devices used by the employee.
    """

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """SELECT D.deviceID, D.manufacturer, D.modelNumber FROM Device D
				INNER JOIN DeviceUsedBy Du ON (D.deviceID = Du.deviceID)
                WHERE empID = %s"""
        cur.execute(sql, (employee_id,))
        r = cur.fetchall()
        cur.close()
        conn.close()
        devices = r

        tuples = {
            'device_list': devices
        }

        return tuples

    except Exception as e:
        print("Some error occurred.")
        print(e)
    cur.close()
    conn.close()
    return []





#####################################################
#   Query (a[iii])
#   Get departments employee works in
#####################################################

def employee_works_in(employee_id):
    """
    Return the departments that the employee works in.
    """

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """SELECT department FROM EmployeeDepartments
	              WHERE empID = %s"""
        cur.execute(sql, (employee_id,))
        r = cur.fetchall()
        cur.close()
        conn.close()
        departments = r

        tuples = {
            'departments': departments,
        }

        return tuples
    except Exception as e:
        print("Some error occurred.")
        print(e)
    cur.close()
    conn.close()
    return []


#####################################################
#   Query (c)
#   Get My Issued Devices
#####################################################

def get_issued_devices_for_user(employee_id):
    """
    Get all devices issued to the user.
        - Return a list of all devices to the user.
    """

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """SELECT deviceID, purchaseDate, manufacturer, modelNumber FROM Device
    	WHERE issuedTo = %s"""
        cur.execute(sql, (employee_id,))
        r = cur.fetchall()
        cur.close()
        conn.close()
        tuples = {
            'device_list': r
        }
        return tuples
    except Exception as e:
        print("Some error occurred.")
        print(e)
    cur.close()
    conn.close()
    return []

#####################################################
#   Get All Devices
#####################################################

def get_all_devices():
    """
    Get all devices available including the model information.
    """

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """SELECT * FROM Device"""
        cur.execute(sql)
        r = cur.fetchall()
        cur.close()
        conn.close()
        device_list = r
        tuples = {
            'device_list': device_list
        }

        return tuples
    except Exception as e:
        print("Some error occurred.")
        print(e)
    cur.close()
    conn.close()
    return []


#####################################################
#   Query (b)
#   Get All Models
#####################################################

def get_all_models():
    """
    Get all models available.
    """

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """SELECT manufacturer, description, modelNumber, Weight FROM Model"""
        cur.execute(sql)
        r = cur.fetchall()
        cur.close()
        conn.close()
        models = r
        tuples = {
            'models': models
        }

        return tuples

    except Exception as e:
        print("Some error occurred.")
        print(e)
    cur.close()
    conn.close()
    return []

#####################################################
#   Query (d[ii])
#   Get Device Repairs
#####################################################

def get_device_repairs(device_id):
    """
    Get all repairs made to a device.
    """

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """ SELECT repairID, faultreport, startdate, enddate, cost, servicename FROM Repair INNER JOIN Service ON(doneBy = abn)
                WHERE doneTo = %s"""
        cur.execute(sql, (device_id,))
        r = cur.fetchall()
        cur.close()
        conn.close()
        tuples = {
            'repairs': r
        }

        return tuples
    except Exception as e:
        print("Some error occurred.")
        print(e)
    cur.close()
    conn.close()
    return []

#####################################################
#   Query (d[i]) + (d[iii/iv])
#   Get Device Info
#####################################################

def get_device_information(device_id):
    """
    Get related device information in detail.
    """

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """ SELECT deviceID, serialnumber, purchasedate, purchasecost, manufacturer, modelnumber,
        issuedTo FROM Device NATURAL JOIN Model WHERE deviceID = %s"""
        cur.execute(sql, (device_id,))
        r = cur.fetchone()
        cur.close()
        conn.close()
        device_info = r
        tuples = {
            'device_id': device_info[0],
            'serial_number': device_info[1],
            'purchase_date': device_info[2],
            'purchase_cost': device_info[3],
            'manufacturer': device_info[4],
            'model_number': device_info[5],
            'issued_to': device_info[6],
        }

        return tuples
    except Exception as e:
        print("Some error occurred.")
        print(e)
    cur.close()
    conn.close()
    return None

#####################################################
#   Query (d[iii/iv])
#   Get Model Info by Device
#####################################################

def get_device_model(device_id):
    """
    Get model information about a device.
    """

    # TODO Dummy Data - Change to be useful!

    # ------------------------------------------ Feedback please. Not sure ------------------------------------------
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        sql = """SELECT M.manufacturer, M.modelnumber, M.description, M.weight
                       FROM Device NATURAL JOIN Model M
                       WHERE deviceid = %s;"""

        cur.execute(sql, (device_id,))
        r = cur.fetchone()
        cur.close()
        conn.close()
        model_info = r

        model = {
            'manufacturer': model_info[0],
            'model_number': model_info[1],
            'description': model_info[2],
            'weight': model_info[3],
        }
        return model

    except Exception as e:
        print("Some error occured.")
        print(e)
    cur.close()
    conn.close()
    return None

#####################################################
#   Query (e)
#   Get Repair Details
#####################################################

def get_repair_details(repair_id):
    """
    Get information about a repair in detail, including service information.
    """

    # TODO Dummy data - Change to be useful!

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """SELECT repairID, faultreport, startdate, enddate, cost, abn,
            serviceName, email, doneTo FROM Repair JOIN Service ON(doneBy = abn) WHERE repairID = %s"""

        cur.execute(sql, (repair_id,))
        repair_info = cur.fetchone()
        repair = {
            'repair_id': repair_info[0],
            'fault_report': repair_info[1],
            'start_date': repair_info[2],
            'end_date': repair_info[3],
            'cost': repair_info[4],
            'done_by': {
                'abn': repair_info[5],
                'service_name': repair_info[6],
                'email': repair_info[7],
            },
            'done_to': repair_info[8],
        }
        cur.close()
        conn.close()
        return repair
    except:
        print("Error")
    cur.close()
    conn.close()
    return None

# ------------------------------------------------------------------------------------------------------------------------------------

#####################################################
#   Query (f[ii])
#   Get Models assigned to Department
#####################################################

def get_department_models(department_name):
    """
    Return all models assigned to a department.
    """

    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """SELECT M.manufacturer, M.modelnumber, maxnumber
                FROM Department D JOIN ModelAllocations MA ON (D.name = MA.department) JOIN Model M ON (M.modelNumber = MA.modelNumber AND M.manufacturer = MA.manufacturer)
                WHERE name = %s"""
        cur.execute(sql, (department_name,))
        r = cur.fetchall()
        cur.close()
        conn.close()
        model_allocations = r
        tuples = {
            'model_allocations': model_allocations
        }

        return tuples
    except Exception as e:
        print("Some error occurred.")
        print(e)
    cur.close()
    conn.close()
    return None

#####################################################
#   Query (f[iii])
#   Get Number of Devices of Model owned
#   by Employee in Department
#####################################################

def get_employee_department_model_device(department_name, manufacturer, model_number):
    """
    Get the number of devices owned per employee in a department
    matching the model.

    E.g. Model = iPhone, Manufacturer = Apple, Department = "Accounting"
        - [ 1337, Misty, 20 ]
        - [ 351, Pikachu, 10 ]
    """

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """ SELECT empID, name, count(deviceid)
            FROM Employee JOIN Device ON(empid = issuedto) NATURAL JOIN EmployeeDepartments
            WHERE department = %s
            AND modelNumber = %s
            AND manufacturer = %s
            GROUP BY empID, name"""
        cur.execute(sql, (department_name, model_number, manufacturer))
        r = cur.fetchall()
        if len(r) == 0:
            return None
        cur.close()
        conn.close()
        employee_counts = r

        tuples = {
            'employee_counts': employee_counts
        }

        return tuples
    except Exception as e:
        print("Some error occurred.")
        print(e)
    cur.close()
    conn.close()
    return None

#####################################################
#   Query (f[iv])
#   Get a list of devices for a certain model and
#       have a boolean showing if the employee has
#       it issued.
#####################################################

def get_model_device_assigned(model_number, manufacturer, employee_id):
    """
    Get all devices matching the model and manufacturer and show True/False
    if the employee has the device assigned.

    E.g. Model = Pixel 2, Manufacturer = Google, employee_id = 1337
        - [123656, False]
        - [123132, True]
        - [51413, True]
        - [8765, False]
    """

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()

    try:
        sql = """SELECT
	                   deviceID,
	                   CASE
                            WHEN issuedTo = %s THEN 'True'
                            ELSE 'False'
                            END as issuedTo
                    FROM (Device
		                  Inner join Employee on(empid = issuedto))
                    WHERE
		                  manufacturer = %s
		                  and
		                  modelNumber = %s;"""

        cur.execute(sql, (employee_id, manufacturer, model_number))
        r = cur.fetchall()
        cur.close()
        conn.close()

        tuples = {
            'device_assigned': r,
        }

        return tuples

    except Exception as e:
        print("Some error occured.")
        print(e)
    cur.close()
    conn.close()
    return None

#####################################################
#   Query (f[iv])
#   Get a list of devices for this model and
#       manufacturer that have not been assigned.
#####################################################

def get_unassigned_devices_for_model(model_number, manufacturer):
    """
    Get all unassigned devices for the model.
    """

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """SELECT deviceID FROM Device WHERE issuedTo is NULL AND modelnumber = %s AND manufacturer = %s"""
        cur.execute(sql, (model_number, manufacturer))
        device_unissued = cur.fetchall()
        tuples = {
            'devices': device_unissued
        }
        cur.close()
        conn.close()
        return tuples
    except:
        print("Error in get_unassigned_devices_for_model")
    cur.close()
    conn.close()
    return None
    device_unissued = [123656, 123132, 51413, 8765]

#####################################################
#   Query (f[iv])
#   Get Employees in Department
#####################################################

def get_employees_in_department(department_name):
    """
    Return the name of all employees in the department.
    """

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """SELECT empid, name FROM EmployeeDepartments JOIN Employee USING(empid) WHERE
                department = %s"""
        cur.execute(sql, (department_name,))
        employees = cur.fetchall()
        tuples = {
            'employees': employees
        }
        cur.close()
        conn.close()
        return tuples
    except:
        print("Error in get_employees_in_department")
    cur.close()
    conn.close()
    return None

#####################################################
#   Query (f[iv])
#   Get Device Employee Assignment
#####################################################

def get_device_employee_department(manufacturer, modelNumber, department_name):
    """
    Return the list of devices and who owns them for a given model
    and department.
    """

    conn  = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()

    try:
        sql = """SELECT deviceid, serialnumber, empid, name FROM Device JOIN Employee ON(issuedTo=empID)
                JOIN EmployeeDepartments USING(empid) WHERE manufacturer = %s AND modelNumber = %s
                AND department = %s"""
        cur.execute(sql, (manufacturer, modelNumber, department_name))
        device_employee = cur.fetchall()
        tuples = {
            'device_list': device_employee
        }
        cur.close()
        conn.close()
        return tuples
    except:
        print("Error in get_device_employee_department")
    cur.close()
    conn.close()
    return None

#####################################################
#   Query (f[v])
#   Issue Device
#####################################################

def issue_device_to_employee(employee_id, device_id):
    """
    Issue the device to the chosen employee.
    """

    conn = database_connect()
    if conn is None:
        return (False, None)

    cur = conn.cursor()

    try:
        sql = """SELECT 1 FROM Device WHERE deviceid = %s AND issuedTo is NULL"""
        cur.execute(sql, (device_id,))
        r = cur.fetchone()
        if r is None:
            return (False, "Device already issued")

        sql = """UPDATE Device SET issuedTo = %s WHERE deviceID = %s"""
        cur.execute(sql, (employee_id, device_id))
        conn.commit()
        cur.close()
        conn.close()
        return (True, None)
    except:
        cur.close()
        conn.close()
        return (False, None)


#####################################################
#   Query (f[vi])
#   Revoke Device Issued to User
#####################################################

def revoke_device_from_employee(employee_id, device_id):
    """
    Revoke the device from the employee.
    """

    conn = database_connect()
    if conn is None:
        return (False, None)

    cur = conn.cursor()

    try:
        sql = """SELECT 1 FROM Device WHERE deviceid = %s AND issuedTo is NOT NULL"""
        cur.execute(sql, (device_id,))
        r = cur.fetchone()
        if r is None:
            return (False, "Device already revoked")

        sql = """SELECT 1 FROM Device WHERE deviceid = %s AND issuedTo = %s"""
        cur.execute(sql, (device_id, employee_id))
        r = cur.fetchone()
        if r is None:
            return (False, "Employee not assigned to device")

        sql = """UPDATE Device SET issuedTo = NULL WHERE issuedTo = %s and deviceid = %s"""
        cur.execute(sql, (employee_id, device_id))
        conn.commit()
        cur.close()
        conn.close()
        return (True, None)
    except:
        cur.close()
        conn.close()
        return (False, None)

#####################################################
#   Search model based on keyword in descrption.
#####################################################
def search_model(description):
    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        description = "%" + description + "%"
        sql = """SELECT manufacturer, description, modelNumber, Weight FROM Model WHERE
                upper(description) LIKE upper(%s) ORDER BY manufacturer"""
        cur.execute(sql, (description, ))
        r = cur.fetchall()
        #if len(r) == 0:
        #    return None
        cur.close()
        conn.close()
        models = r
        tuples = {
            'models': models
        }

        return tuples

    except Exception as e:
        print("Some error occurred.")
        print(e)
    cur.close()
    conn.close()
    return None

#####################################################
#   Filter models based on weight after keyword search
#####################################################
def search_model_by_weight(weights, description):
    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        r = []
        description = "%" + description + "%"
        for weight in weights:
            sql = """SELECT manufacturer, description, modelNumber, Weight FROM Model WHERE
            weight BETWEEN %s and %s AND upper(description) LIKE upper(%s) ORDER BY manufacturer"""
            if weight == 0:
                range = 20
            else:
                range = 19

            cur.execute(sql, (str(weight), str(int(weight) + range), description))
            r += cur.fetchall()
        cur.close()
        conn.close()
        models = r
        tuples = {
            'models': models
        }

        return tuples

    except Exception as e:
        print("Some error occurred.")
        print(str(e))
    cur.close()
    conn.close()
    return None

#####################################################
#   Edit information about the current user
#####################################################
def edit_details(empid, details):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        for d in details.keys():
            if d == 'name':
                sql = """UPDATE Employee SET name =%s WHERE empid =%s"""
                cur.execute(sql, (details[d],empid))
            if d == 'addr':
                sql = """UPDATE Employee SET homeAddress =%s WHERE empid =%s"""
                cur.execute(sql, (details[d],empid))
            if d == 'dob':
                sql = """UPDATE Employee SET dateOfBirth =%s WHERE empid =%s"""
                cur.execute(sql, (details[d],empid))
            if d == 'contact':
                sql = """UPDATE EmployeePhoneNumbers SET phoneNumber = %s WHERE empid =%s"""
                cur.execute(sql, (details[d],empid))
            if d == 'password':
                sql = """UPDATE Employee SET password = %s WHERE empid = %s"""
                cur.execute(sql, (details[d],empid))

        conn.commit()
        sql = """SELECT password FROM Employee WHERE empid = %s"""
        cur.execute(sql, (empid,))
        pwd = cur.fetchone()

        cur.close()
        conn.close()
        return check_login(empid, pwd[0])

    except Exception as e:
        print("Some error occurred.")
        print(str(e))
    cur.close()
    conn.close()
    return None

#####################################################
#   Search users in the managers department who do not use any models
#####################################################
def no_models(manager_id):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """SELECT empID, E.name, homeAddress FROM
            Employee E JOIN EmployeeDepartments USING(empID)
                    JOIN Department ON(Department.name = department)
                    WHERE manager = %s and EXISTS (SELECT E1.empid, COALESCE(COUNT(DeviceID), 0) AS no_of_devices
														FROM Employee E1 LEFT OUTER JOIN DeviceUsedBy USING(empid)
													  WHERE E.empid = E1.empid
														GROUP BY empid
														HAVING COUNT(DeviceID) = 0);"""
        cur.execute(sql, (manager_id,))
        r = cur.fetchall()
        cur.close()
        conn.close()
        tuples = {'employees': r}
        return tuples
    except Exception as e:
        print("Some error occured.")
        print(e)
    cur.close()
    conn.close()
    return None

# =================================================================
# =================================================================

#  FOR MARKING PURPOSES ONLY
#  DO NOT CHANGE

def to_json(fn_name, ret_val):
    """
    TO_JSON used for marking; Gives the function name and the
    return value in JSON.
    """
    return {'function': fn_name, 'res': json.dumps(ret_val)}

# =================================================================
# =================================================================
