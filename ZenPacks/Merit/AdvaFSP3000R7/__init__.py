
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

productNames = ('FSP3000R7Device',
                'FSP3000R7Amplifier',
                'FSP3000R7Fan',
                'FSP3000R7Module',
                'FSP3000R7NCU',
                'FSP3000R7Optical100Gig',
                'FSP3000R7OSC',
                'FSP3000R7OTU100Gig',
                'FSP3000R7PowerSupply',
                'FSP3000R7RamanNPort',
                'FSP3000R7RamanUPort',
                'FSP3000R7Roadm',
                'FSP3000R7Transponder',)
