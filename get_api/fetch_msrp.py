'''
Created on Jul 11, 2017

@author: aneesh.c
'''
import re
import urllib2
import xml.etree.ElementTree as ET
from magento_credentials import *
import pandas as pd



first_partinit ="""
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="urn:Magento" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<SOAP-ENV:Body>
<ns1:multiCall>
<sessionId xsi:type="xsd:string">%s</sessionId>
<calls SOAP-ENC:arrayType="xsd:ur-type[1]" xsi:type="ns1:FixedArray">
"""
second_part = """
<item SOAP-ENC:arrayType="xsd:string[2]" xsi:type="SOAP-ENC:Array">
<item xsi:type="xsd:string">catalog_product.info</item>
<item xsi:type="xsd:string">%s</item>
</item>"""

third_part = """
</calls>
<options xsi:nil="true"/>
</ns1:multiCall>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""


def get_msrp(frame):
    mfg_part_nos = list(frame['MfgPartNumber'])
    request_object = urllib2.Request(log_in_url, login_xml, http_headers)
    response = urllib2.urlopen(request_object)
    html_string = response.read()
    tree = ET.ElementTree(ET.fromstring(html_string))
    for data in tree.getiterator('loginReturn'):
        key = data.text
    first_part = first_partinit % (key)
    init = ''
    for ele in mfg_part_nos:
        init = init + second_part % (ele)
    end_point = first_part+init+third_part
    product_details_obj = urllib2.Request(product_url, end_point, http_headers)
    response = urllib2.urlopen(product_details_obj)
    html_string = response.read()
    second_tree = ET.ElementTree(ET.fromstring(html_string))
    root = second_tree.getroot()
    item_root1 = root[0][0][0]
    l = []
    for item1 in item_root1.findall("item"):
        d = {}
        for i in item1:
            d[i.find("key").text] = i.find("value").text
        if not 'faultCode' in d:
            sub_frame = frame.loc[frame['MfgPartNumber'] == d['product_id']]
            sub_frame['MSRP'] = d['price']
            l.append(sub_frame)
    final_frame = pd.concat(l)
    return final_frame
    