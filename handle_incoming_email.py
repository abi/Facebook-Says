import logging
import wsgiref.handlers
import os
import base64
import urllib
import hashlib

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import urlfetch

from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import mail_handlers

class MailHandler(mail_handlers.InboundMailHandler):
  def receive(self, message):
      
        # More information on how notify.io notification sending works - 
        # http://groups.google.com/group/notify-io/web/developers
        
        # Get the email, hash it send with notify.io
        m = hashlib.md5()
        m.update(message.to.split("<")[1].split("@")[0] + "@gmail.com")
        url = "http://api.notify.io/v1/notify/" + m.hexdigest()
        
        # ADD YOUR OWN API KEY HERE (see link above for more info on that)
        authString = 'Basic ' + base64.b64encode('[ADD YOUR API KEY HERE]:string')
        
        # TODO: This is a bad way of extracting URLs
        # http://www.facebook.com/confirmcontact.php?c=3D2023864552 =20
        # Change =3D to =, = to nothing
        
        plaintext = message.bodies(content_type='text/plain')
        msg = ""
        for text in plaintext:
          msg = msg + text[0]
        
        msgtext = str(message.body)
          
        payload= {'text' : message.subject, 
                  'title' : "Facebook Notification", 
                  'icon' : "http://facebook.com/favicon.ico"}
        
        if message.subject == "Facebook Contact Email Confirmation":
          tempurl = msgtext[msgtext.find("http://"):]
          tempurl = tempurl[:tempurl.find(" ")].replace("3D", "").replace("=\nr", "r").split("=20")[0]
          payload = {'text' : tempurl, 'title' : "Confirm Facebook Email at this URL", 'icon' : "http://facebook.com/favicon.ico"}
        
        payload= urllib.urlencode(payload)
        data = urlfetch.fetch(url, payload=payload, method=urlfetch.POST, headers={'Authorization' : authString})
        

application = webapp.WSGIApplication([('/.*', MailHandler)],
                                     debug=True)
def main():
  logging.getLogger().setLevel(logging.DEBUG)
  run_wsgi_app(application)
  
if __name__ == "__main__":
  main()