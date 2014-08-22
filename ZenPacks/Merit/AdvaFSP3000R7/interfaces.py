################################################################################
#
# Used for 'Display' drop-down in 'Components' section of GUI.
# Has nothing to do with interfaces on a device.
#
# Copyright (C) 2011 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field on the user interface.

"""

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IModuleInfo(IComponentInfo):
    """ Info adapter for Module (container) component """
    inventoryUnitName = schema.Text(title    = u"Model",
                                    readonly = True,
                                    group    = 'Details')

class IOSCInfo(IComponentInfo):
    """ Info adapter for Optical Service Channel component """
    inventoryUnitName = schema.Text(title    = u"Model",
                                    readonly = True,
                                    group    = 'Details')

class IPowerSupplyInfo(IComponentInfo):
    """ Info adapter for Power Supply component """
    inventoryUnitName = schema.Text(title    = u"Model",
                                    readonly = True,
                                    group    = 'Details')

class IAmplifierInfo(IComponentInfo):
    """ Info adapter for Amplifier component """
    inventoryUnitName = schema.Text(title    = u"Model",
                                    readonly = True,
                                    group    = 'Details')

class IRamanNPortInfo(IComponentInfo):
    """ Info adapter for Raman Amplifier Network Port component """
    inventoryUnitName = schema.Text(title    = u"Model",
                                    readonly = True,
                                    group    = 'Details')

class IRamanUPortInfo(IComponentInfo):
    """ Info adapter for Raman Amplifier Upgrade Port component """
    inventoryUnitName = schema.Text(title    = u"Model",
                                    readonly = True,
                                    group    = 'Details')
class IRoadmInfo(IComponentInfo):
    """ Info adapter for ROADM component """
    inventoryUnitName = schema.Text(title    = u"Model",
                                    readonly = True,
                                    group    = 'Details')

class ITransponderInfo(IComponentInfo):
    """ Info adapter for Transponder component """
    inventoryUnitName = schema.Text(title    = u"Model",
                                    readonly = True,
                                    group    = 'Details')

class INCUInfo(IComponentInfo):
    """ Info adapter for NCU component """
    inventoryUnitName = schema.Text(title    = u"Model",
                                    readonly = True,
                                    group    = 'Details')

class IFanInfo(IComponentInfo):
    """ Info adapter for Fan NCU component """
    # Don't need to show any instance data
    pass
