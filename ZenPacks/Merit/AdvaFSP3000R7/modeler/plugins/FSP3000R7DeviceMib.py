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
import cPickle
import time


class FSP3000R7DeviceMib(SnmpPlugin):

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Device"

    # FspR7-MIB mib neSystemId is .1.3.6.1.4.1.2544.1.11.2.2.1.1.0
    # FspR7-MIB mib neSwVersion is .1.3.6.1.4.1.2544.1.11.2.2.1.5.0
    # it's the name and software version of the shelf
    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.2544.1.11.2.2.1.1.0' : 'setHWTag',
        '.1.3.6.1.4.1.2544.1.11.2.2.1.5.0' : 'setOSProductKey',
    })

    inventoryTablecolumns = { '.1.1.': 'inventoryUnitName' }

    entityTablecolumns = {
        '.1.2.': 'entityContainedIn',
        '.1.5.': 'entityIndexAid',
        '.1.7.': 'entityAssignmentState',
        '.1.8.': 'entityEquipmentState',
    }

    opticalIfDiagcolumns = { '.1.3.': 'opticalIfDiagInputPower' }

    # snmpGetTableMaps gets tabular data
    snmpGetTableMaps = (
        GetTableMap('inventoryTableEntry',
                    '1.3.6.1.4.1.2544.2.5.5.1',
                    inventoryTablecolumns),
        GetTableMap('entityTableEntry',
                    '1.3.6.1.4.1.2544.2.5.5.2',
                    entityTablecolumns),
        GetTableMap('opticalIfDiagTableEntry',
                    '1.3.6.1.4.1.2544.1.11.2.4.3.5',
                    opticalIfDiagcolumns),
    )


    def process(self, device, results, log):
        """
        collect snmp information from this device, set serial number,
        and write cached SNMP data for subsequent component modeling in an
        egg file.
        """

        log.info('Retrieving Adva system title and component modeling SNMP data using %s for device %s', self.name(), device.id)

        inventoryTable = entityTable = opticalIfDiagTable = False
        cache_file_time = 0

        # Collect serial number and tabledata
        getdata = {}
        getdata['setHWTag'] = False
        getdata['setOSProductKey'] = 'Unknown'
        getdata, tabledata = results
        if getdata['setHWTag'] is False:
            log.info("Couldn't get system name from Adva shelf.")
            return
        if getdata['setHWTag'] == '':
            log.info("Adva shelf lacks a system name.  Set it before running any modelers.")
            return


        cache_file_name = '/tmp/%s.Adva_inventory_SNMP.pickle' % device.id
        inventoryTable     = tabledata.get('inventoryTableEntry')
        entityTable        = tabledata.get('entityTableEntry')
        opticalIfDiagTable = tabledata.get('opticalIfDiagTableEntry')
        cache_file_time = time.time()

        log.debug( "getdata SNMP call returned: %s", getdata )

        try:
            cache_file = open(cache_file_name, 'w')
            cPickle.dump(inventoryTable,cache_file)
            cPickle.dump(entityTable,cache_file)
            cPickle.dump(opticalIfDiagTable,cache_file)
            cPickle.dump(cache_file_time,cache_file)
        except IOError,cPickle.PickleError:
            log.warn("Couldn't store SNMP data in " + cache_file_name)


        om = self.objectMap(getdata)
        return om
