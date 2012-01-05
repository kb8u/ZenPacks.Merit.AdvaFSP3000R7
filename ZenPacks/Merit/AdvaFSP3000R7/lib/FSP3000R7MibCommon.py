######################################################################
#
# FSP3000R7MibCommon modeler plugin
#
######################################################################

__doc__="""FSP3000R7MibCommon

FSP3000R7MibCommon is a modeler base class to find components on an
Adva FSP3000R7 system.  

"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap
from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7Channels import Channels

class FSP3000R7MibCommon(SnmpPlugin):

    weight = 4

    inventoryTablecolumns = { '.1.1.': 'inventoryUnitName' }

    entityTablecolumns = {
        '.1.2.': 'entityContainedIn',
        '.1.5.': 'entityIndexAid',
        '.1.7.': 'entityAssignmentState',
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
        """collect snmp information for components from this device"""
        log.info('processing %s for device %s', self.name(), device.id)

        getdata, tabledata = results
        inventoryTable     = tabledata.get('inventoryTableEntry')
        entityTable        = tabledata.get('entityTableEntry')
        opticalIfDiagTable = tabledata.get('opticalIfDiagTableEntry')

        if not inventoryTable:
            log.warn( 'No SNMP inventoryTable response from %s for the %s plugin', device.id, self.name() )
            return;
        if not entityTable:
            log.warn( 'No SNMP entityTable response from %s for the %s plugin', device.id, self.name() )
            return;
        else:
            log.debug('SNMP entityTable and inventoryTable responses received')
        # not all modules will respond to opticalIfDiagTable so don't return 
        if not opticalIfDiagTable:
            log.warn( 'No SNMP opticalIfDiagTable response from %s for the %s plugin', device.id, self.name() )
        else:
            log.debug('SNMP opticalIfDiagTable and inventoryTable responses received')

        # dictionary of lists of what submodules are contained
        # in modules & submodules.  Use strings to avoid key errors.
        containsModules = {}
        for entityIndex, entityContainedIn in entityTable.items():
            entityIndex_str       = str(entityIndex)
            entityContainedIn_str = str(entityContainedIn['entityContainedIn'])
            if entityContainedIn_str not in containsModules:
                containsModules[entityContainedIn_str] = []
            containsModules[entityContainedIn_str].append(entityIndex_str)

        # relationship mapping
        rm = self.relMap()

        for entityIndex, inventoryUnitName in inventoryTable.items():
            entityIndex_str = str(entityIndex)
            if self.__model_match(inventoryUnitName['inventoryUnitName'],
                            self.componentModels):
                om = self.objectMap()
                om.EntityIndex = int(entityIndex)
                om.inventoryUnitName = inventoryUnitName['inventoryUnitName']
                om.entityIndexAid = entityTable[entityIndex]['entityIndexAid']
                om.sortKey = self.__make_sort_key(om.entityIndexAid)
                om.entityAssignmentState = entityTable[entityIndex]['entityAssignmentState']
                om.id = self.prepId(om.entityIndexAid)
                om.title = om.entityIndexAid
                om.snmpindex = int(entityIndex)
                log.info('Found component at: %s inventoryUnitName: %s',om.entityIndexAid, om.inventoryUnitName)

                rm.append(om)

                # Now find sub-organizers that respond to OPR
                if not opticalIfDiagTable:
                  continue
                if entityIndex_str not in containsModules:
                  continue
                # EntityIndex's with valid responses to opticalIfDiagTable
                opr_responders = []
                self.__get_opr_responders(opr_responders,entityIndex_str,containsModules,opticalIfDiagTable)

                for entityIndex in opr_responders:
                  om = self.objectMap()
                  om.EntityIndex = int(entityIndex)
                  if entityIndex in inventoryUnitName:
                    om.inventoryUnitName = inventoryUnitName[entityIndex]['inventoryUnitName']
                  else:
                    om.inventoryUnitName = 'Subsystem'
                  om.entityIndexAid = entityTable[entityIndex]['entityIndexAid']
                  om.sortKey = self.__make_sort_key(om.entityIndexAid)
                  om.entityAssignmentState = entityTable[entityIndex]['entityAssignmentState']
                  om.id = self.prepId(om.entityIndexAid)
                  om.title = om.entityIndexAid
                  om.snmpindex = int(entityIndex)
                  log.info('Found component at: %s inventoryUnitName: %s',om.entityIndexAid, om.inventoryUnitName)

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


    def __get_opr_responders(self,opr_responders,entityIndex_str,containsModules,opticalIfDiagTable):
        """recursively walk containsModules looking for matches in opticalIfDiagTable"""
        if entityIndex_str not in containsModules:
            return
        for entityIndex2 in containsModules[entityIndex_str]:
            if entityIndex2 in opticalIfDiagTable:
                # MIB says value of -65535 means not available or invalid
                if opticalIfDiagTable[entityIndex2]['opticalIfDiagInputPower'] != -65535:
                    opr_responders.append(entityIndex2)
            self.__get_opr_responders(opr_responders,entityIndex2,containsModules,opticalIfDiagTable)


    def __make_sort_key(self,entityIndexAid):
        """Return a string to sort on, e.g. 'MOD-1-3' -> '001003000000'
and 'VCH-1-7-N1' -> '  1  7VCH N1'"""
        a = entityIndexAid.split('-',4)
        if len(a) < 3:
            return '000000000'
        if entityIndexAid.startswith('MOD-'):
            return "%03s%03s000000" % (a[1],a[2])
        return "%03s%03s%03s%03s" % (a[1],a[2],a[0],a[3])
