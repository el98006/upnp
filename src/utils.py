'''
Created on Nov 2, 2016

@author: eli
'''
import urllib2
import re
import xml.etree.ElementTree as xt
from idlelib.idle_test.mock_tk import Event

UDNP_SERVICE ='urn:schemas-upnp-org:service'
SUB_MSG_TEMPLATE = ['SUBSCRIBE {} HTTP/1.1',  
'HOST: {}',
'CALLBACK: {}',
'NT: upnp:Event',
]

class upnp_action:
    def init(self, action_name):
        self.name = action_name
        
class upnp_servcie:
    def init(self):
        self.id = ''
        self.service_type = ''
        self.control_url = ''
        self.event_sub_url =''
        self.scpdurl = ''
    
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
        
    def subscribe_to_events(self, receiving_url):
        fh = urllib2.urlopen(self.event_sub_url)
        '''
        message = 
        header = 
        resp = fh.post()
        resp contains names and current values of all evented variables
        '''
    def renew_event_subscription(self):
        
        
        
        
         
    



def print_element(item):
    #service_value = item.text.encode('utf8').rsplit(':',2)[1]
    print '{} = {}'.format(item.tag, item.text)
    
def xml_to_info(xml):
    #with open('xiaomi.xml','rt') as fh:
    #    xml = fh.read()
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
        
        

        
    


if __name__ == '__main__':
    xml_to_info()