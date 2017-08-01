'''
Created on Jul 11, 2017

@author: aneesh.c
'''


log_in_url = 'https://www.gundeals.com/index.php/api/index/index/login'
product_url = 'https://www.gundeals.com/index.php/api/index/index/call'

login_xml="""<?xml version='1.0' encoding='utf-8'?>
<x:Envelope xmlns:x="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:Magento">
    <x:Header/>
    <x:Body>
        <urn:login>
            <urn:username>Chatbot2017</urn:username>
            <urn:apiKey>QYM;86HLiYWx</urn:apiKey>
        </urn:login>
    </x:Body>
</x:Envelope>"""


http_headers = { 
 "User-Agent":"Mozilla/4.0 (compatible; MSIE 5.5;Windows NT)", 
 "Accept" :  "application/soap+xml,multipart/related,text/*", 
 "Cache-Control" :  "no-cache", 
 "Pragma" :  "no-cache", 
 "Content-Type" :  "text/xml; charset=utf-8"
}





first_part ="""
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
</SOAP-ENV:Envelope> """