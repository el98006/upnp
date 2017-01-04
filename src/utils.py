'''
updated on 11/29
Created on Nov 2, 2016

@author: eli
'''
import urllib
import re
import xml.etree.ElementTree as xt
import urllib2




A_ARG_TYPE_InstanceID = 1
DEFAULT_PLAY_SPEED = 1
SERVICE_VER = '1'

SERVICE_TYPE_NAMESPACE = 'urn:schemas-upnp-org:service'
SERVICE_ID_NAMESPACE =  'urn:upnp-org:serviceId'
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
    
      
        
class UpnpService(object):
    ''' service_type: 'AVTransport:1', serviceId: AVTransport, scpdurl:'/AVTransport1.xml'
    control_url = /upnp/control/AVTransport1
    eventSubURL = /upnp/event/AVTransport1
    '''
    def __init__(self, s_id, s_type, **kwargs):
        self.service_id =s_id
        self.service_type = s_type
        if  'control_url'  in kwargs.keys():
            self.control_url = kwargs['control_url']
        else:
            self.control_url = None
        if 'event_sub_url' in kwargs.keys():
            self.event_sub_url = kwargs['event_sub_url']
        else: 
            self.event_sub_url = None
        
        if 'scpd_url' in kwargs.keys():
            self.scpd_url = kwargs['scpd_url']
        else:
            self.scpd_url = None
        self.action_list = {}

    def set_event_sub_url(self, url):
        self.event_sub_url = url
    
    
    def get_service_actions(self):
        '''
        retrieve available list of actions by querying scpdurl
        return 
        stateTable and actionLists
        stableTable: name, dataType, allowedValue
        action: name, argumentList, 
        argument: name, direction, relatedStableVariable
        
        '''
        
        fh = urllib2.urlopen(self.scpd_url)
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

        return 'id:{}, type:{}, \n scpd_url:{}\n control_url:{}'.format(self.service_id, self.service_type, self.scpd_url, self.control_url )
    
    def AV_capapable(self):
        return (self.service_type == ':AVTransport:1')


        
        
    def subscribe_to_events(self, receiving_url):
        #fh = urllib2.urlopen(self.event_sub_url)
        pass
        
         
    
class AVService(UpnpService):
   
    def __init__(self, s_id, s_type, **kwargs):
        UpnpService.__init__(self, s_id, s_type, **kwargs)
        
    def invoke_SetAVTransportURI(self, media_uri, *args,**kwargs):
        
        args = {}
        header_soapaction = SOAPACTION_TEMPLATE.format(service=self.service_id,serviceType=self.service_type,v=SERVICE_VER, actionName='SetAVTransportURI')
        target_uri = media_uri
        
        args['InstanceID'] = 0
        args['CurrentURI'] = target_uri

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

    def invoke_PLAY(self):
        args = {}
        args['InstanceID'] = 0
        args['Speed'] = DEFAULT_PLAY_SPEED   
        msg_body = SOAP_BODY_TEMPLATE
        
        header_soapaction = SOAPACTION_TEMPLATE.format(service=self.service_id,serviceType=self.service_type, v=SERVICE_VER, actionName='Play')
        header = SOAP_HEADER_TEMPLATE
        header['Content-Length'] = len(msg_body)
        header['SOAPACTION'] = header_soapaction
        
        try:
            req = urllib2.Request(self.control_url, data=msg_body, headers=header)
            ret = urllib2.urlopen(req).read()
        except urllib2.HTTPError as e:
            print e.reason
        except urllib2.URLError as e:
            print e.reason
        else:
            print ret
        
        
def get_matching_data(full_str, match_pattern, match_index=1):
    if full_str is None:
        return None
    else:
        _pattern = re.compile(match_pattern)
        
        m_group = re.match(_pattern, full_str)
        if m_group and m_group.group(match_index):
            return m_group.group(match_index)
        else:
            return None
    
def xml_to_info(xml, root_url):
    service_list = []
    xml = re.sub(' xmlns=\"[^\"]+\"','', xml, 1)
    info = xt.fromstring(xml)
    av_playable = False
    s_params = {}
    
    friendly_name = info.find('./device/friendlyName').text 
    print friendly_name
  
    for s in info.findall('./device/serviceList/service'):  
        s_type = get_matching_data(s.find('serviceType').text, SERVICE_TYPE_NAMESPACE + ':(\w+):(\d+)')
        s_id = get_matching_data(s.find('serviceId').text, SERVICE_ID_NAMESPACE+':(\w+)')
        
        
        host_ip_port = extract_host_info(root_url)
        
        scpd_url = s.find('SCPDURL')
        if scpd_url is not None:
            scpd_url = host_ip_port + scpd_url.text
            s_params['scpd_url'] = scpd_url
        
        control_url = s.find('controlURL')
        if control_url is not None:
            control_url = host_ip_port + control_url.text
            s_params['control_url'] = control_url
        
        if s_type is not None:
            service_node = AVService(s_id, s_type, **s_params)
            av_playable = True
        else: 
            service_node = UpnpService(s_id, s_type, **s_params)
            service_node.get_service_actions()
        
        print(service_node)
        service_list.append(service_node)        
     
    if av_playable: 
        return (friendly_name,service_list) 
    else: 
        return None   
        
    
