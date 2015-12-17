#!/usr/bin/env python

"""
Start this in interactive mode by running 'python -i py_debug.py'
This will start you out in an interactive session with objects already
created for the domain and nodes.
"""

from ossie.utils import redhawk

dom = redhawk.attach(redhawk.scan()[0])
print("\nAttached to Domain '%s'" % dom.name)
print("\nAvailable Nodes and Devices:")
nodes = dom.devMgrs
for num, node in enumerate(dom.devMgrs):
    print("%d.  %s" % (num, node.name))
    for dnum, dev in enumerate(node.devs):
        print("\t%d.  %s" % (dnum, dev.name))
print("\nWaveforms launched:")
wfs = dom.apps
for num, wf in enumerate(dom.apps):
    print("%d.  %s" % (num, wf.name))
    for cnum, comp in enumerate(wf.comps):
        print("\t%d.  %s" % (cnum, comp.name))
print
try:
    del(num, node, dnum, dev, wf, cnum, comp)
except NameError:
    pass
