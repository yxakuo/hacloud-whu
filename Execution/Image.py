from Token import Token
import httplib
import json
import urllib
from urlparse import urlparse

class Image(Token):
    def __init__(self):
        Token.__init__(self)
        
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        self.conn = httplib.HTTPConnection(self.apiurlt[1])
        self.conn.request("GET", "%s/images/detail?" % self.apiurlt[2], params, headers)
    
        self.response = self.conn.getresponse()
        self.image_metadata = self.response.read()
        self.image_metadata = json.loads(self.image_metadata)
        self.conn.close()

    def Get_AllActiveImageId(self):
        m = range(len(self.image_metadata['images']))
        image_id=[]
        n = 0
        for i in m:
            if self.image_metadata['images'][i]['status']=='ACTIVE':
                image_id[n]=self.image_metadata['images'][i]['id']
                n = n+1
        return image_id
    
    def Get_AnActiveImageId(self):
        m = range(len(self.image_metadata['images']))
        image_id=''
        for i in m:
            if self.image_metadata['images'][i]['status']=='ACTIVE':
                image_id=self.image_metadata['images'][i]['id']
                return image_id
            
    def Get_AnActiveImageHref(self):
        m = range(len(self.image_metadata['images']))
        image_href=''
        for i in m:
            if self.image_metadata['images'][i]['status']=='ACTIVE':
                image_href = self.image_metadata['images'][i]['links'][0]['href']
                return image_href
            
    def Get_SpecificImageHref(self,image_id):
        m = range(len(self.image_metadata['images']))
        image_href = ''
        for i in m:
            if self.image_metadata['images'][i]['id'] == image_id:
                image_href=self.image_metadata['images'][i]['links'][0]['href']
                return image_href
            
    def Get_AllActiveImageHref(self):
        m = range(len(self.image_metadata['images']))
        n=0
        image_href={}
        for i in m:
            if self.image_metadata['images'][i]['status']=='ACTIVE':
                image_href[n]=self.image_metadata['images'][i]['links'][0]['href']
                n=n+1
        return image_href
    
    def Get_AllActiveImageData(self):
        m = range(len(self.image_metadata['images']))
        n=0
        image_data={}
        for i in m:
            if self.image_metadata['images'][i]['status']=='ACTIVE':
                image_data[n]=self.image_metadata['images'][i]
                n=n+1
        return image_data
    