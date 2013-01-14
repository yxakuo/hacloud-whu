from Token import Token
import httplib
import json
import urllib
from urlparse import urlparse
from error import Error

class F_Volume(Error):
    
    def __init__(self):
        self.token = Token()
        self.apitoken = self.token.get_apitoken()
        self.apiurl = self.token.get_apiurl()
        self.apiurlt = urlparse(self.apiurl)
    
    def List_VolumesAttachedToAnInstance(self,instance_id):
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('GET','%s/servers/%s/os-volume_attachments'%(self.apiurlt[2],instance_id),params,headers)
        reponse = conn.getresponse()
        volume_details = reponse.read()
        volume_details = json.loads(volume_details)
        conn.close()
        return volume_details
    
    def Attach_VolumeToInstance(self,instance_id,volume_id,volume_device):
        params = {
                  'volumeAttachment': {
                                       'volumeId': volume_id,
                                       'device': volume_device
                                       }
                  }
        params=json.dumps(params)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('POST','%s/servers/%s/os-volume_attachments'%(self.apiurlt[2],instance_id),params,headers)
        reponse = conn.getresponse()
        attachment = reponse.read()
        attachment = json.loads(attachment)
        conn.close()
        return attachment
    
    def List_AllVolumetypes(self):
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('GET','%s/os-volume-types' %self.apiurlt[2][:2]+'1.1'+self.apiurlt[2][3:],params,headers)
        reponse = conn.getresponse()
        volume_type = reponse.read()
        volume_type = json.loads(volume_type)
        conn.close()
        return volume_type
    
    def Create_Volume(self,volume_metadata):
        params = json.dumps(volume_metadata)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('POST','%s/volumes' %self.apiurlt[2][:2]+'1.1'+self.apiurlt[2][3:],params,headers)
        reponse = conn.getresponse()
        volume_details = reponse.read()
        volume_details= json.loads(volume_details)
        conn.close()
        return volume_details

###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################

    """the functions under this line is not right yet""" 
    

    def backup_volume(self,data):
        true = True
        params = {
                  "snapshot": {
                               "display_name": "snap-001",
                               "display_description": "Daily backup",
                               "volume_id": "21a0e3ef-a78a-46b8-b552-ec9946df6d8a",
                               "force": true
                               }
                  }
        params = json.dumps(params)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        tenant_id = '70c6e018c0d9416ba85459884adeccd2'
        test= '/v1.1/70c6e018c0d9416ba85459884adeccd2'
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('POST','%s/os-snapshots'%test,params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        print result
        result = json.loads(result)
        conn.close()
        return result

    def list_vbackup(self):
        true = True
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        tenant_id = '70c6e018c0d9416ba85459884adeccd2'
        test= '/v1.1/70c6e018c0d9416ba85459884adeccd2'
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('GET','%s/os-snapshots'%test,params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        print result
        result = json.loads(result)
        conn.close()
        return result

    def delete_vbackup(self):
        true = True
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        tenant_id = '70c6e018c0d9416ba85459884adeccd2'
        test= '/v1.1/70c6e018c0d9416ba85459884adeccd2'
        snapshot_id = '1ace60c5-5799-463b-9f64-6202372195c6'
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('DELETE','%s/os-snapshots/%s'%(test,snapshot_id),params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        print result
        result = json.loads(result)
        conn.close()
        return result

    
    
