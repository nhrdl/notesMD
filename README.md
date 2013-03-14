notesMD
=======

**Dedicated to all those open source warriers who have build best software in the world**

This is a tool that allows you to manage your notes. Original inspiration for this tool comes from [Basket Note Pads][1]. However it looks like basket note pads is no longer maintained. And it lacked some functionality that I wanted.

I wanted to 

 1. Contribute to open source in my small way
 2. Learn python
 3. Learn webkit API
 4. Lean GTK

This is my first python project. Any python experince before this was basic few liner scripts that were written using help from google. HTML UI is not one of my strongest skills and the tool definitely shows it. Please bare with my UI until I manage to convince a friend to polish up the HTML. The tool is basically glued up scripts from various sources. Please look at credits file for more details.

It was much easier to start a new project that manages the notes the way I want. It gave me opportunity to learn python, understand webkit GTK API.

This tool starts a webserver on port 8080 and points webkit view to it.

Basic usage is simple. You just start main.py. It will create the required database for you in your home directory/.config/notesMD if it does not exist. You can add/edit notes on the screen.  Notes can be categorized in baskets. You can add as many baskes as you want.

Notes syntax is a [markdown][2]. This will allow you nicely format your notes. The tools comes with a editor that shows you a preview of how your notes are going to look.

You can also drag and drop almost anything that can dropped. The tool will create a new note in currently selected basket. If you drop a file or link, the tool can serve as a boomark place.

Even though webkit is perfectly capable of handling many of the link destination that your notes are showing, the tool ensures that all links are opened using system's tools set for the link type. In short, behavior should be similar to when you doubleclick the file.

  [1]: http://basket.kde.org/
  [2]:https://www.google.com/search?&q=markdown+