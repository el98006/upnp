'''
Created on Nov 2, 2016

@author: eli
'''
import urllib2
import re
import xml.etree.ElementTree as xt
from idlelib.idle_test.mock_tk import Event
from matplotlib.cbook import Null

UDNP_SERVICE ='urn:schemas-upnp-org:service'
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
                     


class upnp_action:
    '''
    action_name: Play
    argument: name = InstanceID,  direction: in, relatedStateVariable: A_ARG_TYPE_InstanceID;
    name: Speed, direciton: in, relatedStateVariable: TransportPlaySpeed
    
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
        s_type = s.find('serviceType')
        print_element(s_type)
        print_element(s.find('serviceId'))
        print_element(s.find('controlURL'))
        service_node = upnp_service(s.find('serviceId').text, s_type.text)
        service_node.scpdurl = root_url + s.find('SCPDURL')
        print(service_node)
        service_node.get_service_actions()
        service_list.append(service_node)
        

        
    


#if __name__ == '__main__':
#    xml_to_info()