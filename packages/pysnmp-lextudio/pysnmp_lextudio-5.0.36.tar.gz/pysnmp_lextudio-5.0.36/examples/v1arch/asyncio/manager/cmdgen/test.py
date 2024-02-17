
import asyncio
from pysnmp.hlapi.asyncio import *
import time

async def run():
    
    request_args = [
            SnmpEngine(),
            CommunityData('public', mpModel=0),
            UdpTransportTarget(('localhost', 161)),
            ContextData(),
        ]
    while True:
        
        errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
            *request_args,
            ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.8.9'))
        )

        print('sent')

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
            )
                  )
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))

        time.sleep(2)


asyncio.run(run())