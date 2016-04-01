#!/usr/bin/env python

################################################################################
#
# This program is part of the Adva FSP150CC Zenpack for Zenoss.
# Copyright (C) 2015 Russell Dwarshuis
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

usage = '''
Create rrd template local copy and/or update the threshold for receive
optical power on all applicable Adva components so that they will generate an
Error level alert if the optical signal degrades 3 dB from the current value.

set_optical_rx_threshold.py <device>
'''

import os
import sys
import re
import Globals
import subprocess
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from transaction import commit

# allow this many dB loss from initial OPR
lossmargin = 3

dmd = ZenScriptBase(connect=True).dmd

# find device on command line (either IP or device id will work)
if len(sys.argv) < 2:
    print usage
    print 'Error: no device specified on command line'
    sys.exit()

device = dmd.Devices.findDevice(sys.argv[1])

if device is None:
    print usage
    print 'Error: Device not found.'
    sys.exit()

for component in device.getMonitoredComponents():
    if component.__class__.__name__ not in [ 'FSP3000R7Roadm',
                                             'FSP3000R7Amplifier',
                                             'FSP3000R7Transponder',
                                             'FSP3000R7OSC',
                                             'FSP150NetPort' ]:
        continue

    # 3000R7 uses centibels, 150CC uses decibels, datapoint is named differently
    if component.__class__.__name__ == 'FSP150NetPort':
        opr_dp = 'cmEthernetNetPortStatsOPR'
        scale = 1
    else:
        opr_dp = 'Optical input power'
        scale = 10

    # don't set thresholds on containers
    if re.search('^MOD-\d',component.id,flags=re.IGNORECASE):
        continue
    component.makeLocalRRDTemplate(component.__class__.__name__)
    template = component.getRRDTemplateByName(component.__class__.__name__)
    if template is None:
        continue

    # find 'Low optical input power' threshold or continue to next component
    thresholds = template.thresholds()
    if len(thresholds) == 0:
        continue
    for threshold in thresholds:
        if threshold.id == 'Low optical input power':
            break
    if threshold.id != 'Low optical input power':
        continue

    # get current value from rrd
### BUG: next line throws exception if there's spaces in string
### See bug fix in RenderServer.py in to_install directory
    current = component.getRRDValue(opr_dp)
    if str(current) == 'nan' or current is None:
        print '%s threshold not changed:' % component.id
        print "Couldn't read value from rrd file."
        continue

    new_minval = current - lossmargin * scale
    threshold.minval = str(new_minval)
    threshold.enabled = True

    commit()
    print 'Changed %s threshold to %.1f dBm' % \
                 (component.id,float(new_minval)/scale)

print 'Command completed.'
