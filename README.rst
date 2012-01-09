============================
ZenPacks.Merit.AdvaFSP3000R7
============================

Description
===========
Provides monitoring of FSP3000R7 optical transport systems manufactured by Adva
Optical Networking.

This is a subset of the functionality provided by Adva's proprietary Network
Management System.  Most alerts are implemented and optical signal strength
is graphed.  Most blade types will be detected when modeling a system.  Alerts
severities match Adva's NMS severity levels.

----------------------------------

Zenpack contents
================
The ZenPack has the following:

/Network/Adva Device Class
--------------------------
* The system serial number is populated in the summary

Component modeling
------------------
* Power Supply
 - Component template graphs current

* Optical Amplifier
 - Component template graphs Laser bias current, Optical Power received and transmitted when it's available.

* NCU-II (shelf controller card)

* Transponder Component Modeling
 - Component template graphs Laser bias current, Optical Power received and transmitted when it's available.

* Optical Service Channel Component Modeling
 - Component template graphs Laser bias current, Optical Power received and transmitted when it's available.

* Fan Component Modeling

Event Class mapping
-------------------
* Well over a hundred Event Class Mappings for Adva SNMP traps in sensible eventclasses.
* Event severeties match Adva's levels

-------------------

Requirements
============
* Zenoss Versions Supported: 3.0+
* External Dependencies: None
* ZenPack Dependencies: None
* Configuration: No Special configuration should be necessary.

----------------------------------

Installation
============
Normal Installation (packaged egg)

*NOTE* This is a large zenpack due to the size of the Adva MIB files included.
Installation from the Zenoss web interface may fail on especially slow systems
due to time out issues.  If this happens, try installing from the command line:

Download the appropriate package for your Zenoss version from the list
below.

* Zenoss 3.0+ `Latest Package for Python 2.6`_
  
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

Known Issues
===========
* Component templates attempt to graph data that may not be available from
  some components.  This will result in debg level events for SNMP variables
  that don't exist for the component.

* Adva systems respond slowly to SNMP so modeling will probably silently fail
  to detect many components if you try to run all all Modeler Plugins at the
  same time.  The work-around is to repeatedly model with one plugin at a time.
  The modeler code needs to be modified to not query for the same information
  repeatedly for each modeler.

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
|EventClass Mappings|

.. External References Below. Nothing Below This Line Should Be Rendered

.. _Latest Package for Python 2.6: http://github.com/downloads/kb8u/ZenPacks.Merit.AdvaFSP3000R7/ZenPacks.Merit.AdvaFSP3000R7-py2.6.egg

.. |Device Overview| image:: http://github.com/downloads/kb8u/ZenPacks.Merit.AdvaFSP3000R7/raw/master/screenshots/DeviceOverview.png
.. |Power Supply Component| image:: http://github.com/downloads/kb8u/ZenPacks.Merit.AdvaFSP3000R7/raw/master/screenshots/PowerSupply.png
.. |Transponder Component| image:: http://github.com/downloads/kb8u/ZenPacks.Merit.AdvaFSP3000R7/raw/master/screenshots/Transponder.png
.. |EventClass Mappings|| image:: http://github.com/downloads/kb8u/ZenPacks.Merit.AdvaFSP3000R7/raw/master/screenshots/Mappings.png
