'''
Created on Nov 2, 2016

@author: eli
'''
import urllib2
import re
import xml.etree.ElementTree as xt

SERVICE_NAMESPACE ='urn:schemas-upnp-org:service'
SERVICE_VER = '1'

A_ARG_TYPE_InstanceID = 1
DEFAULT_PLAY_SPEED = 1

UDNP_SERVICE ='urn:schemas-upnp-org:service'
SUB_MSG_TEMPLATE = ['SUBSCRIBE {} HTTP/1.1',  
'HOST: {}',
'CALLBACK: {}',
'NT: upnp:Event',
]



SOAP_HEADER_TEMPLATE = {
    "Content-Type"   : "text/xml; charset=\"utf-8\"",
    "Content-Length" : "{}",
    "Connection"     : "close",
    "SOAPACTION"     : "{}"
} 
SOAP_BODY_TEMPLATE ='<?xml version="1.0"?>\
                    <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\
                    <s:Body> <u:actionName xmlns:u="urn:schemas-upnp-org:service:serviceType:v">\
                    <argumentName>{}</argumentName> \
                    </u:actionName>\
                    </s:Body>\
                    </s:Envelope>'  

SOAPACTION_TEMPLATE = "urn:schemas-upnp-org:{service}:{serviceType}:v#{actionName}"
SUB_MSG_TEMPLATE = ['SUBSCRIBE {} HTTP/1.1',  
'HOST: {}',
'CALLBACK: {}',
'NT: upnp:Event',
]
              
NAME_SPACE = {'service_type': 'urn:schemas-upnp-org:service', 'service_id':'urn:upnp-org'}
                    
def extrac_host_info(url):
    pattern = re.compile('http\:\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d+)?')
    
    m = re.match(pattern, url)
    if m:
        host_ip_port = m.group(0)
    else:
        host_ip_port = ''
    return host_ip_port


class upnp_action:
    '''
    action_name: Play
    argument: name = InstanceID,  direction: in, relatedStateVariable: A_ARG_TYPE_InstanceID;
    name: Speed, direction: in, relatedStateVariable: TransportPlaySpeed
    
    methods: execute()
    '''
    
    def __init__(self, action_name, control_url):
        self.name = action_name
        self.argument_list  = []
        self.control_url = control_url
        
    
    
    def execute(self):
        urllib2.Request(self.control_url,data=None, headers ={})
        urllib2.Request
        
class upnp_service:
    ''' service_type: 'AVTransport:1', serviceId: AVTransport, scpdurl:'/AVTransport1.xml'
    control_url = /upnp/control/AVTransport1
    eventSubURL = /upnp/event/AVTransport1
    '''
    def __init__(self, service_type, id):
        self.id = id
        self.service_type = service_type
        self.control_url = ''
        self.event_sub_url =''
        self.scpdurl = ''
        self.action_list =[]
    
    def set_type(self, type):
        self.service_type = type
    
    def set_control_url(self,url):
        self.control_url = url
    
    def set_event_sub_url(self, url):
        self.event_sub_url = url
    
    def set_scpdurl(self, url):
        self.scpdurl = url
    
    def get_service_actions(self):
        '''
        retrieve available list of actions by querying scpdurl
        return 
        stateTable and actionLists
        stableTable: name, dataType, allowedValue
        action: name, argumentList, 
        argument: name, direciton, relatedStableVariable
        
        '''
        ns = "{schemas-upnp-org:service-1-0}:{}"
        fh = urllib2.urlopen(self.scpdurl)
        resp = fh.read()
        root = xt.fromstring(resp)
        for item in root.FindAll(ns.format('actionList/action')):
            action_name = item.FindAll(ns.format('actionList/action/name'))
            new_action = upnp_action(action_name.text, self.control_url)
            self.action_list.append(new_action)
    
    def __repr__(self):
        return 'id:{} type:{} \n scpdurl:{}, control_url:{}'.format(self.id, self.service_type, self.scpdurl, self.control_url )
    
    def AV_capapable(self):
        return (self.service_type == 'AVTransport:1')
        
        
        
        
    def subscribe_to_events(self, receiving_url):
        fh = urllib2.urlopen(self.event_sub_url)
        '''
        message = 
        header = 
        resp = fh.post()
        resp contains names and current values of all evented variables
        '''
    #def renew_event_subscription(self):
        
        
        
    def invoke_PLAY(self):
        argument = {}
        play_action = self.action_list['Play']
        argument['InstanceID'] = 0
        argument['Speed'] = DEFAULT_PLAY_SPEED
        play_content = "http://abc"
        content_len = len(play_content)
        
        header_soapaction = SOAPACTION_TEMPLATE.format(self.service,self.seviceType,SERVICE_VER, 'Play')
        headers = SOAP_HEADER_TEMPLATE.format(content_len, header_soapaction )
        resp = urllib2.Request(self.control_url, play_content, headers=header_soapaction)
        ret = resp.read()   
         
    def invoke_SetAVTransportURI(self):
        header_soapaction = SOAPACTION_TEMPLATE.format(self.service,self.seviceType,SERVICE_VER, 'SetAVTransportURI')
        play_content = "http:: point to the media file"
        content_len  = len(play_content)
        headers = SOAP_HEADER_TEMPLATE.format(content_len, header_soapaction )
        resp = urllib2.Request(self.control_url, play_content, headers)
        ret = resp.read()
        '''<CurrentURI> url to the media </CurrentURI> '''
        headers = SOAP_HEADER_TEMPLATE.format(content_len, header_soapaction )
        resp = urllib2.Request(self.control_url, play_content, headers)
        ret = resp.read()



def print_element(item):
    #service_value = item.text.encode('utf8').rsplit(':',2)[1]
    print '{} = {}'.format(item.tag, item.text)
    
def xml_to_info(xml, root_url):
    #with open('xiaomi.xml','rt') as fh:
    #    xml = fh.read()
    
    
    service_list = []
    xml = re.sub(' xmlns=\"[^\"]+\"','', xml, 1)
    info = xt.fromstring(xml)    
    '''
    for item in info.iter():
        print '{} = {}'.format(item.tag,  item.text.encode('utf8')) 
    '''
    friendly_name = info.find('./device/friendlyName').text 
    print friendly_name
  
    for s in info.findall('./device/serviceList/service'):  
        s_type = s.find('serviceType').text
        s_type = re.sub(NAME_SPACE['service_type'], '', s_type)
        
        service_id = s.find('serviceId').text
        service_id = re.sub(NAME_SPACE['service_id'], '',s_type )

        service_node = upnp_service(s_type, service_id)
        host_ip_port = extrac_host_info(root_url)
        scpd_url = host_ip_port + s.find('SCPDURL').text
        
        control_url = host_ip_port + s.find('controlURL').text
        service_node.set_scpdurl(scpd_url)
        service_node.set_control_url(control_url)
        
        print(service_node)
        
        service_node.get_service_actions()
        service_list.append(service_node)        

        
    


#if __name__ == '__main__':
#    xml_to_info()