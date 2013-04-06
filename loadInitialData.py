#!/usr/bin/env python
from model import Basket, NotesConfig, DBUtil, Note
import datetime

class DataLoader:
    def __init__(self):
        pass
    
    def createNotes(self):
        fileList = {"NotesMD": ("README.md", "data/credits.md", "data/about.md")
                    }
        for basket, notes in fileList.iteritems():
            dbBasket = Basket()
            dbBasket.basketName = basket
            dbBasket.creationDate = dbBasket.modificationDate = datetime.date.today()
            dbBasket.save()
            
            for note in notes:
                dbNote = Note()
                dbNote.basket = dbBasket
                dbNote.creationDate = dbNote.modificationDate = datetime.date.today()
                dbNote.text = open(note).read()
                dbNote.save()
        
if __name__ == '__main__':
    NotesConfig.database.init("/tmp/notes.db")
    DBUtil.createTables()
    DataLoader().createNotes()
