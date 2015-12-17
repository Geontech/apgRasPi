Author:  Thomas Goodwin
Company: Geon Technologies
Date:    2013/10/02
Version: 0.1

Brief:
   
   REDHAWK Node and Device for interfacing with the RTLSDR library from Osmocom.  This 
   set of files also includes an waveform for FM demodulation and REDHAWK 1.8-style 
   "gateway" component implementing a usesdevice relationship with the Device.


Descriptions: 

   (found in raspi)
   
   Name: raspberry_pi
   Type: REDHAWK Node
   Contains a GPP and rtl_sdr_device Devices.
   
   Name: rtl_sdr_device
   Type: REDHAWK Device (Executable)
   Interface to the RTLSDR library (produced by osmocom).  This device will auto-start
   when the enclosing Node is launched as long as the device is found.
   
   
   (found in redhawk)
   
   Name: rtl_fm_receiver
   Type: REDHAWK Waveform
   Simple example waveform to tune FM radio using the rtl_sdr_gateway Component.
   
   Name: rtl_sdr_gateway
   Type: REDHAWK Component
   This component has a usesdevice propertyref dependency to single out the an
   instance of the rtl_sdr_device on a given Domain.
   

Known Issues:

   1) Some property set/gets do not work with the RTLSDR library.  Unknown errors are
      returned and forwarded to the user through the console as ERROR and WARN messages.
      
   2) If a dongle is not found on startup, attempting to stop-start the Device after 
      plugging the dongle in will occasionally crash the Device.  Relaunching the Node
      resolves the problem, but clearly some more checks need to be added to that
      sequence.


Installation:

   1) Compile and install the RTLSDR library (.so) into your /etc/local/lib path.  

   2) Add /etc/local/lib to your LD_LIBRARY_PATH variable:
      export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib

   3) Deployment:
   
      a) If using the REDHAWK IDE, you can 'Import...' these projects into your workspace
         and deploy them into your Node from there.
      
      b) If using a Pi to run the Node from CLI, navigate to where you copied the 
         raspberry_pi Node and rtl_sdr_device Device directories and enter the following:
         
         cp -r ./raspberry_pi $SDRROOT/dev/nodes
         cd ./rtl_sdr_device/cpp
         make distclean; ./reconf; ./configure; make; make install
         
      c) Get a snack.  This process will take a few minutes.
         
   4) At this point, you should be able to use nodeBooter to start the Node as usual.  If 
      successful, you will see INFO messages indicating that the RTL device was found and
      configured with the property settings in the Node.       
