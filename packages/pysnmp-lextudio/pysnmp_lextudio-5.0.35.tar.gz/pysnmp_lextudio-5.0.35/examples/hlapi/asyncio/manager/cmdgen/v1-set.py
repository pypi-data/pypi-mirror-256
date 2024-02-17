"""
SNMPv1
++++++

Send SNMP GET request using the following options:

  * with SNMPv1, community 'public'
  * over IPv4/UDP
  * to an Agent at demo.pysnmp.com:161
  * for an instance of SNMPv2-MIB::sysDescr.0 MIB object
  * Based on asyncio I/O framework

Functionally similar to:

| $ snmpget -v1 -c public demo.pysnmp.com SNMPv2-MIB::sysDescr.0

"""#
import asyncio
from pysnmp.hlapi.asyncio.slim import Slim
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType

async def run():
    slim = Slim(1)
    errorIndication, errorStatus, errorIndex, varBinds = await slim.set(
        'public',
        'demo.pysnmp.com',
        161,
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysLocation", 0), "Shanghai")
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
