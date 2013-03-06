#!/usr/bin/env python
from peewee import DateField, TextField, Model, SqliteDatabase, ForeignKeyField,\
    CharField
import unittest
import datetime

class NotesConfig:
    database = SqliteDatabase(None)

   

class ModelBase(Model):
    creationDate = DateField()
    class Meta:
        database = NotesConfig.database; 

        
class Basket(ModelBase):
    basketName = CharField()

class Note(ModelBase):
    basket = ForeignKeyField(Basket)
    text = TextField()

class Tag(ModelBase):
    tag = CharField()
    

class NoteTag(ModelBase):
    tag = ForeignKeyField(Tag)
    note = ForeignKeyField(Note)
    
        
class DBUtil:
    @staticmethod
    def createTables():
        Basket.create_table()
        Note.create_table()
        

class TesterBase(unittest.TestCase):
    def setUp(self):
        NotesConfig.database.init(":memory:")
        DBUtil.createTables()
    def tearDown(self):
        NotesConfig.database.close()
        NotesConfig.database.init(None)
            
    def testBasketSave(self):
        basket =  Basket()
        basket.basketName = "Hello world"
        basket.creationDate = datetime.date.today()
        basket.save()
        print basket.id
        
        basket =  Basket()
        basket.basketName = "Hello world"
        basket.creationDate = datetime.date.today()
        basket.save()
        print basket.id
     
    def testNoteSave(self):
        basket =  Basket()
        basket.basketName = "Hello world"
        basket.creationDate = datetime.date.today()
        basket.save()
        
        note = Note()
        note.text = "Hello note!!"
        note.basket = basket
        note.creationDate = datetime.date.today()
        note.save()
        print "Note saved", note.id
        
        
if __name__ == '__main__':
    unittest.main()