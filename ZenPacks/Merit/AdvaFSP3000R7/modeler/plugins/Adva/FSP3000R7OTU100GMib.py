######################################################################
#
# FSP3000R7OTU100GMib modeler plugin
#
# Copyright (C) 2014 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7OTU100GMib

FSP3000R7OTU100GMib maps 100G Muxsponder OTU ports on a FSP3000R7 system

"""

from re import match
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibPickle import getCache


# Use SNMP data from Device Modeler in a cache file.  Can't be a PythonPlugin
# since those run before any SnmpPlugin; device modeler is an PythonPlugin so
# the cache file will be created before this is run.
# Can't use FSP3000R7MibCommon since Muxsponder OTU ports don't respond to OPR
class FSP3000R7OTU100GMib(SnmpPlugin):

    modname = 'ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7OTU100Gig'
    relname = 'FSP3000R7OTU100G'

    # FspR7-MIB mib neSystemId is .1.3.6.1.4.1.2544.1.11.2.2.1.1.0.  Not used;
    # Have to get something with SNMP or modeler won't process
    snmpGetMap = GetMap({'.1.3.6.1.4.1.2544.1.11.2.2.1.1.0' : 'setHWTag'})

    def process(self, device, results, log):
        """process snmp information for components from this device"""
        log.info('processing %s for device %s', self.name(), device.id)

        # These models contain OTU100G amplifiers to look for network ports on
        componentModels = ['10TCC-PCTN-10G+100GB',
                           '10TCC-PCTN-10G+100GC',
                           '10TCE-PCN-10G+100G',
                           '10TCE-PCN-10G+100G-GF']

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

        # look for blades containing 100G Muxponder in inventory table
        for bladeEntityIndex in inventoryTable:
            bladeInv = inventoryTable[bladeEntityIndex]['inventoryUnitName']
            bladeIndexAid = entityTable[bladeEntityIndex]['entityIndexAid']
            if not bladeInv in componentModels:
                continue
            log.info('found 100G Muxponder OTU matching model %s' % bladeInv)
    
            # find ports from entityContainedIn for 100G OTU entityIndex
            portEntityIndex,portEntityIndexAid = \
                self.__findPort(log,bladeEntityIndex,entityTable)
            if portEntityIndex is False:
                continue

            om = self.objectMap()
            om.EntityIndex = int(portEntityIndex)
            om.inventoryUnitName = bladeInv
            if 'interfaceConfigIdentifier' in entityTable[portEntityIndex]:
                om.interfaceConfigId = \
                   entityTable[portEntityIndex]['interfaceConfigIdentifier']
            om.entityIndexAid=entityTable[portEntityIndex]['entityIndexAid']
            om.entityAssignmentState = \
                entityTable[portEntityIndex]['entityAssignmentState']
            om.id = self.prepId(om.entityIndexAid)
            om.title = om.entityIndexAid
            om.snmpindex = int(portEntityIndex)
            log.info('Found 100Gig Muxponder OTU at: %s inventoryUnitName: %s',
                     om.entityIndexAid, om.inventoryUnitName)

            rm.append(om)

        return rm


    def __findPort(self,log,parentEntityIndex,entityTable):
        parentEntityIndex = str(parentEntityIndex)
        for entityIndex in entityTable:
           entityContainedIn =str(entityTable[entityIndex]['entityContainedIn'])
           if entityContainedIn == parentEntityIndex:
               if match(r'CH\-\d+\-\d+\-N',
                        entityTable[entityIndex]['entityIndexAid']):
                   return entityIndex,entityTable[entityIndex]['entityIndexAid']
               else:
                   i,a = self.__findPort(log,entityIndex,entityTable)
                   if i is not False:
                       return i,a
        return False, False
