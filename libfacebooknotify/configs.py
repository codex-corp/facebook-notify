from collections import OrderedDict
import gtk
import os
import ConfigParser


class ConfigsWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)

        self.config = ConfigParser.SafeConfigParser(dict_type=OrderedDict)
        self.config.optionxform = str ## dont save as lowercase !!!!

        self.set_default_size(200, 200)

        self.config.add_section('MY_CONFIG')

        self.config.set('MY_CONFIG', 'SECONDS_UPDATE_FREQ', '60')
        self.config.set('MY_CONFIG', 'HISTORY_MAX', '5')
        self.config.set('MY_CONFIG', 'LOGIN_HIGHT', '370')
        self.config.set('MY_CONFIG', 'LOGIN_WIDTH', '825')

        self.liststore = gtk.ListStore(str, str, str)

        self.liststore.append(["Check Notiftications Every", "60", "SECONDS_UPDATE_FREQ"])
        self.liststore.append(["Notiftications Menu History", "5", "HISTORY_MAX"])
        self.liststore.append(["Login window Width", "825", "LOGIN_WIDTH"])
        self.liststore.append(["Login window Height", "370", "LOGIN_HIGHT"])

        treeview = gtk.TreeView(model=self.liststore)

        renderer_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn("Text", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_editabletext = gtk.CellRendererText()
        renderer_editabletext.set_property("editable", True)

        column_editabletext = gtk.TreeViewColumn("Editable Text",
                                                 renderer_editabletext, text=1)
        treeview.append_column(column_editabletext)

        renderer_editabletext.connect("edited", self.text_edited)

        self.add(treeview)


    def text_edited(self, widget, path, text):
        self.liststore[path][1] = text
        config_title = self.liststore[path][0]
        config_value = self.liststore[path][1]
        config_key = self.liststore[path][2]

        self.config.set('MY_CONFIG', config_key, config_value)
        self.lib_path = os.path.join(os.path.dirname(__file__)) ## get libfacebooknotify path

        # Writing our configuration file to 'example.cfg'
        with open(self.lib_path + '/config.cfg', 'w') as configfile:
            self.config.write(configfile)

