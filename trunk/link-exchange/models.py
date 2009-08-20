from django.db import models

from datetime import datetime, timedelta
from urllib2 import urlopen, URLError
from exceptions import ValueError
from link_exchange.scrapemark import scrape
import unicodedata as ud

class Campaign(models.Model):
    """
    A Campaign represents a set of Links exchanged between two sites.
    """
    title = models.CharField(max_length=400, unique=True) 
    main_url = models.URLField(max_length=200) 
    
    contact_name = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    
    css_class = models.CharField(max_length=200, blank=True, help_text='optionally apply css class(es) to this link')
    more_attribute = models.CharField(max_length=400, blank=True, help_text='optionally apply attributes to this link. eg: javascript tracker')
    target = models.CharField(max_length=50, blank=True, help_text='optionally apply a target to this link. ie: _blank')
    
    update_date = models.DateField(auto_now = True)
    pub_date  = models.DateField(auto_now_add = True)
    
    def __unicode__(self):
        return self.title


class Link(models.Model):
    """
    This is the Link model. 
    It contains every information to publish the link and to check the expected backlink.
    """
    name = models.CharField(max_length=400, unique=True, help_text='Unique name for this link. Will be used in the tag {% link "name" %}') 
    campaign = models.ForeignKey('Campaign')
    
    anchor = models.CharField(max_length=400, blank=True, help_text='anchor for this link')
    external_url = models.URLField(max_length=400, blank=True, help_text='destination url for this link')
    text = models.TextField(default="%s", help_text='full html to be inserted including a %s as the link placeholder')   
    active = models.BooleanField(default=True, help_text='Publish this link')
    
    reverse_url  = models.URLField(max_length=400, blank=True, help_text='url of the page containing the backlink')
    reverse_anchor = models.CharField(max_length=400, blank=True, help_text='expected anchor in the backlink')    
    reverse_dest_url = models.URLField(max_length=400, blank=True, help_text='expected url in the backlink')
   
    checked_ok = models.BooleanField(default=False)
    last_checked = models.DateField(auto_now_add = True)
    checked_message = models.CharField(max_length=1024, blank=True)
    
    update_date = models.DateField(auto_now = True)
    pub_date  = models.DateField(auto_now_add = True)
    
    def __unicode__(self):
        return self.name

    def check_backlink(self):
        self.last_checked = datetime.now()
        try:
            url_to_load = self.reverse_url.rsplit('#')[0] # Remove URL fragment identifiers
            response = urlopen(url_to_load) 
            self.checked_message = ' '.join([str(response.code), response.msg])
            links = scrape(""" {* <a href='{{ [links].url }}'>{{ [links].anchor }}</a> *} """,
                url = url_to_load)            
            found = False
            for alink in links['links']:
                if self.reverse_dest_url in alink['url']:
                    found = True
                    if ud.normalize('NFC',self.reverse_anchor) in ud.normalize('NFC',alink['anchor']) :
                        self.checked_ok = True
                    else:
                        self.checked_message = 'Bad anchor in Backlink. "%s" found instead of "%s"' \
                                               % (alink['anchor'],self.reverse_anchor)
                        self.checked_ok = False
                    break        
            if not found :
                self.checked_message = 'Backlink not Found'
                self.checked_ok = False
        except URLError, e:
            if hasattr(e, 'reason'):
                self.checked_message = 'Unreachable: '+str(e.reason)
            elif hasattr(e, 'code') and e.code!=301:
                self.checked_message = 'Error: '+str(e.code)
            else:
                self.checked_message = 'Redirect. Check manually: '+str(e.code)
            self.checked_ok = False
        except ValueError, e:
            print str(e)
            self.checked_message = 'Invalid backlink URL '+str(self.reverse_url)
            self.checked_ok = False
        self.save()
        
