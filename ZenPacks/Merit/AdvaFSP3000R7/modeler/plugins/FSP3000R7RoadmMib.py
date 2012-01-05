######################################################################
#
# FSP3000R7RoadmMib modeler pluginn
#
# Copyright (C) 2011 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7RoadmMib

FSP3000R7RoadmMib maps ROADMs on a FSP3000R7 system

"""

from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibCommon import FSP3000R7MibCommon

class FSP3000R7RoadmMib(FSP3000R7MibCommon):

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Roadm"
    relname = "FSP3000R7Road"

    componentModels = [ 'ROADM-C40/40/OPM-3HU/2DC',
                        'ROADM-C80/0/OPM',
                        '8ROADM-C40/0/OPM',
                        '8ROADM-C80/0/OPM',
                        'CCM-C40/8',
                        '4-OPCM' ]
