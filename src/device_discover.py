'''
Created on Nov 1, 2016

@author: eli
'''
import urllib2
import socket
from utils import xml_to_info, AVService
import base64


SSDP_BROADCAST_PORT = 1900
#SSDP_BROADCAST_ADDR = "10.151.61.255"
SSDP_BROADCAST_ADDR = "239.255.255.250"

SSDP_BROADCAST_PARAMS = ["M-SEARCH * HTTP/1.1",
                         "HOST: {}:{}".format(SSDP_BROADCAST_ADDR,
                                              SSDP_BROADCAST_PORT),
                         "MAN: \"ssdp:discover\"",
                         "MX: 10",
                         "ST: ssdp:all", "", ""]

SSDP_BROADCAST_MSG = "\r\n".join(SSDP_BROADCAST_PARAMS)



def register_dev(url_list): 
    
    devices = []
    for url in url_list:
        fh = urllib2.urlopen(url)
        dev_details = fh.read()
        print url
        device =  xml_to_info(dev_details, url)
        if device:
            devices.append(device)
    return devices
        
        
    
def probe_dev(timeout=3.0):
    devices =[]
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 4)
    s.bind(("",SSDP_BROADCAST_PORT+10))
     
    s.sendto(SSDP_BROADCAST_MSG.encode("UTF-8"),(SSDP_BROADCAST_ADDR, SSDP_BROADCAST_PORT))
    s.settimeout(timeout)
     
     
    while True:
         
        try: 
            data, _ = s.recvfrom(1024)
        except socket.timeout:
            break
        
        try:
            result = [ line.split(':',1) for line in data.decode('UTF-8').split('\r\n')[1:] ]
            device = dict([(entry[0].strip().lower(), entry[1].strip()) for entry in result if len(entry) >= 2])
            devices.append(device)
        except:
            pass
        
   
    device_urls = [device["location"] for device in devices if "AVTransport" in device['st']]
    
    devices = register_dev(device_urls)
    return devices
    
def send_to_dev(device_node):
    s_name, service_list = device_node
    for s in service_list:
        if isinstance(s, AVService):
            s.invoke_SetAVTransportURI('http://www.baidu.com/img/bd_logo1.png')
            s.invoke_PLAY()  
                 
def  list_device(devices):
    for d in devices:
        friendly_name, _ = d
        print '{} -> {}'.format(devices.index(d), friendly_name.encode('utf-8'))
                    
    
if __name__ == '__main__':
    devices = probe_dev(10)
    if devices is None: 
        print ('device available for test, exiting')
        exit()   
    else:
        list_device(devices)
        choice = input('choose the device to test')
        send_to_dev(devices[choice])
        
        
        
    
    
            
    
         

