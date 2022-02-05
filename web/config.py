import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_IP = os.getenv("DATABASE_IP")
    DATABASE_DB = os.getenv("DATABASE_DB")

    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://{}:{}@{}/{}\
        ?driver=ODBC+Driver+17+for+SQL+Server".format(
        DATABASE_USER,
        DATABASE_PASSWORD,
        DATABASE_IP,
        DATABASE_DB
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
