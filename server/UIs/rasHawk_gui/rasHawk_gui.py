import pygtk
pygtk.require('2.0') 
import gtk
from ossie.utils import redhawk, sb
import gobject

class RasHAWK:
    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        sb.show()
        return False
    
    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()
        
    def subRTL(self):
        listOfRTL    = []
        
        for myDev in [self.dom.devices][0]:
            if myDev.name == "rtl_sdr_device":
                listOfRTL.append(myDev._get_identifier())
        
        print self.rtl_list
        print listOfRTL
        
        for idx , rtl in enumerate(self.rtl_list):
            if rtl not in listOfRTL:
                outIdx = idx
                break; 
        
        #self.demod_list[outIdx].disconnect(self.plot_list[outIdx])
        self.demod_list[outIdx].releaseObject()
        del self.demod_list[outIdx]
        del self.rtl_list[outIdx]
        del self.freq_list[outIdx]
        del self.samp_list[outIdx]
        
        self.box_list[outIdx].hide()
        self.table.remove(self.box_list[outIdx])
        del self.box_list[outIdx]
        
        if outIdx != (len(self.rtl_list)):
            print "CHANGING"
            print "outIDx:"+str(outIdx) #0
            print "len(self.rtl_list)" + str(len(self.rtl_list)) #1
            print "len(self.box_list)" + str(len(self.box_list)) #1
            while outIdx < len(self.rtl_list):
                self.table.remove(self.box_list[outIdx])
                self.window.show_all()
                self.table.attach(self.box_list[outIdx], outIdx+1, outIdx+2 , 0, 1)
                outIdx += 1
                
        sb.show()
            
        self.window.show_all()
        
    def addRTL(self):
        listOfRTL = []
        # determine which rtl is new 
        for myDev in [self.dom.devices][0]:
            if myDev.name == "rtl_sdr_device":
                listOfRTL.append(myDev)
        
        for rtl in listOfRTL:
            if rtl._get_identifier() not in self.rtl_list:
                rtlObject = rtl
                #break
    
        # populate gui
        newBox = gtk.HBox(False, 0)
        rtlBox = gtk.VBox(False, 0)
        rtlBox = self.addLabel(rtlBox, "RTL " + str(len(self.rtl_list)))
        
        rtlBox, rtl_freq = self.addDouble(rtlBox, 
                                                    "Frequency:   ", 
                                                    10, 
                                                    "462637500")
        rtlBox, rtl_samp   = self.addDouble(rtlBox, 
                                                    "Sample Rate: ",
                                                    5, 
                                                    "200")
        newBox.pack_start(rtlBox)
        
        self.table.attach(newBox, len(self.rtl_list)+1, len(self.rtl_list)+2, 0, 1)
        self.window.show_all()
        
        sb.stop()
        
        redhawk.Device
        myDemod   = sb.launch("AmFmPmBasebandDemod")
        #plot = sb.LinePSD()
        rtlObject.connect(myDemod)
        #myDemod.connect(plot, usesPortName="fm_dataFloat_out")
        sb.start()
        sb.show()
        
        self.box_list.append(newBox)
        self.rtl_list.append(rtlObject._get_identifier())
        self.demod_list.append(myDemod)
        self.freq_list.append(rtl_freq)
        self.samp_list.append(rtl_samp)
        #self.plot_list.append(plot)
        
    def checkRTL(self):
        numRTLnow = 0
        self.dom = redhawk.attach("REDHAWK_DEV")
        if((self.dom != None) and (self.dom.devices != None)):
            for myDev in self.dom.devices:
                if type(myDev) != None:
                    #print "name is : " + myDev.name
                    if myDev.name == "rtl_sdr_device":
                        numRTLnow += 1
                        #print myDev
                        
            #redhawk.core.ExecutableDevice._get_identifier(self)
            #for dev in self.dom.devices:
                #print type(mgr) 
                #print dev._get_identifier()

            if (numRTLnow > self.numRTL):
                print "\nadd to gui"
                self.addRTL()            
                self.numRTL += 1
            elif (numRTLnow < self.numRTL):
                print "\nsub from gui"
                self.subRTL()
                self.numRTL -= 1
                
        return True
        
    def redhawkSetup(self):
        self.dom = redhawk.attach("REDHAWK_DEV")
        self.numRTL = 0
        self.listOfRTL = []   
        self.rtl_list = []
        self.freq_list = []
        self.samp_list = []
        self.box_list = []
        self.demod_list = []
        #self.plot_list = []
        return
    
    def update(self, button):                
        zipList = zip(self.rtl_list, self.freq_list, self.samp_list)
        for rtlName, freq, sample in zipList:
            for myDev in [self.dom.devices][0]:   
                if (myDev.name == "rtl_sdr_device" and 
                    myDev._get_identifier() == rtlName):
                    rtl = myDev    
            rtl.center_frequency = int(freq.get_text())
            rtl.sample_rate = int(sample.get_text())
            rtl.api()
        
    def addDouble(self, box, label, length, default):
        tempBox = gtk.HBox(False, 0)
        tempLabel = gtk.Label(label)
        tempEntry = gtk.Entry()
        if length != -1:
            tempEntry.set_width_chars(length)
        tempEntry.set_text(default)
        tempBox.pack_start(tempLabel)
        tempBox.pack_start(tempEntry)
        box.pack_start(tempBox)
        return box, tempEntry
    
    def addBool(self, box, label, default):
        tempBox = gtk.HBox(False, 0)
        tempLabel = gtk.Label(label)
        tempBox.pack_start(tempLabel)
        tempCheck = gtk.CheckButton()
        tempBox.pack_start(tempCheck)
        box.pack_start(tempBox)
        return box, tempCheck 
    
    def addLabel (self, box, label):
        tempLabel = gtk.Label(label)
        box.pack_start(tempLabel)
        return box 
    
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("RasHAWK by Geon")
        self.window.set_icon_from_file("geon.png")
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        updateBox = gtk.VBox(False, 0)
        tuneBox  = gtk.VBox(False, 0)   
        ctlBox   = gtk.VBox(False, 0)
        updateBox = self.addLabel(updateBox, "Update Proprties")
        updateBox = self.addLabel(updateBox, " ")
        
        tempImage = gtk.Image()
        tempImage.set_from_stock(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_BUTTON)
        goButton = gtk.Button()
        goButton.set_image(tempImage)
        goButton.connect("clicked", self.update)
        updateBox.pack_start(goButton)
        
        self.table = gtk.Table(2,2)
        self.table.attach(updateBox, 0, 1, 0, 1)
        #self.table.attach(ctlBox, 0, 1, 1, 2)
        self.window.add(self.table)
        self.window.show_all()
        
        self.redhawkSetup()
        gobject.timeout_add_seconds(5, self.checkRTL)        

def main():
   gtk.main()
   return 0        

if __name__ == "__main__":
   RasHAWK()
   main()
