######################################################################
#
# FSP3000R7AmplifierMib modeler plugin
#
# Copyright (C) 2011 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

__doc__="""FSP3000R7AmplifierMib

FSP3000R7AmplifierMib maps EDFA and RAMAN amplifiers on a FSP3000R7 system

"""

from ZenPacks.Merit.AdvaFSP3000R7.lib.FSP3000R7MibCommon import FSP3000R7MibCommon

class FSP3000R7AmplifierMib(FSP3000R7MibCommon):

    modname = "ZenPacks.Merit.AdvaFSP3000R7.FSP3000R7Amplifier"
    relname = "FSP3000R7Amp"

    # ADVA amplifier cards that will be detected by this modeler
    # They must respond to the same performance monitoring MIBs
    componentModels = [ 'EDFA-C-S10',
                        'EDFA-C-S18-GCB',
                        'EDFA-C-S18-GC',
                        'EDFA-C-S20-GCB',
                        'EDFA-C-D20-VGC',
                        'EDFA-C-D20-GC',
                        'EDFA-C-D17-GC',
                        'EDFA-L-D17-GC',
                        'EDFA-C-S20-GCB-DM',
                        'EDFA-C-D20-VGC-DM',
                        'EDFA-C-D20-VLGC-DM',
                        'EDFA-C-D27-GCB-DM',
                        'EDFA-C-S26-VGC-DM',
                        'EDFA-C-S26-VGCB-DM',
                        'AMP-S20H-C15',
                        'AMP-S20L-C15' ]
