######################################################################
#
# FSP3000R7Optical100Gig object class
#
# Copyright (C) 2014 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7Optical100Gig

FSP3000R7Optical100Gig is a 100 Gig Muxponder Optical component of a
FSP3000R7Device Device.  It models the 4 network side optical components
in a 100 Gig muxponder.

"""

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('FSP3000R7Optical100Gig')

class FSP3000R7Optical100Gig(DeviceComponent,ManagedEntity,ZenPackPersistence):
    """FSP3000R7Optical100Gig object"""

    portal_type = meta_type = 'FSP3000R7Optical100Gig'

    _relations = (("FSP3000R7Dev",
                   ToOne(ToManyCont,
                         "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Device",
                         "FSP3000R7Optical100G")),
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
        return(self.id)

    name = viewName

    def device(self):
        return self.FSP3000R7Dev()

    def monitored(self):
        return True

    def manage_deleteComponent(self):
        self.getPrimaryParent()._delObject(self.id)


InitializeClass(FSP3000R7Optical100Gig)
