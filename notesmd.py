#!/usr/bin/env python

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
    
    def header(self):
        template = lookup.get_template("header.html")
        return template.render(base = "file://" + NotesConfig.webDir + "/")
   
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
    
    def edit(self, id):
        template = lookup.get_template("editor.html")
        noteText=""
        if (None != RuntimeSettings.currentNote.text):
            noteText = RuntimeSettings.currentNote.text
            
        return template.render(noteText=noteText, base = "file://" + NotesConfig.webDir + "/")


class NotesApp:
    
    
    def exit(self, arg, a1):
        Gtk.main_quit()
        pass
        
    def quit(self, doesNotMatter):
        global exitLoop
        
        self.window.hide()
        exitLoop = True
        #GLib.idle_add(idleHookFunction, app)    
            
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
        settings = view.get_settings()
        settings.set_property("enable-file-access-from-file-uris", True)
        sw = Gtk.ScrolledWindow()
        sw.add(view)
        box.pack_start(sw, True, True, 5)
        template = NotesWeb().edit("-1");
       # view.open(NotesConfig.formUrl("edit?id=-1"))
        view.load_string(template, "text/html", "UTF-8", "file://" + NotesConfig.webDir)
        #box.add(sw)
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
            self.reload()
        
        RuntimeSettings.currentNote = None    
        dialog.destroy()
        pass
    
    def getTextElement(self, frame):
        doc = frame.get_dom_document()
        element = doc.get_element_by_id("wmd-input")
        return element

    def displayContextMenu(self, view, menu, keyboard, data):
        #print "Context menu", menu.get_children()
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
        f = open("/tmp/t.html", "w")
        f.write(template)
        f.close()
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

    def deleteNote(self, id):
        note = Note.get(Note.id == id)
        note.delete_instance()
        for noteTag in NoteTag.select().where(NoteTag.note == id):
            noteTag.delete_instance()
        self.reload()

    def searchText(self, text):
        self.view.search_text(text, False, True, True)
        self.view.set_highlight_text_matches(True)
                      
    def alert(self, view, frame, message):
        #print message
       
         
        m = re.search("^(\w+):([^_]+)_(\d+)(_(.*))?", message)
        if (m != None):
            action = m.group(1)
            id = m.group(3)
            #print "Action", action, " id", id
            if (action == "EDIT"):
                note = Note.get(Note.id==id)
                self.editNote(note)
            if (action == "ADDTAG"):
                self.addTag(id, m.group(5))
            if (action == "REMOVETAG"):
                self.removeTag(id, m.group(5))
            if (action == "ADDNOTE"):
                self.newNote(None)
                pass
            if (action == "ADDBASKET"):
                self.addBasket(m.group(2))
            if (action == "ADDDROPPEDNOTE"):
                self.addDroppedNote(message[int(m.start(5)):])
            if (action == "SELECTBASKET"):
                self.selectBasket(m.group(5))
            if (action == "DELETENOTE"):
                self.deleteNote(id)
            if (action == "SEARCH_TEXT"):
                self.searchText(m.group(5))
                    
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
        sw.add_with_viewport(self.view) 
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox = Gtk.VBox()
        win.add(vbox)
        
        self.headerView = WebKit.WebView()
        self.headerView.set_size_request(-1, 20)
        
        vbox.pack_start(self.headerView, False, False, 0)
        
        splitter = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)  
        vbox.add(splitter)
        
       # vbox = Gtk.VBox()
       # vbox.pack_start(toolbar, False, False, 0)
        sw.set_size_request( -1, 500)
        splitter.add1(sw)
        
       # vbox.add(sw)

        settings = self.view.get_settings()
        
        if (NotesConfig.showWebInspector):
            settings.set_property("enable-developer-extras",True)
            sw1 = Gtk.ScrolledWindow() 
            self.inspectorView = WebKit.WebView();
            sw1.add(self.inspectorView) 
            inspector = self.view.get_inspector()  
            inspector.connect("inspect-web-view",self.activate_inspector) 
            splitter.add2(sw1)
        #    vbox.add(sw1)
        
          
        settings.set_property("enable-file-access-from-file-uris", True)
        self.view.set_settings(settings)
        
        win.show_all() 
        
        
        win.connect("delete-event", self.exit)
        notesWeb = NotesWeb()
        index = notesWeb.index()
#        self.view.open(NotesConfig.formUrl( ""))
        self.view.load_string(index, "text/html", "UTF-8", "file://" + NotesConfig.webDir)   
        self.headerView.load_string(notesWeb.header(), "text/html", "UTF-8", "file://" + NotesConfig.webDir)
        
        self.view.set_highlight_text_matches(True)    
        win.maximize()
        self.window = win
        self.view.connect("context-menu", self.displayContextMenu)
        self.view.connect("script-alert", self.alert)
        self.headerView.connect("script-alert", self.alert)
        self.view.connect("navigation-policy-decision-requested", self.navigate)


home = expanduser("~")
NotesConfig.configPath = home + "/.config/notesMD"
if (os.path.isdir(NotesConfig.configPath) == False):
    os.makedirs(NotesConfig.configPath)

NotesConfig.webDir = os.path.dirname(os.path.realpath(__file__)) +"/web"
    
dbPath = NotesConfig.configPath + "/notes.db"
NotesConfig.database.init(dbPath)

if (os.path.exists(dbPath) == False):
    DBUtil.createTables()
    DataLoader().createNotes()



app = NotesApp()

        
Gtk.main()


