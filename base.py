#!/usr/bin/env python
from peewee import  Model, DateField, SqliteDatabase

class NotesConfig:
    database = SqliteDatabase(None)
    
class NotesMDObject(Model):
    creationDate = DateField()
    class Meta:
        database = NotesConfig.database; 
