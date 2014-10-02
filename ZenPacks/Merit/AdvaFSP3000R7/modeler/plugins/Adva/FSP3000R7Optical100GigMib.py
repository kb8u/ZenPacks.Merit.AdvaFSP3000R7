######################################################################
#
# FSP3000R7Optical100GigMib modeler plugin
#
######################################################################

__doc__="""Walk the OID for entityFacilityAidString and detect 100Gig
Muxponder optical side entities on network ports matching strings like
OTL-1-1-N-3."""

from pprint import pformat
import re

from Products.DataCollector.plugins.CollectorPlugin \
    import SnmpPlugin, GetTableMap, GetMap

class FSP3000R7Optical100GigMib(SnmpPlugin):

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Optical100Gig"
    relname = "FSP3000R7Optical100G"

    # The inventory table used by the other components does not include
    # the components this plugin is looking for.  Need to look at
    # entityFacilityAidString in entityFacilityTable for these

    snmpGetTableMaps = [GetTableMap('entityFacilityTable',
                                   '.1.3.6.1.4.1.2544.1.11.7.2.7.1',
                                   { '.6' : 'entityFacilityAidString' } )]

    def process(self, device, results, log):
        """process snmp information for components from this device"""
        log.info('processing %s for device %s', self.name(), device.id)

        getdata, tabledata = results

        log.debug('got results: %s', pformat(tabledata))

        # relationship mapping
        rm = self.relMap()

        for snmpIndex in tabledata['entityFacilityTable']:
            entityFacilityAidString = tabledata['entityFacilityTable']\
                                          [snmpIndex]['entityFacilityAidString']
            if re.match('OTL\-\d+\-\d+\-N\-\d$',entityFacilityAidString):
                om = self.objectMap()
                om.title = entityFacilityAidString
                om.id = self.prepId(entityFacilityAidString)
                om.snmpindex = snmpIndex

                rm.append(om)

        return rm
