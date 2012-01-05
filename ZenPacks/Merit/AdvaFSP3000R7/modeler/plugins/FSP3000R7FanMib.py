#################################################################################
# Determine what shelf fans are in an Adva FSP3000R7 shelf
#
# Copyright (C) 2011 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""FSP3000R7FanMib

FSP3000R7FanMib maps shelf fans on an Adva FSP3000R7 system

"""

from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibCommon import FSP3000R7MibCommon

class FSP3000R7FanMib(FSP3000R7MibCommon):
    """Map Adva FSP3000R7 Shelf fan modules."""

    maptype  = "FSP3000R7FanMap"
    modname = "Products.ZenModel.Fan"
    relname  = "fans"
    compname = "hw"

    componentModels = [ 'FAN/9HU','FAN/PLUG-IN']
