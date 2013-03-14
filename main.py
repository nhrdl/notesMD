#!/usr/bin/env python

import cherrypy
import os
import threading
from gi.repository import WebKit 
from gi.repository import Gtk 
from gi.repository import GLib, GObject
from model import NotesConfig, Note, Basket, NoteTag, Tag, DBUtil
from os.path import expanduser

from mako.lookup import TemplateLookup
import datetime
import subprocess
import re
from peewee import fn
from loadInitialData import DataLoader

lookup = TemplateLookup(directories=['web'])
GObject.threads_init()

class RuntimeSettings:
    currentBasket = None
    @staticmethod
    def getTags():
        tags = []
        for tag in Tag.select():
            tags.append("'" + tag.tag.replace("'", "\\'") + "'")
        
        data = "[" + ",".join(tags) + "];"
        
        return data
        

class NotesWeb:
    
    @cherrypy.expose
    def index1(self):
        notes = Note.select()
        for note in notes:
            note.header = note.getHeader()
            print note.text
            
        tmpl = lookup.get_template("index.html")
        return tmpl.render(notes= notes)
    
    @cherrypy.expose
    def index(self, basket=None):
        #+ " collate nocase"
        baskets = Basket.select().order_by(fn.Lower(Basket.basketName))
        
        if (None == basket):
            theBasket = Basket.select().order_by(fn.Lower(Basket.basketName)).first()
        else:
            theBasket = Basket.get(Basket.id == basket)
            
        notes = theBasket.Notes
        for note in notes:
            note.header = note.getHeader()
            
        tmpl = lookup.get_template("container.html")
        RuntimeSettings.currentBasket = theBasket
        tags = RuntimeSettings.getTags()
        return tmpl.render(notes= notes, baskets=baskets, selectedBasket=theBasket, 
                           tagsList=tags, base = "file://" + NotesConfig.webDir + "/")
    
    @cherrypy.expose
    def edit(self, id):
        template = lookup.get_template("editor.html")
        return template.render(noteText=RuntimeSettings.currentNote.text)

class CherryPyStart(threading.Thread):
    def run(self):
        conf = {
        '/':
        {'tools.staticdir.dir': os.path.dirname(os.path.abspath(__file__)) + "/web",
         # 'tools.staticdir.index' : 'index.html',
         'tools.staticdir.on' : True
         },
          
        }
        cherrypy.tree.mount(NotesWeb(), "/", config=conf)
        cherrypy.engine.start()
        
         
#CherryPyStart().start()

    
exitLoop = False

def idleHookFunction(app):
    global exitLoop
   
    if (exitLoop):
        cherrypy.engine.stop()
        Gtk.main_quit()
    
    return True
    


    pass


class NotesApp:
    
    
    def exit(self, arg, a1):
        self.quit(arg)
        
    def quit(self, doesNotMatter):
        global exitLoop
        
        self.window.hide()
        exitLoop = True
        GLib.idle_add(idleHookFunction, app)    
            
    def newNote(self, webview):
        note = Note();
        note.creationDate = datetime.date.today()
        self.editNote(note)
        
    def editNote(self, note):
        RuntimeSettings.currentNote = note
        dialog = Gtk.Dialog(title="Dialog", parent=None, flags=0, 
                            buttons=(Gtk.STOCK_OK, Gtk.ResponseType.OK, Gtk.STOCK_CANCEL, 
                                     Gtk.ResponseType.CANCEL))
        box = dialog.get_content_area()
        view = WebKit.WebView()
        sw = Gtk.ScrolledWindow()
        sw.add(view)
        box.pack_start(sw, True, True, 5)
        view.open(NotesConfig.formUrl("edit?id=-1"))
        box.add(sw)
        box.show_all()
        dialog.maximize()
        response = dialog.run()
        if (Gtk.ResponseType.OK == response):
            element = self.getTextElement(view)
            text = element.get_value()
            
            note.basket = RuntimeSettings.currentBasket
            note.text = text
            note.modificationDate = datetime.date.today()
            note.save()
            self.view.reload()
        
        RuntimeSettings.currentNote = None    
        dialog.destroy()
        pass
    
    def getTextElement(self, frame):
        doc = frame.get_dom_document()
        element = doc.get_element_by_id("wmd-input")
        return element

    def displayContextMenu(self, view, menu, keyboard, data):
        print "Context menu", menu.get_children()
        for item in menu.get_children():
            print "Item", item.get_label()
            x = item.get_label()
            y = "_Back"
            if (y == item.get_label()):
                menu.remove(item)
        
    def addTag(self, noteId, strTag):
        count = Tag.select().where(Tag.tag == strTag).count()
        if (count == 0):
            dbTag = Tag()
            dbTag.creationDate = dbTag.modificationDate = datetime.date.today()
            dbTag.tag = strTag
            dbTag.save()
        else:
            dbTag = Tag.get(Tag.tag == strTag)
            
        note = Note.get(Note.id == noteId)
        noteTag = NoteTag()
        noteTag.note = note
        noteTag.tag = dbTag
        noteTag.creationDate = noteTag.modificationDate = datetime.date.today()
        noteTag.save() 
        
        self.view.execute_script("notesMD.tags = " + RuntimeSettings.getTags())
        
    def reload(self):
        template = NotesWeb().index(RuntimeSettings.currentBasket.id)
        self.view.load_string(template,"text/html", "UTF-8", "file://" + NotesConfig.webDir)
           
    def removeTag(self, noteId, strTag):
        tag = Tag.get(Tag.tag == strTag)
        NoteTag.get(NoteTag.note == noteId, NoteTag.tag == tag.id).delete_instance()
    
    def addBasket(self, basketName):
        basket = Basket()
        basket.creationDate = basket.modificationDate = datetime.date.today()
        basket.basketName = basketName
        basket.save()
        self.reload()
    
    def addDroppedNote(self, path):
        note = Note();
        note.modificationDate =  note.creationDate = datetime.date.today()
        note.basket =  RuntimeSettings.currentBasket
        note.text = path
        note.save()
        self.reload()
    
    def selectBasket(self, basket):
        template = NotesWeb().index(basket)
        self.view.load_string(template,"text/html", "UTF-8", "file://" + NotesConfig.webDir)
              
    def alert(self, view, frame, message):
        #print message
        m = re.search("^(\w+):([^_]+)_(\d+)(_(.*))?", message)
        if (m != None):
            action = m.group(1)
            id = m.group(3)
            print "Action", action, " id", id
            if (action == "EDIT"):
                note = Note.get(Note.id==id)
                self.editNote(note)
            if (action == "ADDTAG"):
                self.addTag(id, m.group(5))
            if (action == "REMOVETAG"):
                self.removeTag(id, m.group(5))
            if (action == "ADDNOTE"):
                self.newNote(None)
            if (action == "ADDBASKET"):
                self.addBasket(m.group(2))
            if (action == "ADDDROPPEDNOTE"):
                self.addDroppedNote(message[int(m.start(5)):])
            if (action == "SELECTBASKET"):
                self.selectBasket(m.group(5))
                
            return True
        else:
            return False
        
    def navigate(self, view, frame, request, action, decision):
       
        uri = request.get_uri()
        if (uri.startswith("notesmd://")):
            decision.ignore()
            uri = request.get_uri().replace("notesmd://", "").replace("[", "").replace("]", "")
            subprocess.call(["gnome-open", uri])
            return True
        if (uri.startswith("basket:")):
            decision.ignore()
            uri = request.get_uri().replace("basket:", "")
            
        return False
    
    def activate_inspector(self, inspector, view):  
        return self.inspectorView
              
    def __init__(self):
        win = Gtk.Window()
        agr = Gtk.AccelGroup()
        win.add_accel_group(agr)
        
        toolbar = Gtk.Toolbar()
        # toolbar.set_style(Gtk.ToobarStyle.GTTOOLBAR_ICONS)
        newNoteTb = Gtk.ToolButton(Gtk.STOCK_NEW)
        newNoteTb.connect("clicked", self.newNote)
        key, mod = Gtk.accelerator_parse("<Control>N")
        newNoteTb.add_accelerator("clicked", agr, key, mod, Gtk.AccelFlags.VISIBLE)
        
        sep = Gtk.SeparatorToolItem()
        quittb = Gtk.ToolButton(Gtk.STOCK_QUIT)
        quittb.connect("clicked", self.quit)
        toolbar.insert(newNoteTb, 0)
        toolbar.insert(sep, 1)
        toolbar.insert(quittb, 2)
        
        self.view = WebKit.WebView()
        sw = Gtk.ScrolledWindow() 
        sw.add(self.view) 

        
        vbox = Gtk.VBox()
        vbox.pack_start(toolbar, False, False, 0)
        win.add(vbox)
        vbox.add(sw)

        if (NotesConfig.showWebInspector):
            sw1 = Gtk.ScrolledWindow() 
            self.inspectorView = WebKit.WebView();
            sw1.add(self.inspectorView) 
            inspector = self.view.get_inspector()  
            inspector.connect("inspect-web-view",self.activate_inspector) 
            vbox.add(sw1)
        
        settings = self.view.get_settings()
        settings.set_property("enable-developer-extras",True)  
        settings.set_property("enable-file-access-from-file-uris", True)
        print settings.get_property("enable-file-access-from-file-uris")
        self.view.set_settings(settings)
        
        win.show_all() 
        win.connect("delete-event", self.exit)
        index = NotesWeb().index()
#        self.view.open(NotesConfig.formUrl( ""))
        self.view.load_string(index, "text/html", "UTF-8", "file://" + NotesConfig.webDir)       
        win.maximize()
        self.window = win
        self.view.connect("context-menu", self.displayContextMenu)
        self.view.connect("script-alert", self.alert)
        self.view.connect("navigation-policy-decision-requested", self.navigate)


home = expanduser("~")
NotesConfig.configPath = home + "/.config/notesMD"
if (os.path.isdir(NotesConfig.configPath) == False):
    os.makedirs(NotesConfig.configPath)

NotesConfig.webDir = "/home/niranjan/work/notesMD" +"/web"
    
dbPath = NotesConfig.configPath + "/notes.db"
NotesConfig.database.init(dbPath)

if (os.path.exists(dbPath) == False):
    DBUtil.createTables()
    DataLoader().createNotes()



app = NotesApp()

        
Gtk.main()


