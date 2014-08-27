import cPickle
import time
from pprint import pformat

def getCache (deviceId, modelerName, log):
    cache_file_name = '/tmp/%s.Adva_inventory_SNMP.pickle' % deviceId

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
        log.info('Could not open or read %s', cache_file_name)
        bad_cache = 1

    if bad_cache or cache_file_time < time.time() - 900:
        log.warn("Cached SNMP doesn't exist or is older than 15 minutes. You must include the modeler plugin FSP3000R7Device")
        return False, inventoryTable, entityTable, opticalIfDiagTable, containsOPRModules

    if not inventoryTable:
        log.warn('No SNMP inventoryTable response from %s %s',
                 deviceId, modelerName)
        return False, inventoryTable, entityTable, opticalIfDiagTable, containsOPRModules
    if not entityTable:
        log.warn('No SNMP entityTable response from %s for the %s plugin',
                 deviceId, modelerName)
        return False, inventoryTable, entityTable, opticalIfDiagTable, containsOPRModules
    else:
        log.debug('SNMP entityTable and inventoryTable responses received')
    # not all modules will respond to opticalIfDiagTable so don't return False
    if not opticalIfDiagTable:
        log.warn(
          'No SNMP opticalIfDiagTable response from %s for the %s plugin',
          deviceId, modelerName)
    else:
        log.debug(
            'SNMP opticalIfDiagTable and inventoryTable responses received')

    # dictionary of lists of what modules or submodules contain
    # submodules that respond to OPR
    containsOPRModules = {}
    if opticalIfDiagTable:
        for entityIndex in opticalIfDiagTable:
            if 'opticalIfDiagInputPower' not in opticalIfDiagTable[entityIndex]:
                continue
            # MIB says value of -65535 means not available or invalid
            if opticalIfDiagTable[entityIndex]['opticalIfDiagInputPower'] == \
                 -65535:
                continue
            # create entry for the OPR responding module inself
            containsOPRModules[entityTable[entityIndex]['entityIndexAid']] = \
                 [entityIndex]
            # create entry for the immediate parent or append
            parentIndex = str(entityTable[entityIndex]['entityContainedIn'])
            parentIndexAid = entityTable[parentIndex]['entityIndexAid']
            if parentIndexAid not in containsOPRModules:
                containsOPRModules[parentIndexAid] = [entityIndex]
            else:
                containsOPRModules[parentIndexAid].append(entityIndex)
            # create entry for all parents above immediate parent
            while(parentIndex):
                parentIndex = __get_parent(log,parentIndex,entityTable)
                if not parentIndex:
                    break
                parentIndexAid = entityTable[parentIndex]['entityIndexAid']
                if parentIndexAid not in containsOPRModules:
                    containsOPRModules[parentIndexAid] = [entityIndex]
                else:
                    containsOPRModules[parentIndexAid].append(entityIndex)

    return True,inventoryTable,entityTable,opticalIfDiagTable,containsOPRModules


def __get_parent(log,childIndex,entityTable):
    if not childIndex in entityTable:
        return False
    if not 'entityContainedIn' in entityTable[childIndex]:
        return False
    if entityTable[childIndex]['entityContainedIn'] == 0:
        return False
    return str(entityTable[childIndex]['entityContainedIn'])
