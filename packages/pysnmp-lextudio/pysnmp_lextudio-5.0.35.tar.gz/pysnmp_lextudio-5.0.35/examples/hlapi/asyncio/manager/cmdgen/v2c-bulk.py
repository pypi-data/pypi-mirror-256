"""
SNMPv2c
+++++++

Send SNMP GET request using the following options:

  * with SNMPv2c, community 'public'
  * over IPv4/UDP
  * to an Agent at demo.pysnmp.com:161
  * for an instance of SNMPv2-MIB::sysDescr.0 MIB object
  * Based on asyncio I/O framework

Functionally similar to:

| $ snmpbulkget -v2c -c public demo.pysnmp.com SNMPv2-MIB::sysDescr.0

"""#
import asyncio
from pysnmp.hlapi.asyncio.slim import Slim
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType

async def run():
    slim = Slim()
    errorIndication, errorStatus, errorIndex, varBinds = await slim.bulk(
        'public',
        'demo.pysnmp.com',
        161,
        0,
        50,
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        for varBind in varBinds:
            print(" = ".join([x.prettyPrint() for x in varBind]))

    slim.close()


asyncio.run(run())
