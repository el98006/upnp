'''
Created on Nov 2, 2016

@author: eli
'''
import urllib
import re
import xml.etree.ElementTree as xt

def xml_to_info():
    xml = xt.parse('xiaomi.xml')
    re
    info = xml.getroot()
    for item in info.iter():
        print item.tag
        print item.text
    


if __name__ == '__main__':
    xml_to_info()