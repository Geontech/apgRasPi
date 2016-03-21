# APG Raspberry Pi Tech Challenge

**Development Ceased:** Winter 2013
**Final Report Date:** 7 March 2014
**Date of this Document:** 21 March 2016

**Directories:**

 * raspberry_pi - Software resident on the Raspberry Pi sensor node
 * server - Software resident on the REDHAWK domain laptop
 * documentation - Related notes, walk-throughs, sub-topics (see notes below)
 * testing - An early experimentation with the LOB calculation component and related simulations

## Very Important Notes

1.  This project is a couple of years old; it began in REDHAWK 1.8.6 and concluded using REDHAWK 1.9.0.  Neither of these are the present version of REDHAWK nor are they compatible.

2.  If you try to use the Raspberry Pi installation instructions in the documentation folder, you will end up with a 1.8-ish installation, which is where the project began.  The steps are similar for compiling 1.9 and 1.10, however please note that other changes between these versions will create considerable friction in trying to get anything basic working using the direct contents of this repository.

3.  The LOB calculation component was a stretch goal for the project.  Its behavior was simulated, but for screenshots the component was hard-coded to 30 degrees.

4.  The GPS Receiver was not being used for precise time synchronization; essentially it was also for graphing locations of nodes in the network.  It can be eliminated if you simply want to recreate a node with the RTL device.

5.  At the time this work was published, there was no RTL2832U Device publicly available let alone one with FEI interface support.  As of 1.10.0, the RTL2832U Device is part of the REDHAWK core assets and can be easily deployed in replacement for our `rtl_sdr_device` which in the master branch DOES NOT support FEI allocations.

6.  The `waveform_example` was an example that only demodulated voice from our FRS radios.  Also, the extra TuneFilterDecimate is not actually needed in this instance.

7.  The Arduino -based antenna switching unit was employed to stabilize the switching frequency between the antennas since controlling it from the Pi's GPIO directly caused considerable jitter since it is not on an RTOS.  

8.  The Arduino's programming file for performing the switching is not included in this repository.  Unfortunately, it no longer exists.  Moreover the implementation required a custom switch board, so this is all left as an exercise to the end-user since the missing programming file effectively makes this whole step a custom solution.

9.  The `documentation` folder contains some general topics related to this work.  It is not a series of guides for fully recreating this work.  It is not a description for how to apply this repository's contents into an more recent version installation of REDHAWK SDR.  No document like those two exists at this time and likely will not since, as one will read below, much of this is now OBE because of public releases from the REDHAWK SDR team or requires the user to create a custom solution to finish the implementation.


## What to Expect from this Repo

If you have deployed a REDHAWK 1.9.0 to an x86 workstation and a Raspberry Pi, you can expect a fairly turn-key use of this repository to do the following:

1.  Deploy a NON-FEI RTL2832U Receiver (`rtl_sdr_device`)
2.  Deploy a GPS Receiver that communicates with a GlobalSat BU-353 serial receiver
3.  Deploy an antenna switching Device that inputs from the Pi's GPIO via WiringPi to read switch positions from  a user-provided switch interface
4.  Deploy a Node that implements the above 3 Devices
5.  Deploy a Device that can output via WiringPi using the Pi's GPIO to trigger transmissions in a particularly-modified FRS hand-held radio (which was an off-the-shelf part as described in the AOC Challenge write-up)
6.  Waveform that uses REDHAWK Components to demodulate FRS FM Radio signals that will automatically connect to the aforementioned RTL2832U Device (`usesdevice` relationship)

### Q: So can I use this in the latest REDHAWK release?  

#### A: Yes and no.  

You can use the REDHAWK SDR RTL2832U Device as a replacement for our `rtl_sdr_device` so long as you modify the `usesdevice` relationship in the Waveform (or create a new Waveform) that tries to allocate to whatever center frequency, bandwidth, etc. you have of interest.  You will also have to make changes to the provided Node DCD XML file as described later.  For reference, the best sampling performance we could attain with a Pi and RTL2832U via USB was just under 250 Ksps.

Given the simplicity of each Device and the reliance of each on an external library (NMEA and WiringPi), it might be an interesting exercise to create new Device projects and port the code from the provided devices into those new projects.  From there you would need to update the Node definition to use the new UUIDs for these Devices and delete the C++ implementation processor requirements for x86/x86_64 (since they are irrelevant for Devices since you are compiling it and deploying it manually for the hardware where you intend it to run which is different than Components, which is why those properties actually exist).

### Q: Can I not simply open and regenerate those two Devices in the IDE?  

#### A: Yes...and no.  

It is true the IDE will let you attempt this.  It is wrong to assume it will work.  This is especially wrong if you are jumping to 2.0 which both unified and changed a great many things (like Property kind relationships).  Our YouTube videos on the Property Kinds series cover these old and new behaviors.

## Moving Forward

First, installing REDHAWK 1.9.0 onto a Raspberry Pi is very similar to the 1.8 instructions in documentation.  The primary difference is which repository you use.  At the step where you clone from Axios Engineering, change this to the [REDHAWK SDR](git://github.com/redhawksdr/framework-core) one.  Then switch to the 1.9.0 tag.

Next, the installation process for the REDHAWK Devices in this repository are all fairly similar.  As long as the libraries are installed (nmea, included in gps_receiver's top-level folder, and WiringPi, available online), one can then compile and install each locally on the Raspberry Pi using `reconf; make; make install`.  This will place them on the SDRROOT of the Raspberry Pi.  

Then, you will need a node definition for the Pi.  We provide one that should work as long as none of the UUIDs for the Devices have been touched.  If you have swapped out the `rtl_sdr_device` for the REDHAWK SDR `RTL2832U` one, this obviously will not be true anymore so you will have to update that reference.  If you are skipping having the GPS receiver, you will need to delete its reference(s) from the Node.  The folder and DCD.xml need to be placed in the `$SDRROOT/dev/nodes/` path on the Raspberry Pi.  A boot script is provided if one is interested in automatically starting the Node on boot-up.  However it requires a network connection to an active Domain and properly configured local `/etc/omniORB.cfg` to work.

Next, on your REDHAWK Domain system, you will need to install the `waveform_example`.  Via the IDE, this is dragging the project to the Target SDR.  If you are using an updated version of REDHAWK, you need to make sure the port names referenced in the SAD.XML match each target's port names because they changed recently (or, delete those connections from the XML, save, and re-add them in the diagram view, save, and deploy again).  If you swapped RTL Devices for the REDHAWK SDR one, the `usesdevice` relationship will need to be modified to allocate the tuner.  Because it is an FEI tuner, you will need to populate the minimum set of properties to do so (there is a wizard for this in the IDE for 2.0 that is available from the right-click menu as shown in our Waveform Usage 2.0 video on YouTube).

Finally, start the Domain and the GPP Node on an x86/x86_64 compatible computer that will be serving as the controller and executor of the Waveform's components.  Start the Raspberry Pi's node as well and verify that both nodes are showing in the Domain's Device Manager's list in either the SCA Explorer or the IDE's snap-in.  If everything is fine, you can now launch the Waveform by right-clicking the Domain in the IDE and following the prompts.

Unless something has gone wrong you should be demodulating FM transmissions at this point.  If you are using our RTL device, you will have to configure its tuning properties on the device itself.  If you are using the REDHAWK SDR FEI one, you can should be able to adjust these by selecting the allocation from the IDE, right-clicking, and following the prompts.

### Q: Wait... What can go wrong?

#### A: Many things. 

1.  If you find that your Raspberry Pi's Node either doesn't show or is showing a broken Device, it means you should go check the nodeBooter console window associated with it (or the log files) to see why those Devices didn't start.  It's not possible to fully cover the myriad of reasons this could be, so debugging skills will be necessary here.  When in doubt, start nodeBooter with a different debug level.

2.  If when launching the Waveform, your Domain (via the IDE or other means) complains that the `usesdevice` relationship couldn't be met (calling it an allocation), it means the collection of property IDs and values reference in the Waveform's SAD.XML could not be resolved to match properties on any Device in the system.  This usually means property IDs are wrong, the Device itself cannot hit the figures you're trying to set, or soemthing along those lines.  Usually the answer can be seen by changing the nodeBooter debug level if it's not immediately apparent in a log window.

3.  If the Domain rejects launching the Waveform because no suitable executable device could be found, this means you do not have an x86 or x86_64 GPP running somewhere within the Domain (or at least you do not have one with enough resources remaining to support the Waveform, less likely).  If you inspect your Domain and see that indeed no Device Managers have a GPP with an x86/x86_64 processor running, this is your problem: start a node to fill that need.  That need exists because the REDHAWK SDR core asset components in this example waveform *all* require that processor type for their allocations to succeed.

4.  If the Raspberry Pi's Node log indicates it cannot find or start certain devices, make sure they are in-fact installed in the SDRROOT.  Also ensure the UUIDs and paths match the correct locations.  Starting recently for example, the core asset Devices have begun to be installed in an `rh` subdirectory.

5.  If the Waveform cannot launch because Components cannot be found, this may also be related to recent changes in how the core asset Components are installed in the system.  Like the Devices (mentioned above), each is installed in an `rh` subdirectory.  Therefore the references in our older Waveform definition might not match the updated ones if you're using a new version of REDHAWK.

## Getting Support

Please keep in mind however that this project is no longer active.  There is no support expressed or implied in our having published these works.  However, as time is permits, we can attempt to address support questions through redhawk@geontech.com; responses may come from alternate addresses of other engineers.
