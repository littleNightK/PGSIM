import mysql.connector
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

def create_information_table():
    connect = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    password=config['database']['password'],
    database=config['database']['database']
)
    cursor = connect.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS information (
            `Citizen ref` VARCHAR(255) NOT NULL,
            `Citizen Name` VARCHAR(255) NOT NULL,
            `Citizen ID` VARCHAR(255) NOT NULL,
            `DOB` VARCHAR(255) NOT NULL,
            `Gender` VARCHAR(10) NOT NULL,
            `Address` VARCHAR(255) NOT NULL,
            `Marriage Status` VARCHAR(255) NOT NULL,
            `Status` VARCHAR(255) NOT NULL,
            PRIMARY KEY (`Citizen ID`)
        )
    """)
    connect.commit()
    cursor.close()
    connect.close()

def create_marriage_table():
    connect = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    password=config['database']['password'],
    database=config['database']['database']
)
    cursor = connect.cursor()
    cursor.execute("""
         CREATE TABLE IF NOT EXISTS `marriages` (
        `Citizen1_ID` VARCHAR(255) NOT NULL,
        `Citizen2_ID` VARCHAR(255) NOT NULL,
        `Date` VARCHAR(50),
        PRIMARY KEY (`Citizen1_ID`, `Citizen2_ID`)
    )
""")

def create_death_table():
    connect = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    password=config['database']['password'],
    database=config['database']['database']
)
    cursor = connect.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS death (
        `Citizen_ID` VARCHAR(255) NOT NULL,
        `Date of Death` VARCHAR(50),
        `Place of Death` VARCHAR(100),
        `Cause of Death` VARCHAR(100)

    )
""")
    connect.commit()
    cursor.close()
    connect.close()

def create_birth_table():
    connect = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    password=config['database']['password'],
    database=config['database']['database']
)
    cursor = connect.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS birth (
        `Name` VARCHAR(50),
        `ID` VARCHAR(50) PRIMARY KEY,
        `Father Name` VARCHAR(50),
        `Mother Name` VARCHAR(50),
        `Date of Birth` VARCHAR(50),
        `Place of Birth` VARCHAR(100),
        `Gender` VARCHAR(10)
    )
""")
    connect.commit()
    cursor.close()
    connect.close()
