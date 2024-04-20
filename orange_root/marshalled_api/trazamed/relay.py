import string
from urllib import response
from zeep import Client, Settings
from zeep.wsse.username import UsernameToken
from zeep.plugins import Plugin,HistoryPlugin
#from lxml import etree
#from zeep import xsd
import pathlib



#from zeep.transports import Transport
#transport = Transport(timeout=10, operation_timeout=300)

#from zeep.wsse.signature import Signature
user_name_token = UsernameToken('testwservice', 'testwservicepsw')
settings = Settings(strict=False, xml_huge_tree=False, force_https=True, raw_response=False )
history = HistoryPlugin()
wsdl='https://servicios.pami.org.ar/trazamed.WebService?wsdl'
#wsdl='trazamed.wsdl'
wsdl= pathlib.Path(__file__) / "trazamed.wsdl"
client = Client(wsdl=wsdl,
                settings=settings,
                wsse=user_name_token,
                plugins=[history])

factory = client.type_factory('ns0')


#op = factory.getTransaccionesNoConfirmadas()
#op.arg0="pruebasws"
#tito["arg1"]="Clave1234"
#tito["arg5"]="glnws"
#tito["arg8"]="01/01/2024"
#tito["arg9"]="04/04/2024"
#element = client.get_element('{http://business.mywebservice.inssjp.com/}getTransaccionesNoConfirmadas')
#a = element(
#                [
#                    xsd.Element("arg0", xsd.String()),
#                    xsd.Element("arg1", xsd.String()),
#                    xsd.Element("arg5", xsd.String())
#                ]
#                                             'pruebasws', 
#                                            'Clave1234',None,None,None,
#                                             'glnws',None,None,
#                                             '01/01/2024',
#                                             '04/04/2024'
#
#)

#    {
#                                             "arg0":'pruebasws', 
#                                             "arg1":'Clave1234',
#                                             "arg5":'glnws',
#                                             "arg8":'01/01/2024',
#                                             "arg9":'04/04/2024'
#                                             }
#                                             )

#b =  a(arg0='pruebasws',arg1='Clave1234',arg5='glnws')

#res = factory.transaccionesWSResult()
#toto = client.create_message(client.service,'getTransaccionesNoConfirmadas')

service = client.create_service(
    binding_name='{http://business.mywebservice.inssjp.com/}IWebServiceSoapBinding', 
    address='https://servicios.pami.org.ar/trazamed.WebService')

#
response = service.getTransaccionesNoConfirmadas(
    'pruebasws', 
    'Clave1234',None,None,None,
    'glnws',None,None,
    '01/01/2024',
    '04/04/2024'
    )


#print(response.text)
print(history.last_sent)
print(history.last_received)

if not response.hay_error:
    for e in response.list:
        print(e._id_transaccion)


#for hist in [history.last_sent, history.last_received]:
#    print(etree.tostring(hist["envelope"], encoding="unicode", pretty_print=True))

def fake(call):
    return [None,1,2,"tree"]

#def get_relay(a:string):
#    return fake