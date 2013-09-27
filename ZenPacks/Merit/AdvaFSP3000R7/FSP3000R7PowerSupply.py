######################################################################
#
# FSP3000R7PowerSupply object class
#
# Copyright (C) 2011 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7PowerSupply

FSP3000R7PowerSupply is a component of a FSP3000R7Device Device
"""

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('FSP3000R7Amplifier')

class FSP3000R7PowerSupply(DeviceComponent, ManagedEntity, ZenPackPersistence):
    """FSP3000R7PowerSupply object"""

    portal_type = meta_type = 'FSP3000R7PowerSupply'

    # set default _properties
    EntityIndex           = -1
    inventoryUnitName     = 'Not set by modeler'
    entityIndexAid        = 'Not set by modeler'
    sortKey               = '000000000'
    entityAssignmentState = 'Not set by modeler'

    _properties = (
        # from ADVA inventory entityTable
        {'id':'EntityIndex',           'type':'int',    'mode':''},
        # from ADVA inventory MIB
        {'id':'inventoryUnitName',     'type':'string', 'mode':''},
        # human readable physical location of Amplifier in shelf
        {'id':'entityIndexAid',        'type':'string', 'mode':''},
        # string used to sort names in GUI
        {'id':'sortKey',               'type':'string', 'mode':''},
        )

    _relations = (("FSP3000R7Dev",
                   ToOne(ToManyCont,
                         "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Device",
                         "FSP3000R7PwrSupply")),
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
        else:
            return self.entityIndexAid

    # use viewName as titleOrId because that method is used to display a human
    # readable version of the object in the breadcrumbs
    titleOrId = name = viewName

    def primarySortKey(self):
        return self.entityIndexAid

    def device(self):
        return self.FSP3000R7Dev()

    # Power supplies can only be in a provisioned state
    def monitored(self):
        return True

    def manage_deleteComponent(self):
        self.getPrimaryParent()._delObject(self.id)


InitializeClass(FSP3000R7PowerSupply)
