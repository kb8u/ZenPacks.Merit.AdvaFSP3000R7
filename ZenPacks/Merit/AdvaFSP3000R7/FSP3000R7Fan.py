######################################################################
#
# FSP3000R7Fan object class
#
# Copyright (C) 2013 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7Fan

FSP3000R7Fan is a component of a FSP3000R7Device Device

"""

from Globals import InitializeClass
from Products.ZenModel.Fan import Fan

import logging
log = logging.getLogger('FSP3000R7Fan')

class FSP3000R7Fan(Fan):
    """FSP3000R7Fan object"""

    portal_type = meta_type = 'FSP3000R7Fan'

    def manage_deleteComponent(self):
        self.getPrimaryParent()._delObject(self.id)

InitializeClass(FSP3000R7Fan)
