from peewee import SqliteDatabase
from basket import Basket
from note import Note
class NotesConfig:
    database = SqliteDatabase(None)

    @staticmethod
    def createTables():
        Basket.create_table()
        Note.create_table()
