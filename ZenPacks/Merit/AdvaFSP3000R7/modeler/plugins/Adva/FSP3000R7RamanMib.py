######################################################################
#
# FSP3000R7RamanMib modeler plugin
#
# Copyright (C) 2014 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7RamanMib

FSP3000R7RamanMib maps RAMAN amplifiers on a FSP3000R7 system

"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibPickle import getCache


class FSP3000R7RamanMib(SnmpPlugin):

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Raman"
    relname = "FSP3000R7Raman"

    # opticalIfDiagRamanPumpPower OID
    snmpGetTableMaps = [GetTableMap('opticalIfDiag',
                                    '.1.3.6.1.4.1.2544.1.11.2.4.3.5.1',
                                    { '.14' : 'RamanPumpPower' })]

    def process(self, device, results, log):
        """process snmp information for components from this device"""
        log.info('processing %s for device %s', self.name(), device.id)

        # SNMP table
        getdata, tabledata = results

        # cached data from device modeler
        inventoryTable = entityTable = opticalIfDiagTable = False
        containsOPRModules = {}
        gotCache, inventoryTable, entityTable, opticalIfDiagTable, \
            containsOPRModules = getCache(device.id, self.name(), log)
        if not gotCache:
            log.debug('Could not get cache for %s' % self.name())
            return

        # relationship mapping
        rm = self.relMap()

        td = tabledata['opticalIfDiag']
        for entityIndex in td:
            # skip invalid entries
            if td[entityIndex]['RamanPumpPower'] == -2147483648:
                continue

            om = self.objectMap()

            if entityIndex in inventoryTable:
                invName = inventoryTable[entityIndex]['inventoryUnitName']
            else:
                invName = ''
            modName = entityTable[entityIndex]['entityIndexAid']

            om.EntityIndex = int(entityIndex)
            om.inventoryUnitName = invName
            # Add comment (e.g. 'RAMAN from Niles') if one exists
            if 'interfaceConfigIdentifier' in entityTable[entityIndex]:
                om.interfaceConfigId = \
                    entityTable[entityIndex]['interfaceConfigIdentifier']
            om.entityIndexAid = modName
            om.entityAssignmentState = \
                entityTable[entityIndex]['entityAssignmentState']
            om.id = self.prepId(modName)
            om.title = modName
            om.snmpindex = int(entityIndex)
            log.info('Found RAMAN amp at: %s inventoryUnitName: %s',
                     modName, invName)
            rm.append(om)

        return rm
