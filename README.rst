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

* NCU-II (shelf controller card)

* Transponder Component Modeling

  * Component template graphs Laser bias current, Optical Power received and transmitted when it's available.

* Optical Service Channel Component Modeling

  * Component template graphs Laser bias current, Optical Power received and transmitted when it's available.

* Fan Component Modeling

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

- Update_optical_power_threshold
Create rrd template local copy and/or update the threshold for receive
optical power on amplifiers, transponders, OSCs and ROADMs so that they will
generate an Error level alert if the optical signal degrades 3 dB from
the current value.

Requirements
============

* Zenoss Versions Supported: 3.0+
* External Dependencies: None
* ZenPack Dependencies: None
* Configuration: No Special configuration should be necessary.

Installation
============
Normal Installation (packaged egg)

*NOTE* This is a large zenpack due to the size of the Adva MIB files included.
Installation from the Zenoss web interface may fail on especially slow systems
due to time out issues.  If this happens, try installing from the command line:

Download the appropriate package for your Zenoss version from the Zenoss
Zenpack site:

* Zenoss 3.0+ `Latest Package`_
  
Then copy it to your Zenoss server and run the following commands as the zenoss
user::

    zenpack --install <package.egg>
    zenoss restart
    
If you don't want to do a full restart, you should be able to just restart
zenhub and zopectl::

    zenhub restart &&  zopectl restart
   
Developer Installation (link mode)
----------------------------------
If you wish to further develop and possibly contribute back to this
ZenPack you should clone the git repository, then install the ZenPack in
developer mode using the following commands::

    git clone git://github.com/zenoss/ZenPacks.Merit.AdvaFSP3000R7
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

Known Issues
===========

* Component templates attempt to graph data that may not be available from
  some components.  This will result in debg level events for SNMP variables
  that don't exist for the component.

* The Device modeler FSP3000R7Mib must be run before any component modelers.

* SNMP cache file needs to be created in /tmp.  The file will not be removed
  when the device is deleted from zenoss.  The Adva system must have a name
  or modeling may fail.  The file name is of the form:
  /tmp/SYSTEM-NAME.Adva_inventory_SNMP.pickle where

* All traps do not have a corresponding event class; traps added to Adva
  version 11.2.3 from 10.1.4 have not been added.


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
