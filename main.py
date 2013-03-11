#!/usr/bin/env python

import cherrypy
import os
import threading
import gi
from gi.repository import WebKit 
from gi.repository import Gtk 
from gi.repository import GLib, GObject
from model import NotesConfig, Note, Basket

from mako.lookup import TemplateLookup
import datetime
import time
import subprocess

lookup = TemplateLookup(directories=['web'])
GObject.threads_init()

class RuntimeSettings:
    currentBasket = None

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
        baskets = Basket.select().order_by(Basket.basketName)
        
        if (None == basket):
            theBasket = Basket.select().order_by(Basket.basketName).first()
        else:
            theBasket = Basket.get(Basket.id == basket)
            
        notes = theBasket.Notes
        for note in notes:
            note.header = note.getHeader()
            
        tmpl = lookup.get_template("container.html")
        RuntimeSettings.currentBasket = theBasket
        return tmpl.render(notes= notes, baskets=baskets, selectedBasket=theBasket)
    
    @cherrypy.expose
    def edit(self, id):
        template = lookup.get_template("editor.html")
        return template.render()

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
        
         
CherryPyStart().start()

    
exitLoop = False

def idleHookFunction(app):
    global exitLoop
   
    if (exitLoop):
        cherrypy.engine.stop()
        Gtk.main_quit()
    
    return True
    
class NotesApp:
    
    
    def exit(self, arg, a1):
        self.quit(arg)
        
    def quit(self, doesNotMatter):
        global exitLoop
        
        self.window.hide()
        exitLoop = True
        GLib.idle_add(idleHookFunction, app)    
            
    def newNote(self, webview):
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
            note = Note();
            note.basket = RuntimeSettings.currentBasket
            note.text = text
            note.creationDate = note.modificationDate = datetime.date.today()
            note.save()
            self.view.reload()
        
            
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
        
        
    def alert(self, view, frame, message):
        print message
        return True
        
    def navigate(self, view, frame, request, action, decision):
        decision.ignore()
        print "A", request.get_uri()
        uri = request.get_uri().replace("notesmd://", "").replace("[", "").replace("]", "")
        print "URI", uri
        #Gtk.show_uri(None, uri, time.time())
        subprocess.call(["gnome-open", uri])
        return True
        
            
    def __init__(self):
       
        toolbar = Gtk.Toolbar()
        # toolbar.set_style(Gtk.ToobarStyle.GTTOOLBAR_ICONS)
        newNoteTb = Gtk.ToolButton(Gtk.STOCK_NEW)
        newNoteTb.connect("clicked", self.newNote)
        sep = Gtk.SeparatorToolItem()
        quittb = Gtk.ToolButton(Gtk.STOCK_QUIT)
        quittb.connect("clicked", self.quit)
        toolbar.insert(newNoteTb, 0)
        toolbar.insert(sep, 1)
        toolbar.insert(quittb, 2)
        
        self.view = WebKit.WebView()
        sw = Gtk.ScrolledWindow() 
        sw.add(self.view) 

        win = Gtk.Window()
        vbox = Gtk.VBox()
        vbox.pack_start(toolbar, False, False, 0)
        win.add(vbox)
        vbox.add(sw)

        win.show_all() 
        win.connect("delete-event", self.exit)
        self.view.open(NotesConfig.formUrl( ""))
        
        win.maximize()
        self.window = win
        self.view.connect("context-menu", self.displayContextMenu)
        self.view.connect("script-alert", self.alert)
        self.view.connect("navigation-policy-decision-requested", self.navigate)



NotesConfig.database.init("/tmp/notes.db")

app = NotesApp()

        
Gtk.main()


