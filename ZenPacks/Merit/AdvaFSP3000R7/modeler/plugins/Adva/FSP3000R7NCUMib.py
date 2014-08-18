######################################################################
#
# FSP3000R7NCUMib modeler pluginn
#
# Copyright (C) 2011 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7NCUMib

FSP3000R7NCUMib maps NCU amplifiers on a FSP3000R7 system

"""

from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibCommon import FSP3000R7MibCommon
from ZenPacks.Merit.AdvaFSP3000R7.lib.NCUModels import NCUModels

class FSP3000R7NCUMib(FSP3000R7MibCommon):

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7NCU"
    relname = "FSP3000R7Ncu"

    componentModels = NCUModels
