#################################################################################
# Determine what power supplies are in an Adva FSP3000R7 shelf
#
# Copyright (C) 2011 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""FSP3000R7PowerSupplyMib

FSP3000R7PowerSupplyMib maps power supplies on an Adva FSP3000R7 system

"""

from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibCommon import FSP3000R7MibCommon
from ZenPacks.Merit.AdvaFSP3000R7.lib.PowerSupplyModels import PowerSupplyModels

class FSP3000R7PowerSupplyMib(FSP3000R7MibCommon):
    """Map Adva FSP3000R7 Shelf power supply modules."""

    modname  = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7PowerSupply"
    relname  = "FSP3000R7PwrSupply"

    componentModels = PowerSupplyModels
