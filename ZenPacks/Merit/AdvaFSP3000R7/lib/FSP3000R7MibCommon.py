######################################################################
#
# FSP3000R7MibCommon modeler plugin
#
######################################################################

__doc__="""FSP3000R7MibCommon

FSP3000R7MibCommon is a modeler base class to find components on an
Adva FSP3000R7 system. It uses stored SNMP data from an Adva system in a
file in /tmp so if there is more than one component to be modeled, the
subsequent components will not have to get the same information over and over.
Without this, a system may respond so slowly that modeling times out in
Zenoss.  The stored SNMP data is created by the Adva device modeler which
must be run first."""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7Channels import Channels
import cPickle
import time
import os


# Use SNMP data from Device Modeler in a cache file.  Can't be a PythonPlugin
# since those run before any SnmpPlugin; device modeler is an PythonPlugin so
# the cache file will be created before this is run.
class FSP3000R7MibCommon(SnmpPlugin):

    # FspR7-MIB mib neSystemId is .1.3.6.1.4.1.2544.1.11.2.2.1.1.0.  Not used;
    # Have to get something with SNMP or modeler won't process
    snmpGetMap = GetMap({'.1.3.6.1.4.1.2544.1.11.2.2.1.1.0' : 'setHWTag'})


    def process(self, device, results, log):
        """process snmp information for components from this device"""
        log.info('processing %s for device %s', self.name(), device.id)

        # tabledata is not used (get tables from cache pickle file created
        # in FSP3000R7Device modeler)
        getdata = {}
        getdata['setHWTag'] = False
        getdata, tabledata = results
        if not getdata['setHWTag']:
            log.info("Couldn't get system name from Adva shelf.")

        cache_file_name = '/tmp/%s.Adva_inventory_SNMP.pickle' % device.id

        inventoryTable = entityTable = opticalIfDiagTable = False
        cache_file_time = 0

        bad_cache = 0

        try:
            cache_file = open(cache_file_name, 'r')
            inventoryTable = cPickle.load(cache_file)
            entityTable = cPickle.load(cache_file)
            opticalIfDiagTable = cPickle.load(cache_file)
            cache_file_time = cPickle.load(cache_file)
            cache_file.close()
        except IOError,cPickle.PickleError:
            log.debug('Could not open or read %s', cache_file_name)
            bad_cache = 1

        if bad_cache or cache_file_time < time.time() - 900:
            log.warn("Cached SNMP doesn't exist or is older than 15 minutes. You must include the modeler plugin FSP3000R7Device")
            return

        if not inventoryTable:
            log.warn('No SNMP inventoryTable response from %s for %s',
                     device.id, self.name())
            return;
        if not entityTable:
            log.warn('No SNMP entityTable response from %s for the %s plugin',
                     device.id, self.name())
            return;
        else:
            log.debug('SNMP entityTable and inventoryTable responses received')
        # not all modules will respond to opticalIfDiagTable so don't return
        if not opticalIfDiagTable:
            log.warn(
              'No SNMP opticalIfDiagTable response from %s for the %s plugin',
              device.id, self.name())
        else:
            log.debug(
                'SNMP opticalIfDiagTable and inventoryTable responses received')

        # dictionary of lists of what submodules are contained
        # in modules & submodules. Use strings to avoid key errors.
        containsModules = {}
        for entityIndex, entityContainedIn in entityTable.items():
            entityIndex_str = str(entityIndex)
            entityContainedIn_str = str(entityContainedIn['entityContainedIn'])
            if entityContainedIn_str not in containsModules:
                containsModules[entityContainedIn_str] = []
            containsModules[entityContainedIn_str].append(entityIndex_str)

        # relationship mapping
        rm = self.relMap()

        for entityIndex, inventoryUnitName in inventoryTable.items():
            entityIndex_str = str(entityIndex)
            if self.__model_match(inventoryUnitName['inventoryUnitName'],
                            self.componentModels) \
              and entityIndex in entityTable \
              and 'entityAssignmentState' in entityTable[entityIndex] \
              and 'entityEquipmentState' in entityTable[entityIndex] \
              and entityTable[entityIndex]['entityAssignmentState'] == 1 \
              and entityTable[entityIndex]['entityEquipmentState'] == 1:
                om = self.objectMap()
                om.EntityIndex = int(entityIndex)
                om.inventoryUnitName = inventoryUnitName['inventoryUnitName']
                if 'interfaceConfigIdentifier' in entityTable[entityIndex]:
                    om.interfaceConfigId = \
                        entityTable[entityIndex]['interfaceConfigIdentifier']
                om.entityIndexAid = entityTable[entityIndex]['entityIndexAid']
                om.sortKey = self.__make_sort_key(om.entityIndexAid)
                om.entityAssignmentState = \
                    entityTable[entityIndex]['entityAssignmentState']
                om.id = self.prepId(om.entityIndexAid)
                om.title = om.entityIndexAid
                om.snmpindex = int(entityIndex)
                log.info('Found component at: %s inventoryUnitName: %s',
                         om.entityIndexAid, om.inventoryUnitName)

                rm.append(om)

                # Now find sub-organizers that respond to OPR
                if not opticalIfDiagTable:
                    continue
                if entityIndex_str not in containsModules:
                    continue
                # EntityIndex's with valid responses to opticalIfDiagTable
                opr_responders = []
                self.__get_opr_responders(opr_responders,
                                          entityIndex_str,
                                          containsModules,
                                          opticalIfDiagTable)

                for entityIndex in opr_responders:
                    # skip non-production components. entityEquipmentState is 0
                    # (undefined) for sub-organizers so don't check it here.
                    if not (entityIndex in entityTable \
                      and 'entityAssignmentState' in entityTable[entityIndex] \
                      and entityTable[entityIndex]['entityAssignmentState']==1):
                        continue;
                    om = self.objectMap()
                    om.EntityIndex = int(entityIndex)
                    if entityIndex in inventoryUnitName:
                        om.inventoryUnitName = \
                            inventoryUnitName[entityIndex]['inventoryUnitName']
                    else:
                        om.inventoryUnitName = 'Subsystem'
                    if 'interfaceConfigIdentifier' in entityTable[entityIndex]:
                        om.interfaceConfigId = \
                           entityTable[entityIndex]['interfaceConfigIdentifier']
                    om.entityIndexAid=entityTable[entityIndex]['entityIndexAid']
                    om.sortKey = self.__make_sort_key(om.entityIndexAid)
                    om.entityAssignmentState = \
                        entityTable[entityIndex]['entityAssignmentState']
                    om.id = self.prepId(om.entityIndexAid)
                    om.title = om.entityIndexAid
                    om.snmpindex = int(entityIndex)
                    log.info('Found component at: %s inventoryUnitName: %s',
                             om.entityIndexAid, om.inventoryUnitName)

                    rm.append(om)

        return rm

    def __model_match(self,inventoryUnitName,componentModels):
        for model in componentModels:
            # Test different channel variations if there's a # on end
            if model.endswith('#'):
                all_ch = Channels.dwdm_old_channels+Channels.cwdm_channels
                for ch in all_ch:
                    model_var = model + ch
                    if inventoryUnitName == model_var:
                        return True
            if inventoryUnitName == model:
                return True
        return False


    def __get_opr_responders(self,
                             opr_responders,
                             entityIndex_str,
                             containsModules,
                             opticalIfDiagTable):
        """recursively walk containsModules looking for matches in opticalIfDiagTable"""
        if entityIndex_str not in containsModules:
            return
        for entityIndex2 in containsModules[entityIndex_str]:
            if entityIndex2 in opticalIfDiagTable:
                # MIB says value of -65535 means not available or invalid
                if opticalIfDiagTable[entityIndex2]['opticalIfDiagInputPower'] != -65535:
                    opr_responders.append(entityIndex2)
            self.__get_opr_responders(opr_responders,
                                      entityIndex2,
                                      containsModules,
                                      opticalIfDiagTable)


    def __make_sort_key(self,entityIndexAid):
        """Return a string to sort on, e.g. 'MOD-1-3' -> '001003000000'
and 'VCH-1-7-N1' -> ' 1 7VCH N1'"""
        a = entityIndexAid.split('-',4)
        if len(a) < 3:
            return '000000000'
        if entityIndexAid.startswith('MOD-') or entityIndexAid.startswith('FAN-'):
            return "%03s%03s000000" % (a[1],a[2])
        return "%03s%03s%03s%03s" % (a[1],a[2],a[0],a[3])
