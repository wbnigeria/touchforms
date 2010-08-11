from __future__ import absolute_import

import datetime
from django.conf import settings
from couchdbkit.ext.django.schema import *
import bhoma.apps.xforms.const as const
from bhoma.utils.parsing import string_to_datetime
import copy
from couchdbkit.schema.properties_proxy import SchemaListProperty
from bhoma.utils.logging import log_exception

"""
Couch models.  For now, we prefix them starting with C in order to 
differentiate them from their (to be removed) django counterparts.
"""

class MetadataDocument(Document):
    # this is currently unused but may be chosen over the non-doc class
    # if i can get nested schema props working
    """
    Metadata of an xform, from a meta block structured like:
        
        <Meta>
            <clinic_id />
            <TimeStart />
            <TimeEnd />
            <username />
            <user_id />
            <uid />
        </Meta>
    
    Everything is optional.
    """
    clinic_id = StringProperty()
    time_start = DateTimeProperty()
    time_end = DateTimeProperty()
    username = StringProperty()
    user_id = StringProperty()
    uid = StringProperty()
    
    @classmethod
    def from_meta_block(cls, meta_block):
        instance = Metadata()
        try:
            
            if const.TAG_META_CLINIC_ID in meta_block:
                instance.clinic_id = str(meta_block[const.TAG_META_CLINIC_ID])
            if const.TAG_META_TIMESTART in meta_block:
                instance.time_start = string_to_datetime(meta_block[const.TAG_META_TIMESTART])
            if const.TAG_META_TIMEEND in meta_block:
                instance.time_end = string_to_datetime(meta_block[const.TAG_META_TIMEEND])
            if const.TAG_META_USERNAME in meta_block:
                instance.username = meta_block[const.TAG_META_USERNAME]
            if const.TAG_META_USER_ID in meta_block:
                instance.user_id = meta_block[const.TAG_META_USER_ID]
            if const.TAG_META_UID in meta_block:
                instance.uid = meta_block[const.TAG_META_UID]
        except Exception, e:
            log_exception(e)
        return instance
    
    class Meta:
        app_label = 'xforms'
    
class Metadata(object):
    """
    Metadata of an xform, from a meta block structured like:
        
        <Meta>
            <clinic_id />
            <TimeStart />
            <TimeEnd />
            <username />
            <user_id />
            <uid />
        </Meta>
    
    Everything is optional.
    """
    """
    clinic_id = StringProperty()
    time_start = DateTimeProperty()
    time_end = DateTimeProperty()
    username = StringProperty()
    user_id = StringProperty()
    uid = StringProperty()
    """
    clinic_id = None
    time_start = None
    time_end = None
    username = None
    user_id = None
    uid = None

    def __init__(self, meta_block):
        if const.TAG_META_CLINIC_ID in meta_block:
            self.clinic_id = str(meta_block[const.TAG_META_CLINIC_ID])
        if const.TAG_META_TIMESTART in meta_block:
            self.time_start = string_to_datetime(meta_block[const.TAG_META_TIMESTART])
        elif "time_start" in meta_block:
            self.time_start = string_to_datetime(meta_block["time_start"])
        if const.TAG_META_TIMEEND in meta_block:
            self.time_end = string_to_datetime(meta_block[const.TAG_META_TIMEEND])
        elif "time_end" in meta_block:
            self.time_end = string_to_datetime(meta_block["time_end"])
        if const.TAG_META_USERNAME in meta_block:
            self.username = meta_block[const.TAG_META_USERNAME]
        if const.TAG_META_USER_ID in meta_block:
            self.user_id = meta_block[const.TAG_META_USER_ID]
        if const.TAG_META_UID in meta_block:
            self.uid = meta_block[const.TAG_META_UID]
    
    def to_dict(self):
        return dict([(key, getattr(self, key)) for key in \
                     ("clinic_id", "time_start", "time_end",
                      "username", "user_id","uid")])

class CXFormInstance(Document):
    """An XForms instance."""
    
    @property
    def type(self):
        return self.all_properties().get(const.TAG_TYPE, "")
        
    @property
    def version(self):
        return self.all_properties().get(const.TAG_VERSION, "")
        
    @property
    def uiversion(self):
        return self.all_properties().get(const.TAG_UIVERSION, "")
    
    @property
    def namespace(self):
        return self.all_properties().get(const.TAG_NAMESPACE, "")
    
    @property
    def metadata(self):
        if (const.TAG_META) in self.all_properties():
            meta_block = self.all_properties()[const.TAG_META]
            meta = Metadata(meta_block)
            return meta
            
        return None
        
    class Meta:
        app_label = 'xforms'
    
    def __unicode__(self):
        return "%s (%s)" % (self.type, self.namespace)
