'''
Created on Nov 2, 2016

@author: eli
'''
import urllib2
import re
import xml.etree.ElementTree as xt
import xml

UPNP_SERVICE ='urn:schemas-upnp-org:service'
SUB_MSG_TEMPLATE = ['SUBSCRIBE {} HTTP/1.1',  
'HOST: {}',
'CALLBACK: {}',
'NT: upnp:Event',
]

POST_MSG_TEMPLATE = {
    "Content-Type"   : "text/xml; charset=\"utf-8\"",
    "Content-Length" : "{}",
    "Connection"     : "close",
#    "SOAPACTION"     : "\"{}#{}\""
} 
                     
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
    name: Speed, direciton: in, relatedStateVariable: TransportPlaySpeed
    
    methods: execute()
    '''
    
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
        argument: name, direction, relatedStableVariable
        
        '''
        
        fh = urllib2.urlopen(self.scpdurl)
        resp = fh.read()
        '''
        with open('AVTransport1.xml', 'rt') as xml:
            resp = xml.read()
        '''
        resp = re.sub(' xmlns=\"[^\"]+\"','', resp, 1)
        root = xt.fromstring(resp)
        for item in root.findall('./actionList/action'):
            action_name = item.find('name')
            new_action = upnp_action(action_name.text)
            print new_action
            self.action_list.append(new_action)
    
    def __repr__(self):
        return 'service id:{} type:{}\nscpdurl:{}\ncontrol_url:{}\n'.format(self.id, self.service_type, self.scpdurl, self.control_url )
    
    def do_action(self, upnp_action):
        ''' accept an action object, create payload and send to service control_url and perform an action,
        return result
        '''    
        
        
        
    def subscribe_to_events(self, receiving_url):
        fh = urllib2.urlopen(self.event_sub_url)
        '''
        message = 
        header = 
        resp = fh.post()
        resp contains names and current values of all evented variables
        '''
    #def renew_event_subscription(self):
        
        
        
        
         
    



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
        

        
    
'''

if __name__ == '__main__':
    s = upnp_service('AVTransport:1', 'AVTransport:1')
    s.set_control_url('/xml/AVTransport1')
    s.get_service_actions()
'''
