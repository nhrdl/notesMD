#!/usr/bin/env python
from base import NotesMDObject, NotesConfig
import unittest
from peewee import TextField
import datetime

class Basket(NotesMDObject):
    notesText = TextField()
    pass


class TestBasket(unittest.TestCase):
    
    def setUp(self):
        NotesConfig.database.init(":memory:")
        Basket.create_table()
       
        
        
    def testSomething(self):
        basket =  Basket()
        basket.notesText = "Hello world"
        basket.creationDate = datetime.date.today()
        basket.save()
        print basket.id
        
        basket =  Basket()
        basket.notesText = "Hello world"
        basket.creationDate = datetime.date.today()
        basket.save()
        print basket.id
    
if __name__ == '__main__':
    unittest.main()