'''
Created on Nov 2, 2016

@author: eli
'''
import urllib
import re
import xml.etree.ElementTree as xt

UDNP_SERVICE ="urn:schemas-upnp-org:service"

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