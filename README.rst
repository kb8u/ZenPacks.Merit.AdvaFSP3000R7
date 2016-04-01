============================
ZenPacks.Merit.AdvaFSP3000R7
============================

.. contents::

Description
===========
Provides monitoring of FSP3000R7 optical transport systems manufactured by Adva
Optical Networking in Zenoss.

This is a subset of the functionality provided by Adva's proprietary FSP Network
Manager.  Most alerts are implemented and optical signal strength
is graphed.  Most blade types will be detected when modeling a system.  The five
severity levels used in Adva's FSP Network Manager are mapped to the five
severity levels in Zenoss.

Also included is a script to set a threshold for monitoring of receive optical
signal levels 3 dBm below the current value.

Zenpack contents
================
The ZenPack has the following:

/Network/Adva Device Class
--------------------------
* The device overview page has the system name in the Tag field, and the software version number in the OS Model field.

Component modeling
------------------
Modelers detect most blade and pluggable optical hardware types:

* Power Supply

  * Component template graphs current

* Optical Amplifier

  * Component template graphs Laser bias current, Optical Power received and transmitted when it's available.

* Raman Amplifier network and upgrade ports

  * Component template graphs optical power transmit, estimated signal gain, OSC gain, back reflection, OSC power received and Raman pump power

* NCU-II (shelf controller card)

* Transponder Component Modeling

  * Component template graphs Laser bias current, Optical Power received, bits/secnod, packets/second and ethernet errors/second.

* 100 Gigabit/s Transponder Network, Upgrade and optical component modeling

  * Component templates for FEC uncorrected blocks, FEC corrected errors, BER before FEC and Logical lanes, and optical power received on the 4 lanes.

* Optical Service Channel Component Modeling

  * Component template graphs Laser bias current, Optical Power received and transmitted when it's available.

* Fan Component Modeling

* Blade Modeling

  * Model number for each blade in a system

Adva MIBs
---------
Adva Optical Networking vendor MIBs

* ADVA-MIB
* FspR7-LAYER2-MIB
* FspR7-MIB

Event Class mapping
-------------------

* Well over two hundred Event Class Mappings for Adva SNMP traps in sensible event classes.
* Event severities match Adva's levels

Command
------

- update_Adva_OPR_threshold
Create rrd template local copy and/or update the threshold for receive
optical power on amplifiers, transponders, OSCs and ROADMs so that they will
generate an Error level alert if the optical signal degrades 3 dB from
the current value.

Requirements
============

* Zenoss Versions Supported: 4.0+
* External Dependencies: None
* ZenPack Dependencies: None
* Configuration: No Special configuration should be necessary.

Installation
============
Normal Installation (packaged egg)

*NOTE* This version requires a modified version of SnmpPerformanceConfig.py
be copied to $ZENHOME/Products/ZenHub/services/ from the to_install directory
of this Zenpack.  The modified version allows SNMP indexes to be at places
other than the end of on OID.  As the zenoss user, copy the file before
restarting zenoss or the zenoss daemons.  Also, the update_Adva_OPR_threshold
command will not work unless a bug fix in RenderServer.py is installed in
$ZENHOME/Products/ZenRRD

This is a large zenpack due to the size of the Adva MIB files included.
Installation from the Zenoss web interface may fail on especially slow systems
due to time out issues.  If this happens, try installing from the command line:

Download the appropriate package for your Zenoss version from the Zenoss
Zenpack site:

* Zenoss 4.0+ `Latest Package`_
  
Then copy it to your Zenoss server and run the following commands as the zenoss
user::

    zenpack --install <package.egg>
    cp $ZENHOME/ZenPacks/<package.egg>/to_install/SnmpPerformanceConfig.py $ZENHOME/Products/ZenHub/services
    cp $ZENHOME/ZenPacks/<package.egg>/to_install/RenderServer.py $ZENHOME/Products/ZenRRD
    zenoss restart
    
If you don't want to do a full restart, you should be able to just restart
zenhub, zenperfsnmp and zopectl::

    zenhub restart && zenperfsnmp restart &&  zopectl restart
   
Developer Installation (link mode)
----------------------------------
If you wish to further develop and possibly contribute back to this
ZenPack you should clone the git repository, then install the ZenPack in
developer mode using the following commands::

    git clone git://github.com/kb8u/zenoss/ZenPacks.Merit.AdvaFSP3000R7
    zenpack --link --install ZenPacks.Merit.AdvaFSP3000R7
    zenoss restart
    
Change History
==============

* 1.0

  * Initial Release

* 1.1

  * Removed Serial number from overview.  It was the database serial number.

  * Added system name to Tag field in overview.

  * Device modeler FSP3000R7Mib now caches SNMP responses to a file in /tmp
    to work around Zeonss timeout problems with slow SNMP responses from
    large Adva systems.

  * Removed FSP3000R7Roadm performance template from device organizer
    performance template.

* 1.2

  * Added ethernets statistics.  Note that these are for the prior 15 minute
    interval.

  * Added Adva entityStateOper checking and /Status/Adva event class

* 1.3

  * Fixed bug that caused modelers to fail when opticalIfDiagTable is empty

* 1.4

  * Fixed bug that prevented components from being deleted

* 1.5

  * Only adds components that are provisioned

* 1.6

  * Added modeling of new hardware (e.g. 100Gig).  Added threshold setting
    command.

* 1.7

  * Fixed bugs with component templates showing up twice, fan components not
    deleting through GUI in Zenoss 4.3.2

* 1.8

  * Added comments configured on components to GUI

* 1.9

  * Added Raman amplifiers and Blades.  Removed blades from other components.

* 1.10

  * Added 100 Gig Transponder components.  Removed commands to get SNMP
    statistics where index is not at the end of the OID

* 1.12

  * Changed modeler to retry bogus optical power receive recadings with
    snmpget.

* 1.13

  * Changed update_Adva_OPR_threshold to work on both FSP3000R7 and FSP150CC
    models.  Fixed bug in RenderServer.py so the command will work on devices
    on remote collectors.

Known Issues
===========

* Component templates attempt to graph data that may not be available from
  some components.  This may result in debug level events for SNMP variables
  that don't exist for the component.

* The Device modeler FSP3000R7DeviceMib must be run before any component
  modelers.

* SNMP cache file needs to be created in /tmp.  The file will not be removed
  when the device is deleted from zenoss.  The Adva system must have a name
  or modeling may fail.  The file name is of the form:
  /tmp/SYSTEM-NAME.Adva_inventory_SNMP.pickle 

* All traps do not have a corresponding event class; traps added to Adva
  versions newer than 10.1.4 have not been added.


Screenshots
===========
Device Overview
---------------
|Device Overview|

Power Supply Component
----------------------
|Power Supply Component|

Transponder Component
---------------------
|Transponder Component|

EventClass Mappings
-------------------
|EventClass Mappings|

.. External References Below. Nothing Below This Line Should Be Rendered

.. _Latest Package: http://wiki.zenoss.org/ZenPack:Adva_FSP3000R7

.. |Device Overview| image:: https://github.com/kb8u/ZenPacks.Merit.AdvaFSP3000R7/raw/master/screenshots/DeviceOverview.png
.. |Power Supply Component| image:: https://github.com/kb8u/ZenPacks.Merit.AdvaFSP3000R7/raw/master/screenshots/PowerSupply.png
.. |Transponder Component| image:: https://github.com/kb8u/ZenPacks.Merit.AdvaFSP3000R7/raw/master/screenshots/Transponder.png
.. |EventClass Mappings| image:: https://github.com/kb8u/ZenPacks.Merit.AdvaFSP3000R7/raw/master/screenshots/Mappings.png
