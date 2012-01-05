######################################################################
#
# FSP3000R7DeviceMib modeler plugin
#
# Copyright (C) 2011 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7DeviceMib

FSP3000R7DeviceMib gets System name from the NCU-II

"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class FSP3000R7DeviceMib(SnmpPlugin):

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Device"

    # FspR7-MIB mib neDatabaseSerialNumber is .1.3.6.1.4.1.2544.1.11.2.2.1.17.0
    # it's the serial number of the shelf
    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.2544.1.11.2.2.1.17.0' : 'setHWSerialNumber',
       })

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('Retrieving serial number using %s for device %s', self.name(), device.id)
        # Collect serial number.  tabledata is not applicable here
        getdata, tabledata = results

        log.debug( "getdata SNMP call returned: %s", getdata )
        om = self.objectMap(getdata)
        return om
