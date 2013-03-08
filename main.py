#!/usr/bin/env python

import cherrypy
import os
import threading
import gi
from gi.repository import WebKit 
from gi.repository import Gtk 
from gi.repository import GLib, GObject
from model import NotesConfig

from mako.template import Template
from mako.lookup import TemplateLookup

lookup = TemplateLookup(directories=['web'])
GObject.threads_init()


class NotesWeb:
    def index(self):
        tmpl = lookup.get_template("index.html")
        return tmpl.render(salutation="Hello", target="World")
    
    index.exposed = True


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
        global exitLoop
        exitLoop = True
        GLib.idle_add(idleHookFunction, app)    
            
    def save(self, webview):
        pass
    
    def displayContextMenu(self, view, menu, keyboard, data):
        print "Context menu", menu.get_children()
        for item in menu.get_children():
            print "Item", item.get_label()
            x = item.get_label()
            y = "_Back"
            if (y == item.get_label()):
                menu.remove(item)
        
        
    def __init__(self):
       
        toolbar = Gtk.Toolbar()
        # toolbar.set_style(Gtk.ToobarStyle.GTTOOLBAR_ICONS)
        savetb = Gtk.ToolButton(Gtk.STOCK_SAVE)
        savetb.connect("clicked", self.save)
        sep = Gtk.SeparatorToolItem()
        quittb = Gtk.ToolButton(Gtk.STOCK_QUIT)
        toolbar.insert(savetb, 0)
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
        self.view.open("http://localhost:8080/")
        
        win.maximize()
        self.window = win
        self.view.connect("context-menu", self.displayContextMenu)




NotesConfig.database.init("/tmp/notes.db")

app = NotesApp()

        
Gtk.main()


