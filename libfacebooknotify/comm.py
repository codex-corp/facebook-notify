#Facebook status notifier for GNOME and Cinnamon
#Copyright (C) 2013 was Developed by Hany alsamman <hany@codexc.com>
#Copyright (C) 2009 John Stowers <john.stowers@gmail.com>
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import time
import threading
import tempfile
import urllib2
import traceback

import libfacebooknotify.facebook as facebook


class FacebookCommunicationManager(threading.Thread):
    FB_AID = 44911717818
    FB_API_KEY = "cf61e1494a431f7db3c8372cc4a17bdf"
    FB_SECRET = "144b35ddb210ca2543051d4a3d03313b"

    def __init__(self):
        threading.Thread.__init__(self)
        #func : (cb, *args, **kwargs)
        self._pending = []
        self._pending_photos = []
        self._photo_cache = {}
        self._stopped = False
        self._event = threading.Event()
        self._fb = facebook.Facebook(self.FB_API_KEY, self.FB_SECRET)
        self._tmpdir = tempfile.mkdtemp(prefix="facebook", suffix="cache")
        #self._fb.auth.createToken()
        #self._fb.login(popup=True)
        #self._fb.auth.getSession()

        print
        "facebook parsing using: %s (%s)" % (facebook.RESPONSE_FORMAT, getattr(facebook, "JSON_MODULE", "N/A"))

    def stop(self):
        self._stopped = True
        #self._event.set()

    def call_facebook_function(self, cb, func, *args, **kwargs):
        self._pending.insert(0, (cb, func, args, kwargs))
        #self._event.set()

    def download_photo(self, cb, url, *args, **kwargs):
        if url in self._photo_cache:
            cb(self._photo_cache[url], *args, **kwargs)
        else:
            self._pending_photos.insert(0, (cb, url, args, kwargs))
            #self._event.set()

    def get_login_url(self):
        return self._fb.get_login_url()

    def get_permissions_url(self):
        return self._fb.get_ext_perm_url("offline_access")

    def got_permissions(self):
        print
        self._fb.ext_perms
        return self._fb.ext_perms

    def run(self):
        while not self._stopped:
            while True:
                #do any pending facebook calls
                try:
                    cb, funcname, args, kwargs = self._pending.pop()
                    print
                    "Calling %s... " % funcname,
                    func = self._fb
                    for f in funcname.split("."):
                        func = getattr(func, f)
                    try:
                        res = func(*args)
                        print
                        "finished"
                    except facebook.FacebookError, e:
                        print
                        "facebook error: %s" % e.msg
                        res = {}
                    except urllib2.URLError, e:
                        print
                        "comm error: %s" % str(e.reason)
                        res = {}
                    try:
                        cb(res)
                    except Exception:
                        traceback.print_exc()
                except IndexError:
                    break

                #do any pending image downloads
                try:
                    cb, url, args, kwargs = self._pending_photos.pop()
                    try:
                        print
                        "Downloading %s... " % url
                        inf = urllib2.urlopen(url)
                        fd, pic = tempfile.mkstemp(dir=self._tmpdir, suffix=".jpg")

                        os.write(fd, inf.read())
                        os.close(fd)
                        inf.close()

                        print
                        "finished"
                        self._photo_cache[url] = pic
                    except urllib2.URLError, e:
                        print
                        "error: %s" % str(e.reason)
                        pic = ""
                    try:
                        cb(pic, *args, **kwargs)
                    except Exception:
                        traceback.print_exc()
                except IndexError:
                    break

                #minimum of 1 second between subsequent facebook calls
                time.sleep(1)

            time.sleep(0.1)
            #self._event.wait()
            #self._event.clear()