#!/usr/bin/python

# Purpose: Node DCD.xml's define a set of IDs and names that must be unique
#    Domain which causes trouble when deploying clones of a Node throughout
#    a Domain.  This script updates the deviceconfiguration ID and Name with 
#    a new UUID and increment.  It also updates the componentinstantiation(ref)
#    (ref)id fields with the new Name of the Node.  The new name will be the
#    original name suffixed with the first 2 hex digits from the new UUID.
import fileinput, re, uuid

try:
    id = uuid.uuid4()
    designator = str(id)[:2]
    
    print "New Node UUID: {0}".format(str(id))
    print "Node name will end: {0}".format(designator)

    for line in fileinput.input(files='DeviceManager.dcd.xml', inplace=1, backup='.bak'):
       line = re.sub(r'(deviceconfiguration\s+id="DCE:)(.+?)("\s+name="\w+?)([a-f0-9]{0,2})(")', 
                     r'\g<1>{0}\g<3>{1}\g<5>'.format(str(id), designator), 
                     line)
       line = re.sub(r'(componentinstantiation.+?id=".+?)([a-f0-9]{0,2})(:.+?")',
                     r'\g<1>{0}\g<3>'.format(designator),
                     line)
       line = re.sub(r'(simpleref\s+refid="stream_id"\s+value="rtl_sdr_)(.+?)(")',
                     r'\g<1>{0}\g<3>'.format(designator),
                     line)
       print line.rstrip()
except Exception as e:
    print "Something went wrong."
    print e 
