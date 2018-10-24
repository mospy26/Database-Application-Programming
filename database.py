#!/usr/bin/env python3
"""
DeviceManagement Database module.
Contains all interactions between the webapp and the queries to the database.
"""

import configparser
import json
from modules import pg8000

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
	# Also, we are not doing anything to prevent sql injection in this code.
	# This is ok for a toy assignment, but do not use this code as a model when you are
	# writing a real system for a client or yourself.

    # TODO
    # Check if the user details are correct!
    # Return the relevant information (watch the order!)
    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()

    try:
        sql = """SELECT empid, name, homeAddress, dateOfBirth FROM Employee
        WHERE empID = %s and password = %s"""
        cur.execute(sql, (employee_id, password))
        r = cur.fetchone()
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
    """

    # TODO Dummy Data - Change to be useful!
    # Return a list of departments
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

        tuples = {
            'departments': manager_of
        }

        return tuples
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return False

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
    """

    # TODO Dummy Data - Change to be useful!
    # Return a list of devices issued to the user!
    # Each "Row" contains [ deviceID, manufacturer, modelNumber]
    # If no devices = empty list []

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

    # TODO Dummy Data - Change to be useful!
    # Return a list of departments

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """SELECT * FROM EmployeeDepartments
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

    # TODO Dummy Data - Change to be useful!
    # Return a list of devices issued to the user!
    # Each "Row" contains [ deviceID, purchaseDate, modelNumber, manufacturer ]
    # If no devices = empty list []

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



    # devices = [
    #     [7, '2017-08-28', 'Zava', '1146805551'],
    #     [8, '2017-09-22', 'Topicware', '5798231046'],
    #     [6123, '2017-09-05', 'Dabshots', '6481799600'],
    #     [1373, '2018-04-19', 'Cogibox', '6700815444'],
    #     [8, '2018-02-10', 'Feednation', '2050267274'],
    #     [36, '2017-11-05', 'Muxo', '8768929463'],
    #     [17, '2018-01-14', 'Izio', '5886976558'],
    #     [13, '2017-09-08', 'Skyndu', '5296853075'],
    #     [24, '2017-10-22', 'Yakitri', '8406089423'],
    # ]
    #
    # tuples = {
    #     'device_list': devices
    # }
    #
    # return tuples


#####################################################
#   Get All Devices
#####################################################

def get_all_devices():
    """
    Get all devices available including the model information.
    """

    # TODO Dummy Data - Change to be useful!
    # Return a list of devices issued to the user!
    # Each "Row" contains [ deviceID, purchaseDate, modelNumber, manufacturer ]
    # If no devices = empty list []

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


    # devices = [
    #     [7, '2017-08-28', 'Zava', '1146805551'],
    #     [8, '2017-09-22', 'Topicware', '5798231046'],
    #     [6123, '2017-09-05', 'Dabshots', '6481799600'],
    #     [1373, '2018-04-19', 'Cogibox', '6700815444'],
    #     [8, '2018-02-10', 'Feednation', '2050267274'],
    #     [36, '2017-11-05', 'Muxo', '8768929463'],
    #     [17, '2018-01-14', 'Izio', '5886976558'],
    #     [13, '2017-09-08', 'Skyndu', '5296853075'],
    #     [24, '2017-10-22', 'Yakitri', '8406089423'],
    # ]
    #
    # tuples = {
    #     'device_list': devices
    # }

    return tuples


#####################################################
#   Query (b)
#   Get All Models
#####################################################

def get_all_models():
    """
    Get all models available.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the list of models with information from the model table.
    # Each "Row" contains: [manufacturer, description, modelnumber, weight]
    # If No Models = EMPTY LIST []

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

    models = [
        ['Feednation', 'Expanded didactic instruction set', '2050267274', 31],
        ['Zoombox', 'Profit-focused global extranet', '8860068207', 57],
        ['Shufflebeat', 'Robust clear-thinking functionalities', '0288809602', 23],
        ['Voonyx', 'Vision-oriented bandwidth-monitored instruction set', '5275001460', 82],
        ['Tagpad', 'Fundamental human-resource migration', '3772470904', 89],
        ['Wordpedia', 'Business-focused tertiary orchestration', '0211912271', 17],
        ['Skyndu', 'Quality-focused web-enabled parallelism', '5296853075', 93],
        ['Tazz', 'Re-engineered well-modulated contingency', '8479884797', 95],
        ['Dabshots', 'Centralized empowering protocol', '6481799600', 68],
        ['Rhybox', 'Re-contextualized bifurcated orchestration', '7107712551', 25],
        ['Cogibox', 'Networked disintermediate application', '6700815444', 27],
        ['Meedoo', 'Progressive 24-7 orchestration', '3998544224', 43],
        ['Zoomzone', 'Reverse-engineered systemic monitoring', '9854941272', 50],
        ['Meejo', 'Secured static implementation', '3488947459', 75],
        ['Topicware', 'Extended system-worthy forecast', '5798231046', 100],
        ['Izio', 'Open-source static productivity', '5886976558', 53],
        ['Zava', 'Polarised incremental paradigm', '1146805551', 82],
        ['Demizz', 'Reduced hybrid website', '9510770736', 63],
        ['Muxo', 'Switchable contextually-based throughput', '8768929463', 40],
        ['Wordify', 'Front-line fault-tolerant middleware', '8465785368', 84],
        ['Twinder', 'Intuitive contextually-based local area network', '5709369365', 78],
        ['Jatri', 'Horizontal disintermediate workforce', '8271780565', 31],
        ['Chatterbridge', 'Phased zero tolerance architecture', '8429506128', 39],
    ]

    tuples = {
        'models': models
    }

    return tuples


#####################################################
#   Query (d[ii])
#   Get Device Repairs
#####################################################

def get_device_repairs(device_id):
    """
    Get all repairs made to a device.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the repairs done to a certain device
    # Each "Row" contains:
    #       - repairid
    #       - faultreport
    #       - startdate
    #       - enddate
    #       - cost
    #       - servicename (of who did the repair)
    # If no repairs = empty list

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """ SELECT repairID, faultreport, startdate, enddate, cost, servicename FROM Repair
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


    repairs = [
        [17, 'Never, The', '2018-07-16', '2018-09-22', '$837.13', 'TopDrive'],
        [18, 'Gonna', '2018-08-03', '2018-09-22', '$1726.99', 'Pikachu'],
        [19, 'Give', '2018-09-04', '2018-09-17', '$1751.01', 'INeedSleep'],
        [20, 'You', '2018-07-21', '2018-09-23', '$1496.36', 'PleaseHelp'],
        [21, 'Up', '2018-08-17', '2018-09-18', '$1133.88', 'IseeTheSun'],
        [22, 'Never', '2018-08-08', '2018-09-24', '$1520.95', 'BabySharkdooodoodooo'],
        [23, 'Gonna', '2018-09-01', '2018-09-29', '$611.09', 'McNuggies'],
        [24, 'Let', '2018-07-05', '2018-09-15', '$1736.03', 'ImaFirinMahLazor'],
    ]

    tuples = {
        'repairs': repairs
    }

    return tuples


#####################################################
#   Query (d[i]) + (d[iii/iv])
#   Get Device Info
#####################################################

def get_device_information(device_id):
    """
    Get related device information in detail.
    """

    # TODO Dummy Data - Change to be useful!
    # Return all the relevant device information for the device

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """ SELECT deviceID, serialnumber, purchasedate, purchasecost, manufacturer, modelnumber,
        description, weight FROM Device NATURAL JOIN Model WHERE  deviceID = %s"""
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
            'description': device_info[6],
            'weight': device_info[7],
        }

        return tuples
    except Exception as e:
        print("Some error occurred.")
        print(e)
    cur.close()
    conn.close()
    return None
    device_info = [
        1,                      # DeviceID
        '2721153188',           # SerialNumber
        '2017-12-19',           # PurchaseDate
        '$1009.10',             # PurchaseCost
        'Zoomzone',             # Manufacturer
        '9854941272',           # ModelNumber
        'what battery?',        # Description
        256,                    # Weight
    ]

    tuples = {
        'device_id': device_info[0],
        'serial_number': device_info[1],
        'purchase_date': device_info[2],
        'purchase_cost': device_info[3],
        'manufacturer': device_info[4],
        'model_number': device_info[5],
        'description': device_info[6],
        'weight': device_info[7],
    }

    return tuples


#####################################################
#   Query (f[ii])
#   Get Models assigned to Department
#####################################################

def get_department_models(department_name):
    """
    Return all models assigned to a department.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the models allocated to the department.
    # Each "row" has: [ manufacturer, modelnumber, maxnumber ]

    conn = database_connect()
    if conn is None:
        return None

    cur = conn.cursor()
    try:
        sql = """ SELECT manufacturer, modelnumber, maxnumber
                FROM Department D JOIN ModelAllocations MA ON (D.name = MA.department) JOIN Model M ON (M.modelNumber = MA.modelNumber AND M.manufacturer = MA.manufacturer)
                WHERE manager = %s"""
        cur.execute(sql, (device_id,))
        r = cur.fetchone()
        cur.close()
        conn.close()
        device_info = r
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

    model_allocations = [
        ['Devpulse', '4030141218', 153],
        ['Gabcube', '1666158895', 186],
        ['Feednation', '2050267274', 275],
        ['Zoombox', '8860068207', 199],
        ['Shufflebeat', '0288809602', 208],
        ['Voonyx', '5275001460', 264],
        ['Tagpad', '3772470904', 227],
    ]

    tuples = {
        'model_allocations': model_allocations
    }

    return tuples


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

    # TODO Dummy Data - Change to be useful!
    # Return the number of devices owned by each employee matching department,
    #   manufacturer and model.
    # Each "row" has: [ empid, name, number of devices issued that match ]

    employee_counts = [
        [1337, 'Misty', 20],
        [351, 'Pikachu', 1],
        [919, 'Hermione', 8],
    ]

    tuples = {
        'employee_counts': employee_counts
    }

    return tuples


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

    # TODO Dummy Data - Change to be useful!
    # Return each device of this model and whether the employee has it
    # issued.
    # Each "row" has: [ device_id, True if issued, else False.]

    device_assigned = [
        [123656, False],
        [123132, True],
        [51413, True],
        [8765, False],
    ]

    tuples = {
        'device_assigned': device_assigned,
    }

    return tuples


#####################################################
#   Query (f[iv])
#   Get a list of devices for this model and
#       manufacturer that have not been assigned.
#####################################################

def get_unassigned_devices_for_model(model_number, manufacturer):
    """
    Get all unassigned devices for the model.
    """

    # TODO Dummy Data - Change to be useful!
    # Return each device of this model that has not been issued
    # Each "row" has: [ device_id ]
    device_unissued = [123656, 123132, 51413, 8765]

    tuples = {
        'devices': device_unissued
    }

    return tuples


#####################################################
#   Query (f[iv])
#   Get Employees in Department
#####################################################

def get_employees_in_department(department_name):
    """
    Return the name of all employees in the department.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the employees in the department.
    # Each "row" has: [ empid, name ]

    employees = [
        ['15905', 'Rea Fibbings'],
        ['09438', 'Julia Norville'],
        ['36020', 'Adora Lansdowne'],
        ['98809', 'Nathanial Farfoot'],
        ['58407', 'Lynne Smorthit'],
    ]

    tuples = {
        'employees': employees
    }

    return tuples


#####################################################
#   Query (f[iv])
#   Get Device Employee Assignment
#####################################################

def get_device_employee_department(manufacturer, modelNumber, department_name):
    """
    Return the list of devices and who owns them for a given model
    and department.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the devices matching the manufacturer and model number in the
    #   department with the employees assigned.
    # Each row has: [ deviceid, serialnumber, empid, employee name ]

    device_employee = [
        [16, '5952579566', '71800', 'Bond James'],
        [17, '8357570070', '17804', 'Spongebob'],
        [18, '8019230513', '73946', 'Chez Grater'],
        [19, '5816272977', '81716', 'Totoro'],
        [20, '3768555569', '37387', 'Doraemon'],
        [21, '3079176995', '52675', 'Fred Weasley'],
        [22, '3804476813', '36020', 'George Weasley'],
    ]

    tuples = {
        'device_list': device_employee
    }

    return tuples


#####################################################
#   Query (f[v])
#   Issue Device
#####################################################

def issue_device_to_employee(employee_id, device_id):
    """
    Issue the device to the chosen employee.
    """

    # TODO issue the device from the employee
    # Return (True, None) if all good
    # Else return (False, ErrorMsg)
    # Error messages:
    #       - Device already issued?
    #       - Employee not in department?

    # return (False, "Device already issued")
    return (True, None)


#####################################################
#   Query (f[vi])
#   Revoke Device Issued to User
#####################################################

def revoke_device_from_employee(employee_id, device_id):
    """
    Revoke the device from the employee.
    """

    # TODO revoke the device from the employee.
    # Return (True, None) if all good
    # Else return (False, ErrorMsg)
    # Error messages:
    #       - Device already revoked?
    #       - employee not assigned to device?

    # return (False, "Device already unassigned")
    return (True, None)


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
