######################################################################
#
# FSP3000R7Component object class
#
# Copyright (C) 2014 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7Component

FSP3000R7Component is a base class for components of a FSP3000R7Device Device.
Override: portal_type = meta_type = 'FSP3000R7Component'
          _relations = ....
          InitializeClass(FSP3000R7Component)

"""

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity


class FSP3000R7Component(DeviceComponent, ManagedEntity, ZenPackPersistence):
    """FSP3000R7Component object"""

    # override this in subclass
    portal_type = meta_type = 'FSP3000R7Component'

    # set default _properties
    EntityIndex           = -1
    inventoryUnitName     = 'Not set by modeler'
    entityIndexAid        = 'Not set by modeler'
    interfaceConfigId     = ''
    sortKey               = '000000000'
    entityAssignmentState = 'Not set by modeler'

    _properties = (
        # from ADVA inventory entityTable
        {'id':'EntityIndex',           'type':'int',    'mode':''},
        # from ADVA inventory MIB
        {'id':'inventoryUnitName',     'type':'string', 'mode':''},
        # human readable physical location of Component in shelf
        {'id':'entityIndexAid',        'type':'string', 'mode':''},
        # link comments (interfaceConfigIdentifier)
        {'id':'interfaceConfigId',     'type':'string', 'mode':''},
        # string used to sort names in GUI
        {'id':'sortKey',               'type':'string', 'mode':''},
        {'id':'entityAssignmentState', 'type':'string', 'mode':''},
        )

    factory_type_information = ({
        'actions': ({
            'id': 'perfConf',
            'name': 'Template',
            'action': 'objTemplates',
            'permissions': (ZEN_CHANGE_DEVICE,),
            },),
        },)

    isUserCreatedFlag = True

    def isUserCreated(self):
        """
        Returns the value of isUserCreated. True adds SAVE & CANCEL buttons to Details menu
        """
        return self.isUserCreatedFlag

    def viewName(self):
        """Human readable version of this object"""
        if self.inventoryUnitName == 'Not set by modeler' or self.EntityIndex == '-1':
            return "Unknown"
        return(self.entityIndexAid)

    name = viewName

    def primarySortKey(self):
        return self.sortKey

    def device(self):
        return self.FSP3000R7Dev()

    def manage_deleteComponent(self):
        self.getPrimaryParent()._delObject(self.id)
