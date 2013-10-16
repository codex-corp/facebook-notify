#Facebook status notifier for GNOME and Cinnamon
#Copyright (C) 2013 was Developed by Hany alsamman <hany@codexc.com>
#Copyright (C) 2009 John Stowers <john.stowers@gmail.com>
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

from libfacebooknotify import DEFAULT_BROWSER

# import the backend module
EW_BACKEND = None
try:
    if DEFAULT_BROWSER != "gtkmozembed":
        raise Exception
    import gtkmozembed
    EW_BACKEND = "gtkmozembed"
except:
    if DEFAULT_BROWSER != "webkit":
        raise Exception
    import webkit
    EW_BACKEND = "webkit"

class BrowserEmbed:
    def __init__(self):
        self._embed_widget = None
        print "browser using: %s" % EW_BACKEND
        if EW_BACKEND == "webkit":
            self._embed_widget = webkit.WebView()
            #disable flash to stop segfault on destroy
            self._embed_widget.get_settings().props.enable_plugins = False
        elif EW_BACKEND == "gtkmozembed":
            self._embed_widget = gtkmozembed.MozEmbed()
        else:
            raise Exception('No valid backend available')

    def open_url(self, url):
        if EW_BACKEND == "webkit":
            return self._embed_widget.open(url)
        elif EW_BACKEND == "gtkmozembed":
            return self._embed_widget.load_url(url)
        else:
            raise Exception('No valid backend available')

    def get_widget(self):
        return self._embed_widget