######################################################################
#
# FSP3000R7RamanUPortMib modeler plugin
#
# Copyright (C) 2014 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7RamanUPortMib

FSP3000R7RamanUPortMib maps RAMAN amplifier Upgrade ports on a FSP3000R7 system

"""

from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7RamanMib import FSP3000R7RamanPortMib


class FSP3000R7RamanUPortMib(FSP3000R7RamanPortMib):
    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7RamanUPort"
    relname = "FSP3000R7RamanUPort"

    portType = '-U'
