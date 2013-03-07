#!/usr/bin/env python

import cherrypy
import os
import gi
from gi.repository import WebKit 
from gi.repository import Gtk 
from gi.repository import GLib


class NotesWeb:
    def index(self):
        return "Hello world"
    
    index.exposed = True

    
exitLoop = False
    
class NotesApp:
    def exit(self, arg, a1):
        global exitLoop
        exitLoop = True
        self.window.hide()
        
    def save(self, webview):
        pass
    
    def __init__(self):
       
        toolbar = Gtk.Toolbar()
        #toolbar.set_style(Gtk.ToobarStyle.GTTOOLBAR_ICONS)
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
        
        win.maximize()
        self.window = win


idle_index = 0

def idleHookFunction(app):
    global idle_index
    if (idle_index != 0):
        cherrypy.tree.mount(NotesWeb(), "/")
        cherrypy.engine.start()
        app.view.open("http://localhost:8080/")
        idle_index = 0

    if (exitLoop):
        cherrypy.engine.stop()
        Gtk.main_quit()
    
    return True

app = NotesApp()

idle_index=GLib.idle_add(idleHookFunction, app)

        
Gtk.main()


