__doc__="""FSP3000R7ModuleMib

Look for modules that contain amplifier stages, transponder optics. etc.

"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7Channels import Channels
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibPickle import getCache
from ZenPacks.Merit.AdvaFSP3000R7.lib.FanModels import FanModels
from ZenPacks.Merit.AdvaFSP3000R7.lib.NCUModels import NCUModels
from ZenPacks.Merit.AdvaFSP3000R7.lib.PowerSupplyModels import PowerSupplyModels

# flatten list of lists
FanorNCUorPSModels = [item for sublist in \
                          [FanModels,NCUModels,PowerSupplyModels]
                              for item in sublist]

class FSP3000R7ModuleMib(SnmpPlugin):

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Module"
    relname = "FSP3000R7Mod"

    # FspR7-MIB mib neSystemId is .1.3.6.1.4.1.2544.1.11.2.2.1.1.0.  Not used;
    # Have to get something with SNMP or modeler won't process
    snmpGetMap = GetMap({'.1.3.6.1.4.1.2544.1.11.2.2.1.1.0' : 'setHWTag'})

    def process(self, device, results, log):
        """process snmp information for containers for this device"""
        log.info('processing %s for device %s', self.name(), device.id)

        # tabledata is not used (get tables from cache pickle file created
        # in FSP3000R7Device modeler)
        getdata = {}
        getdata['setHWTag'] = False
        getdata, tabledata = results
        if not getdata['setHWTag']:
            log.info("Couldn't get system name from Adva shelf.")

        inventoryTable = entityTable = opticalIfDiagTable = False
        containsModules = {}
        gotCache, inventoryTable, entityTable, opticalIfDiagTable, \
            containsModules = getCache(device.id, self.name(), log)
        if not gotCache:
            log.debug('Could not get cache for %s' % self.name())
            return

        # relationship mapping
        rm = self.relMap()

        # pick up MOD-* containers from entityTable
        for entityIndex in entityTable:
            # Power Supply, NCU and Fan models are already top level containers
            if not (entityIndex in inventoryTable):
                continue
            inventoryUnitName = inventoryTable[entityIndex]['inventoryUnitName']
            if inventoryUnitName in FanorNCUorPSModels:
                continue
            if entityTable[entityIndex]['entityIndexAid'].startswith('MOD-'):
                om = self.objectMap()
                om.EntityIndex = int(entityIndex)
                om.inventoryUnitName = inventoryUnitName
                om.entityIndexAid = entityTable[entityIndex]['entityIndexAid']
                om.entityAssignmentState = \
                    entityTable[entityIndex]['entityAssignmentState']
                om.interfaceConfigId     = ''
                om.sortKey               = '000000000'
                om.entityAssignmentState = 'Not set by modeler'
                om.containedIn = 'Chassis'
                om.id = self.prepId(om.entityIndexAid)
                om.title = om.entityIndexAid
                om.snmpindex = int(entityIndex)
                log.info('Found module at: %s inventoryUnitName: %s',
                         om.entityIndexAid, om.inventoryUnitName)
                rm.append(om)

        return rm
