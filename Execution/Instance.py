from Token import Token
import httplib
import json
import urllib
from urlparse import urlparse
from Image import Image
from Flavor import Flavor
from error import Error

class F_Instance(Token):

    Instance_Info = {}
    
    def __init__(self):
        Token.__init__(self)
    
    def Get_AllInstanceDetails(self):
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
            
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request("GET", "%s/servers" % self.apiurlt[2], params, headers)
        request = conn.getresponse()
        instance_details = request.read()
        instance_details = json.loads(instance_details)
        conn.close()
        return instance_details
        
    def Get_SpecificInstanceDetails(self,instance_id):
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request("GET", "%s/servers/%s" % (self.apiurlt[2],instance_id), params, headers)
        request = conn.getresponse()
        instance_details = request.read()
        instance_details = json.loads(instance_details)
        conn.close()
        return instance_details
    
    def Get_AllInstanceSerialNumber(self):
        instance_info = self.Get_AllInstanceDetails()
        instance_id = []
        for i in range(len(instance_info['servers'])):
            instance_id.append(instance_info['servers'][i]['id'])

        for i in range(len(instance_info['servers'])):
            instance_info = self.Get_SpecificInstanceDetails(instance_id[i])
            self.Instance_Info[instance_id[i]] = {instance_info['server']['name'] : instance_info['server']['OS-EXT-SRV-ATTR:instance_name']}

    def Get_SpecificInstanceName(self,instance_id):
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request("GET", "%s/servers/%s" % (self.apiurlt[2],instance_id), params, headers)
        request = conn.getresponse()
        instance_details = request.read()
        instance_details = json.loads(instance_details)
        conn.close()
        return instance_details['server']['name']
    
    def Get_InstanceImageHref(self,instance_id):
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request("GET", "%s/servers/%s" % (self.apiurlt[2],instance_id), params, headers)
        request = conn.getresponse()
        instance_details = request.read()
        instance_details = json.loads(instance_details)
        conn.close()
        return instance_details['server']['image']['links']['href']
    
    def Get_InstanceImageId(self,instance_id):
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request("GET", "%s/servers/%s" % (self.apiurlt[2],instance_id), params, headers)
        request = conn.getresponse()
        instance_details = request.read()
        instance_details = json.loads(instance_details)
        conn.close()
        return instance_details['server']['image']['id']
    
    def Get_InstanceFlavorHref(self,instance_id):
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request("GET", "%s/servers/%s" % (self.apiurlt[2],instance_id), params, headers)
        request = conn.getresponse()
        instance_details = request.read()
        instance_details = json.loads(instance_details)
        conn.close()
        return instance_details['server']['flavor']['links']['href']
    
    def Get_InstanceFlavorId(self,instance_id):
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request("GET", "%s/servers/%s" % (self.apiurlt[2],instance_id), params, headers)
        request = conn.getresponse()
        instance_details = request.read()
        instance_details = json.loads(instance_details)
        conn.close()
        return instance_details['server']['flavor']['id']
    
    def Create_Instance(self,instance_name,image_id,flavor_id):
        
        image = Image()
        image_href = image.get_anactiveimagehref()
        flavor = Flavor()
        flavor_href = flavor.get_specificflavorhref(flavor_id)
        
        instance = { "server": { "name": instance_name, "imageRef": image_href, "flavorRef": flavor_href} }
        params = json.dumps(instance)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request("POST", "%s/servers" % self.apiurlt[2], params, headers)
        request = conn.getresponse()
        instance_metadata = request.read()
        instance_metadata = json.loads(instance_metadata)
        conn.close()
        return instance_metadata

    def Delete_Instance(self,instance_id):
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }

        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('DEELTE','%s/servers/%s'%(self.apiurlt[2],instance_id),params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        print result
        result = json.loads(result)
        conn.close()
        return result
    
    def Reboot_Instance(self,instance_id):
        
        params = {"reboot" : {"type" : "HARD"}}
        params = json.dumps(params)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }

        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('POST','%s/servers/%s/action'%(self.apiurlt[2],instance_id),params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        result = json.loads(result)
        conn.close()
        return result
############################################################################################################################
############################################################################################################################    
############################################################################################################################
############################################################################################################################   
############################################################################################################################
############################################################################################################################       
    
    
    def Create_Instanceimage(self,instance_id,image_name):
        instance = '7bf07850-a47c-4cfd-8cd3-f5a0ea251faa'
        #params = {"pause" : {"id":"7bf07850-a47c-4cfd-8cd3-f5a0ea251faa"}}
        params = {
                  "createImage" : {
                                   "name" : "new-image",
                                   "metadata": {
                                                "ImageType": "Gold",
                                                "ImageVersion": "2.0"
                                                }
                                   }
                  }
        params = json.dumps(params)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }

        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('POST','%s/servers/%s/action'%(self.apiurlt[2],instance),params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        result = json.loads(result)
        conn.close()
        return result
    
    def Migrate_Instance(self,instance_id):
        instance = '7bf07850-a47c-4cfd-8cd3-f5a0ea251faa'
        #params = {"pause" : {"id":"7bf07850-a47c-4cfd-8cd3-f5a0ea251faa"}}
        params = {
                  "os-migrateLive": {
                                     "host": "0443e9a1254044d8b99f35eace132080",
                                     "block_migration": 'false',
                                     "disk_over_commit": 'false'
                                    }
                  }
        params = json.dumps(params)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }

        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('POST','%s/servers/%s/action'%(self.apiurlt[2],instance),params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        result = json.loads(result)
        conn.close()
        return result
    
    def Rebuild_Instance(self,instance_id,image_id):
        instance = '7bf07850-a47c-4cfd-8cd3-f5a0ea251faa'
        image_id = '0f7064ba-3292-4da1-a471-bfbac28aafd0'
        #params = {"pause" : {"id":"7bf07850-a47c-4cfd-8cd3-f5a0ea251faa"}}
        params = {
                  "rebuild": {
                              "imageRef": "cedef40a-ed67-4d10-800e-17455edce175",
                              "OS-DCF:diskConfig": "AUTO"
                              }
                  }
        params = json.dumps(params)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }

        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('POST','%s/servers/%s/action'%(self.apiurlt[2],instance),params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        result = json.loads(result)
        conn.close()
        return result
    
    def Resize_Instance(self,instance_id,flavor_id):
        instance = '7bf07850-a47c-4cfd-8cd3-f5a0ea251faa'
        image_id = '0f7064ba-3292-4da1-a471-bfbac28aafd0'
        #params = {"pause" : {"id":"7bf07850-a47c-4cfd-8cd3-f5a0ea251faa"}}
        params = {
                  "resize": {
                             "flavorRef": "1",
                             "OS-DCF:diskConfig": "AUTO"
                             }
                  }
        params = json.dumps(params)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }

        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('POST','%s/servers/%s/action'%(self.apiurlt[2],instance),params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        result = json.loads(result)
        conn.close()
        return result

    def Set_Instance(self):
        instance = '7bf07850-a47c-4cfd-8cd3-f5a0ea251faa'
        image_id = '0f7064ba-3292-4da1-a471-bfbac28aafd0'
        #params = {"pause" : {"id":"7bf07850-a47c-4cfd-8cd3-f5a0ea251faa"}}
        params = {
                  "server" :
                            {
                             "name" : "new-server-test",
                             "accessIPv4":"192.168.1.1"
                             }
                  }
        params = json.dumps(params)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }

        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('PUT','%s/servers/%s'%(self.apiurlt[2],instance),params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        result = json.loads(result)
        conn.close()
        return result
 
    def Change_InstanceAdminPassword(self,instance_id,instance_password):
        instance = '7bf07850-a47c-4cfd-8cd3-f5a0ea251faa'
        image_id = '0f7064ba-3292-4da1-a471-bfbac28aafd0'
        #params = {"pause" : {"id":"7bf07850-a47c-4cfd-8cd3-f5a0ea251faa"}}
        params = {
                  "changePassword" : {
                                      "adminPass" : "foo"
                                      }
                  }
        params = json.dumps(params)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }

        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('POST','%s/servers/%s/action'%(self.apiurlt[2],instance),params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        result = json.loads(result)
        conn.close()
        return result
    
    def Backup_Instance(self,instance_id):
        instance = '7bf07850-a47c-4cfd-8cd3-f5a0ea251faa'
        image_id = '0f7064ba-3292-4da1-a471-bfbac28aafd0'
        #params = {"pause" : {"id":"7bf07850-a47c-4cfd-8cd3-f5a0ea251faa"}}
        params = {
                  "createBackup": {
                                   "name": "Backup 1",
                                   "backup_type": "daily",
                                   "rotation": 1
                                   }
                  }
        params = json.dumps(params)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }

        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('POST','%s/servers/%s/action'%(self.apiurlt[2],instance),params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        result = json.loads(result)
        conn.close()
        return result

    def Freeze_Instance(self,instance_id):
        instance = '7bf07850-a47c-4cfd-8cd3-f5a0ea251faa'
        image_id = '0f7064ba-3292-4da1-a471-bfbac28aafd0'
        #params = {"pause" : {"id":"7bf07850-a47c-4cfd-8cd3-f5a0ea251faa"}}
        params = {"lock":"AUTO"}
        params = json.dumps(params)
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        conn = httplib.HTTPConnection(self.apiurlt[1])
        conn.request('POST','%s/servers/%s/action'%(self.apiurlt[2],instance),params,headers)
        reponse = conn.getresponse()
        result = reponse.read()
        result = json.loads(result)
        conn.close()
        return result