============================
ZenPacks.Merit.AdvaFSP3000R7
============================

.. contents::
   :depth: 3

Description
===========
Provides monitoring of FSP3000R7 optical transport systems manufactured by Adva
Optical Networking.

This is a subset of the functionality provided by Adva's proprietary Network
Management System.  Most alerts are implemented and optical signal strength
is graphed.  Most blade types will be detected when modeling a system.  Alerts
severities match Adva's NMS severity levels.

Components
==========
The ZenPack has the following:
* /Network/Adva Device Class
  * The system serial number is populated in the summary

* Power Supply Component Modeling
  * Component template graphs current

* Optical Amplifier Component Modeling
  * Component template graphs Laser bias current, Optical Power received and transmitted when it's available.

* NCU-II (shelf controller card) Component Modeling

* Transponder Component Modeling
  * Component template graphs Laser bias current, Optical Power received and transmitted when it's available.

* Optical Service Channel Component Modeling
  * Component template graphs Laser bias current, Optical Power received and transmitted when it's available.

* Fan Component Modeling

* Well over a hundred Event Class Mappings for Adva SNMP traps in sensible eventclasses.

