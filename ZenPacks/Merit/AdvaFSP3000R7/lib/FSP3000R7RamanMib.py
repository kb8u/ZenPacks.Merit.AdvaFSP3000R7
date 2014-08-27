######################################################################
#
# FSP3000R7RamantMib modeler plugin
#
# Copyright (C) 2014 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7RamanPortMib

FSP3000R7RamanMib maps RAMAN amplifier ports on a FSP3000R7 system

"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibPickle import getCache


# Use SNMP data from Device Modeler in a cache file.  Can't be a PythonPlugin
# since those run before any SnmpPlugin; device modeler is an PythonPlugin so
# the cache file will be created before this is run.
# Can't use FSP3000R7MibCommon since Raman amplifiers don't respond to OPR
class FSP3000R7RamanPortMib(SnmpPlugin):

    # set relationships in child class
    modname = ''
    relname = ''
    # set in child class, either -N or -U (Network or Upgrade)
    portType = ''

    # FspR7-MIB mib neSystemId is .1.3.6.1.4.1.2544.1.11.2.2.1.1.0.  Not used;
    # Have to get something with SNMP or modeler won't process
    snmpGetMap = GetMap({'.1.3.6.1.4.1.2544.1.11.2.2.1.1.0' : 'setHWTag'})

    def process(self, device, results, log):
        """process snmp information for components from this device"""
        log.info('processing %s for device %s', self.name(), device.id)

        # These models contain Raman amplifiers to look for network ports on
        componentModels = ['RAMAN-C10', '2RAMAN-C15-LL', 'AMP-S20L-C15']

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

        # look for blades containing RAMAN amplifier in inventory table
        for bladeEntityIndex in inventoryTable:
            bladeInv = inventoryTable[bladeEntityIndex]['inventoryUnitName']
            bladeIndexAid = entityTable[bladeEntityIndex]['entityIndexAid']
            if not bladeInv in componentModels:
                continue
            log.info('found Raman matching model %s' % bladeInv)
    
            # find ports from entityContainedIn for RAMAN entityIndex
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
            log.info('Found Raman %s port at: %s inventoryUnitName: %s',
                     self.portType,om.entityIndexAid, om.inventoryUnitName)

            rm.append(om)

        return rm


    def __findPort(self,log,parentEntityIndex,entityTable):
        parentEntityIndex = str(parentEntityIndex)
        for entityIndex in entityTable:
           entityContainedIn =str(entityTable[entityIndex]['entityContainedIn'])
           if entityContainedIn == parentEntityIndex:
               if entityTable[entityIndex]['entityIndexAid'].endswith(
                             self.portType):
                   return entityIndex,entityTable[entityIndex]['entityIndexAid']
               else:
                   i,a = self.__findPort(log,entityIndex,entityTable)
                   if i is not False:
                       return i,a
        return False, False
