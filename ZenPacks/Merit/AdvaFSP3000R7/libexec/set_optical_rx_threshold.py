#!/usr/bin/env python

################################################################################
#
# This program is part of the Adva FSP3000R7 Zenpack for Zenoss.
# Copyright (C) 2013 Russell Dwarshuis
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

usage = '''
Create rrd template local copy and/or update the threshold for receive
optical power on all transponders, amplifiers, ROADMs and OSCs so that they
will generate an Error level alert if the optical signal degrades 3 dB from
the current value.

set_optical_rx_threshold.py <device>
'''

import os
import sys
import re
import Globals
import subprocess
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from transaction import commit

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
                                             'FSP3000R7OSC' ]:
        continue
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
### BUG: next line throws exception (due to spaces in string & bug in library?)
### workaround is to get the value from the rrdfile with rrdtool
#    current = component.getRRDValue('Optical input power_Optical input power')
    rrdfile = os.environ['ZENHOME'] + '/perf/' + \
        component.getRRDFileName('Optical input power_Optical input power')
    sp = subprocess.Popen(['rrdtool','lastupdate', rrdfile],
                          stdout = subprocess.PIPE,
                          stderr = subprocess.PIPE)
    out,err = sp.communicate()
    if err:
        print '%s threshold not changed:' % component.id
        print 'rrd file is missing or too new. Try again in 10 minutes.'
        continue
    current = out.split()[-1]
    if current is None:
        print '%s threshold not changed:' % component.id
        print "Couldn't read value from rrd file."
        continue
    try:
        current = float(current)
    except ValueError:
        print '%s threshold not changed:' % component.id
        print "Couldn't read value from rrd file."
        continue

    new_minval = current - 30.0
    threshold.minval = str(new_minval)
    threshold.enabled = True

    commit()
    print 'Changed %s threshold to %.1f dBm' % \
                 (component.id,float(new_minval)/10)

print 'Command completed.'
