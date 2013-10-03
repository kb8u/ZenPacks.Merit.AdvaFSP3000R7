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

    # FspR7-MIB mib neSystemId is .1.3.6.1.4.1.2544.1.11.2.2.1.1.0
    # FspR7-MIB mib neSwVersion is .1.3.6.1.4.1.2544.1.11.2.2.1.5.0
    # it's the name and software version of the shelf
    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.2544.1.11.2.2.1.1.0' : 'setHWTag',
        '.1.3.6.1.4.1.2544.1.11.2.2.1.5.0' : 'setOSProductKey',
    })


    def process(self, device, results, log):
        """
        collect snmp information from this device, set serial number,
        and write cached SNMP data for subsequent component modeling in a
        pickle file.
        """

        log.info('Retrieving Adva system title using %s for device %s',
                 self.name(), device.id)

        # Collect tag and serial number 
        getdata = {}
        getdata['setHWTag'] = False
        getdata['setOSProductKey'] = 'Unknown'
        getdata, tabledata = results
        if not getdata['setHWTag']:
            log.info("Couldn't get system name from Adva shelf.")
            return

        om = self.objectMap(getdata)
        return om
