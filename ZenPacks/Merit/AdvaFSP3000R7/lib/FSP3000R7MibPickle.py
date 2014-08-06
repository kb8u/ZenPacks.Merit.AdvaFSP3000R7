import cPickle
import time

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
        log.debug('Could not open or read %s', cache_file_name)
        bad_cache = 1

    if bad_cache or cache_file_time < time.time() - 900:
        log.warn("Cached SNMP doesn't exist or is older than 15 minutes. You must include the modeler plugin FSP3000R7Device")
        return False, inventoryTable, entityTable, opticalIfDiagTable, containsModules

    if not inventoryTable:
        log.warn('No SNMP inventoryTable response from %s %s',
                 deviceId, modelerName)
        return False, inventoryTable, entityTable, opticalIfDiagTable, containsModules
    if not entityTable:
        log.warn('No SNMP entityTable response from %s for the %s plugin',
                 deviceId, modelerName)
        return False, inventoryTable, entityTable, opticalIfDiagTable, containsModules
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

    # dictionary of lists of what submodules are contained
    # in modules & submodules. Use strings to avoid key errors.
    containsModules = {}
    for entityIndex, entityContainedIn in entityTable.items():
        entityIndex_str = str(entityIndex)
        entityContainedIn_str = str(entityContainedIn['entityContainedIn'])
        if entityContainedIn_str not in containsModules:
            containsModules[entityContainedIn_str] = []
        containsModules[entityContainedIn_str].append(entityIndex_str)

    return True,inventoryTable,entityTable,opticalIfDiagTable,containsModules

