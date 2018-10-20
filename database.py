import pg8000
import configparser
import sys

login_details = {}

# connect to the database
def database_connect():
    # parse the config file
    config = configparser.ConfigParser()
    config.read("config.ini")

    connection = None
    #connect to database
    try:
        connection = pg8000.connect(database=config['DATABASE']['username'],
                                    user=config['DATABASE']['username'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])
    except pg8000.OperationalError as o:
        print("ERROR: Update your config.ini, or check your wifi with correct VPN details")
        print(o)
        exit(-1)
    except pg8000.ProgrammingError as p:
        print("ERROR: Check your password and username in the config.ini file")
        print(p)
        exit(-1)
    except Exception as e:
        print("ERROR: Some error occurred!")
        print(e)
        exit(-1)

    return connection
