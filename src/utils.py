'''
updated on 11/29
Created on Nov 2, 2016

@author: eli
'''
import urllib.urlencode
import re
import xml.etree.ElementTree as xt
import urllib2.HTTPError, urllib2.URLError




A_ARG_TYPE_InstanceID = 1
DEFAULT_PLAY_SPEED = 1
SERVICE_VER = '1'

NAME_SPACE = {'service_type': 'urn:schemas-upnp-org:service', 'service_id':'urn:upnp-org'}
SERVICE_NAMESPACE ='urn:schemas-upnp-org:service-1-0'

SOAP_HEADER_TEMPLATE = {
    'Content-Type' : 'text/xml; charset="utf-8"',
    "Content-Length": "",
    "Connection"     : "close",
    "SOAPACTION"     : ""
} 

SOAP_BODY_TEMPLATE ='<?xml version="1.0"?>\
                    <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\
                    <s:Body> \
                    <u:{actionName} xmlns:u="urn:schemas-upnp-org:service:{serviceType}:{version}">\
                    {arguments} \
                    </u:{actionName}>\
                    </s:Body>\
                    </s:Envelope>' 
 

SOAPACTION_TEMPLATE = "urn:schemas-upnp-org:{service}:{serviceType}:{v}#{actionName}"

SUB_MSG_TEMPLATE = ['SUBSCRIBE {} HTTP/1.1',  
'HOST: {}',
'CALLBACK: {}',
'NT: upnp:Event',
]
              


def extract_host_info(url):
    pattern = re.compile('http\:\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d+)?')
    
    m = re.match(pattern, url)
    if m:
        host_ip_port = m.group(0)
    else:
        host_ip_port = ''
    return host_ip_port

def wrap_in_xml( my_arg):
    xml_template = '<{key}> {value} </{key}>'
    arg_list = []
    for key, value in my_arg.items():
        item = xml_template.format(key=key, value=value)
        arg_list.append(item)
    
    return ' '.join(arg_list)

class upnp_action:
    
    def __init__(self, action_name=''):
        self.name = action_name
        self.argument_list  = []

        
    def __eq__(self, other_action):
        return self.name == other_action.name 
    
    def __repr__(self):
        return '\tActionName: {}'.format(self.name)
    
      
        
class upnp_service:
    ''' service_type: 'AVTransport:1', serviceId: AVTransport, scpdurl:'/AVTransport1.xml'
    control_url = /upnp/control/AVTransport1
    eventSubURL = /upnp/event/AVTransport1
    '''
    def __init__(self, service_type, service_id):
        self.service_id = service_id
        self.service_type = service_type
        self.control_url = ''
        self.event_sub_url =''
        self.scpdurl = ''
        self.action_list = {}
    
    def set_type(self, service_type):
        self.service_type = service_type
    
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
        argument: name, direction, relatedStableVariable
        
        '''
        
        fh = urllib2.urlopen(self.scpdurl)
        resp = fh.read()
        resp = re.sub(' xmlns=\"[^\"]+\"','', resp, 1)
        root = xt.fromstring(resp)
        for item in root.findall('./actionList/action'):
            try: 
                action_name = item.find('name')
            except:
                continue
            new_action = upnp_action(action_name.text)
            print new_action
            self.action_list[action_name] = new_action
    
    def __repr__(self):

        return 'id:{} type:{} \n scpdurl:{}, control_url:{}'.format(self.service_id, self.service_type, self.scpdurl, self.control_url )
    
    def AV_capapable(self):
        return (self.service_type == ':AVTransport:1')


        
        
    def subscribe_to_events(self, receiving_url):
        fh = urllib2.urlopen(self.event_sub_url)
      
    
        
        
        
    def invoke_PLAY(self):
        args = {}
        args['InstanceID'] = 0
        args['Speed'] = DEFAULT_PLAY_SPEED   
        msg_body = SOAP_BODY_TEMPLATE() 
        
        header_soapaction = SOAPACTION_TEMPLATE.format(service=self.service_id,serviceType=self.service_type, v=SERVICE_VER, actionName='Play')
        header = SOAP_HEADER_TEMPLATE
        header['Content-Length'] = len(msg_body)
        header['SOAPACTION'] = header_soapaction
        
       
        req = urllib2.Request(self.control_url, data=msg_body, headers=header)
        ret = urllib2.urlopen(req).read()
        print ret
        
        
         
    def invoke_SetAVTransportURI(self):
        
        args = {}
        header_soapaction = SOAPACTION_TEMPLATE.format(service=self.service_id,serviceType=self.service_type,v=SERVICE_VER, actionName='SetAVTransportURI')
        target_uri = 'http://us.napster.com/assets/logos/logo-napster@3x-4b04e0ffd563311e5789303bb7031a27.png'
        
        args['InstanceID'] = 0
        args['CurrentURI'] = urllib.urlencode(target_uri)

        attr = wrap_in_xml(args)
        
        msg_body = SOAP_BODY_TEMPLATE.format(actionName='SetAVTransportURI', serviceType='AVTransport', version='1', arguments=attr)
              
        SOAP_HEADER_TEMPLATE['Content-Length'] = len(msg_body)
        SOAP_HEADER_TEMPLATE['SOAPACTION'] = header_soapaction
       
        print msg_body
        try: 
            req = urllib2.Request(self.control_url, data=msg_body, headers=SOAP_HEADER_TEMPLATE)
            resp = urllib2.urlopen(req).read()
        except urllib2.HTTPError as e:
            print e.reason
        except urllib2.URLError as e:
            print e.reason
        else:
            print resp
            



def xml_to_info(xml, root_url):
    service_list = []
    xml = re.sub(' xmlns=\"[^\"]+\"','', xml, 1)
    info = xt.fromstring(xml)    
    
    friendly_name = info.find('./device/friendlyName').text 
    print friendly_name
  
    for s in info.findall('./device/serviceList/service'):  
        s_type = s.find('serviceType').text
        s_type = re.sub(NAME_SPACE['service_type'], '', s_type)
        
        service_id = s.find('serviceId').text
        service_id = re.sub(NAME_SPACE['service_id'], '',s_type )

        service_node = upnp_service(s_type, service_id)
        host_ip_port = extract_host_info(root_url)
        scpd_url = host_ip_port + s.find('SCPDURL').text
        
        control_url = host_ip_port + s.find('controlURL').text
        service_node.set_scpdurl(scpd_url)
        service_node.set_control_url(control_url)
        
        print(service_node)
        
        service_node.get_service_actions()
        service_list.append(service_node)        
        if service_node.AV_capapable():
            service_node.invoke_SetAVTransportURI()
        
    
