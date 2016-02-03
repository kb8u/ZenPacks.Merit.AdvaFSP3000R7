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

FSP3000R7DeviceMib gets System name from the NCU-II.  It creates a pickle
file with information needed by component modelers so the same information
does not have to be queried from the shelf over and over.  The Adva shelves
can respond very slowly and without this strategy zenoss can time out before
all the SNMP information is returned."""


from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
import cPickle
import time
import subprocess
from pprint import pformat


class FSP3000R7DeviceMib(PythonPlugin):
    """Use a PythonPlugin instead of SnmpPlugin since they run first in
       def collectDevice in /opt/zenoss/Products/DataCollector/zenmodeler.py
       Need that order so the pickle file will be created first."""

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Device"


    def copyDataToProxy(self, device, proxy):
        """add zSnmpCommunity to device proxy"""
        result = PythonPlugin.copyDataToProxy(self, device, proxy)
        proxy.zSnmpCommunity = device.zSnmpCommunity


    def collect(self, device, log):
        log.info('Starting to collect SNMP data using snmpget and snmpbulkwalk')
        # from the FspR7-MIB mib, neSystemId has the name of the system
        # and neSwVersion is the software version
        neSystemId = '.1.3.6.1.4.1.2544.1.11.2.2.1.1.0'
        neSwVersion = '.1.3.6.1.4.1.2544.1.11.2.2.1.5.0'

        inventoryUnitNameOID = '1.3.6.1.4.1.2544.2.5.5.1.1.1'
        entityContainedInOID = '1.3.6.1.4.1.2544.2.5.5.2.1.2'
        entityIndexAidOID = '1.3.6.1.4.1.2544.2.5.5.2.1.5'
        interfaceConfigIdentifierOID = '1.3.6.1.4.1.2544.1.11.2.4.3.1.1.1'
        entityAssignmentStateOID = '1.3.6.1.4.1.2544.2.5.5.2.1.7'
        entityEquipmentStateOID = '1.3.6.1.4.1.2544.2.5.5.2.1.8'
        opticalIfDiagInputPowerOID = '1.3.6.1.4.1.2544.1.11.2.4.3.5.1.3'

        getdata = {}
        
        self.__snmpget(device,neSystemId,'setHWTag',getdata)
        log.info('Got system name %s' % getdata['setHWTag'])
        self.__snmpget(device,neSwVersion,'setOSProductKey',getdata)
        log.info('Got software version %s' % getdata['setOSProductKey'])

        inventoryTable = {}
        raw_inventory = {}
        raw_inventory = self.__snmpgettable(device,inventoryUnitNameOID)
        self.__make_cacheable('inventoryUnitName',raw_inventory,inventoryTable)
        log.debug('inventoryTable: %s' % pformat(inventoryTable))

        entityTable = {}
        raw_entityContainedIn = {}
        raw_entityContainedIn = self.__snmpgettable(device,entityContainedInOID)
        self.__make_cacheable('entityContainedIn',
                              raw_entityContainedIn,
                              entityTable)

        raw_entityIndexAid = {}
        raw_entityIndexAid = self.__snmpgettable(device,entityIndexAidOID)
        self.__make_cacheable('entityIndexAid',
                              raw_entityIndexAid,
                              entityTable)

        raw_interfaceConfigIdentifier = {}
        raw_interfaceConfigIdentifier = \
          self.__snmpgettable(device,interfaceConfigIdentifierOID)
        self.__make_cacheable('interfaceConfigIdentifier',
                              raw_interfaceConfigIdentifier,
                              entityTable)

        raw_entityAssignmentState = {}
        raw_entityAssignmentState = self.__snmpgettable(device,
                                                       entityAssignmentStateOID)
        self.__make_cacheable('entityAssignmentState',
                              raw_entityAssignmentState,
                              entityTable)

        raw_entityEquipmentState = {}
        raw_entityEquipmentState = self.__snmpgettable(device,
                                                       entityEquipmentStateOID)
        self.__make_cacheable('entityEquipmentState',
                              raw_entityEquipmentState,
                              entityTable)
        log.debug('entityTable: %s' % pformat(entityTable))

        opticalIfDiagTable = {}
        raw_opticalIfDiagInputPower = {}
        raw_opticalIfDiagInputPower= self.__snmpgettable(device,
                                                     opticalIfDiagInputPowerOID)
        self.__make_cacheable('opticalIfDiagInputPower',
                              raw_opticalIfDiagInputPower,
                              opticalIfDiagTable)
        # sometimes Avda shelves give bogus -65535 input power readings for
        # components that really do have input power readings when you do a
        # specific snmpget on them.
        for index, opr_dict in opticalIfDiagTable.items():
            try:
                if opr_dict['opticalIfDiagInputPower'] == -65535:
                    oid = opticalIfDiagInputPowerOID + '.' + index
                    w = {}
                    self.__snmpget(device,oid,'opr',w)
                    opticalIfDiagTable[index] = \
                            { 'opticalIfDiagInputPower' : int(w['opr']) }
            except (KeyError, ValueError):
                pass
        log.debug('opticalIfDiagTable: %s' % pformat(opticalIfDiagTable))

        cache_file_name = '/tmp/%s.Adva_inventory_SNMP.pickle' % device.id
        try:
            cache_file = open(cache_file_name,'w')
            cPickle.dump(inventoryTable,cache_file)
            cPickle.dump(entityTable,cache_file)
            cPickle.dump(opticalIfDiagTable,cache_file)
            cPickle.dump(time.time(),cache_file)
            cache_file.close()
        except IOError,cPickle.PickleError:
            log.warn("Couldn't cache SNMP data in", cache_file_name)

        return getdata


    def process(self, device, results, log):
        """Set the system name and software version"""

        log.debug('in process, got results:',results)
        rm = self.relMap()
        om = self.objectMap(results)
        return om


    def __snmpget(self,device,oid,oid_name,results):
        cmd = ['snmpget','-v2c','-t','3',
               '-c',device.zSnmpCommunity, '-Onq', device.manageIp,oid]
        try:
            results[oid_name] = \
                subprocess.check_output(cmd).split(' ')[1].strip('\n"')
        except subprocess.CalledProcessError, IndexError:
            results[oid_name] = ''


    def __snmpgettable(self,device,oid):
        """Use snmpbulkwalk to get data.  Use timeout of 5 seconds since
           shelves can be very slow to respond"""
        cmd = ['snmpbulkwalk','-v2c','-t','5',
               '-c',device.zSnmpCommunity, '-Onq', device.manageIp,oid]
        results = {}
        try:
            walk_output = subprocess.check_output(cmd).split('\n')
            for line in walk_output:
                try:
                    oid,val = line.split(' ',1)
                    oid = oid.lstrip('.')
                    val = val.strip('"')
                except ValueError:
                    continue
                try:
                    val = int(val)
                except ValueError:
                    pass
                results[oid] = val
        except subprocess.CalledProcessError, IndexError:
            pass
        return results


    def __make_cacheable(self,name,raw,results):
        for oid,val in raw.items():
            index = oid.split('.')[-1]
            if index not in results:
                results[index] = {}
            results[index][name] = val
