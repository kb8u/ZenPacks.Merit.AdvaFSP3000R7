######################################################################
#
# FSP3000R7Module object class
#
# Copyright (C) 2014 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7Module

FSP3000R7Module is a component of a FSP3000R7Device Device
that contains other components.  It corresponds to a card that has sub
components, e.g. an amplifier card having different stages that report
separately.
"""

from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7Component import *

import logging
log = logging.getLogger('FSP3000R7Module')

class FSP3000R7Module(FSP3000R7Component):
    """FSP3000R7Module object"""

    portal_type = meta_type = 'FSP3000R7Module'

    _relations = (("FSP3000R7Dev",
                   ToOne(ToManyCont,
                         "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Device",
                         "FSP3000R7Mod")),)


InitializeClass(FSP3000R7Module)
