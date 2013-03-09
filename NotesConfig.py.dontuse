from peewee import SqliteDatabase
from model import Basket, Note

class NotesConfig:
    database = SqliteDatabase(None)

    @staticmethod
    def createTables():
        Basket.create_table()
        Note.create_table()
