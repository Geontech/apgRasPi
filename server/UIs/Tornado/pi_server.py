#!/usr/bin/env python

import os
import sys
import time
import pdb
import json
import socket
import argparse
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop

from threading import Timer
from heapq import merge

from ossie.utils import redhawk
from ossie.utils.redhawk.channels import ODMListener
from ossie.utils.weakmethod import WeakBoundMethod


def getLaptopIPaddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    ipaddr = s.getsockname()[0]
    s.close()
    return ipaddr

def getLaptopLatLon():
    dom = redhawk.attach(redhawk.scan()[0])
    for node in dom.devMgrs:
        if node.name.lower() == 'LaptopNode':
            for dev in node.devs:
                if dev.name.lower() == 'gps_receiver':
                    gps_port = dev.getPort('GPS_idl')
                    pos = gps_port._get_gps_time_pos().position
                    return pos.lat, pos.lon, pos.valid
    lat = raw_input("WARNING: Unable to find GPS device connected to server.\nPlease enter latitude in degrees: ")
    lon = raw_input("Please enter longitue in degrees: ")
    return lat, lon, True

def _parseInput():
    parser = argparse.ArgumentParser(description='Launch Server')
    ipaddr = getLaptopIPaddress()
    parser.add_argument('-a', help='IP address to use for serving', default=ipaddr)
    parser.add_argument('-p', help='Port to use for serving', default='8080')
    args = vars(parser.parse_args())
    return args


class MapHandler(tornado.web.RequestHandler):
    def initialize(self, ipaddr, port, lat, lon):
        self._ipaddr = ipaddr
        self._port   = port
        self._lat    = lat
        self._lon    = lon

    def get(self):
        print("A client pulled map_template.html to show the map")
        pis = 0
        dom = redhawk.attach(redhawk.scan()[0])
        for node in dom.devMgrs:
            print("Node name: %s" % node.name)
            if 'raspberry' in node.name.lower():
                pis = pis + 1
        print("Number of pis: %s" % pis)
        self.render("map_template.html", ipaddr=self._ipaddr, port=self._port, lat=self._lat, lon=self._lon, num_pis=0)
 

class WebSocketMapHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("A websocket connection was opened to the Map websocket")
        self._connectToDomain()
        self._setupOdmListener()
        Timer(1.0, self._hack).start()
    
    """ Connect to domain, add pis found to our list, add them to the GUI.  """
    def _connectToDomain(self):
        self.dom = redhawk.attach(redhawk.scan()[0])
        rx_pis, tx_pis = self._getPisList()
        for node in rx_pis:
            lat, lon, valid = self._getNodeLatLon(node)
            self.update_map(node.name, 'add', lat, lon)
        for node in tx_pis:
            lat, lon, valid = self._getNodeLatLon(node)
            self.update_map(node.name, 'addTx', lat, lon)
 
    def _setupOdmListener(self):
        try:
            self.odm = ODMListener()
            self.odm.connect(self.dom)
            self.odm.deviceManagerAdded.addListener(WeakBoundMethod(self.deviceManagerAdded))
            self.odm.deviceManagerRemoved.addListener(WeakBoundMethod(self.deviceManagerRemoved))
        except:
            print("  ERROR: setupOdmListener failed; please make sure a REDHAWK Domain Manager is running\n")

    def _hack(self):
        rx_pis, tx_pis = self._getPisList()
        for node in rx_pis:
            self.update_map(node.name, 'add', 0.0, 0.0)
        for node in tx_pis:
            self.update_map(node.name, 'addTx', 0.0, 0.0)
        cb = tornado.ioloop.PeriodicCallback(self._timed_pi_update, 1000)
        cb.start()        
        lob_poll = tornado.ioloop.PeriodicCallback(self._pollLobComponents, 2000)
        lob_poll.start()
 
    def on_message(self, message):
        print("\nMessage received from map client: %s" % message)
 
    def on_close(self):
        print("\nWebsocket connection to %s closed" % self)

    def update_map(self, name, action, lat, lon, lob_angle=0.0):
        # action: 'add', 'addTx', 'remove', 'addLob', or 'update'
        data = {'nodeName': name, 'action': action, 'lat': lat, 'lon': lon, 'angle': int(lob_angle)}
        msg = json.dumps(data)
        self.write_message(json.dumps(msg))
        if ((action <> 'update') and (action <> 'addLob')):
            print("Will now %s marker for node %s located at %s, %s" % (action, name, lat, lon))

    def deviceManagerAdded(self, evt):
        print("Added device manager %s" % evt.sourceName)
        #pdb.set_trace()
        if 'raspberry_pi' in evt.sourceName.lower():
            #print("This is where I will call self.update_map to add a marker")
            self.update_map(evt.sourceName, 'add', 0.0, 0.0)
 
    def deviceManagerRemoved(self, evt):
        print("Removed device manager %s" % evt.sourceName)
        if evt.sourceName.lower() == 'raspberry_pi':
            #print("This is where I will call self.update_map to remove a marker")
            self.update_map(evt.sourceName, 'remove', 0.0, 0.0)
                
    
    """ Timed update of node positions at runtime """
    def _timed_pi_update(self):
        rx_pis, tx_pis = self._getPisList()            
        for node in list(merge(rx_pis, tx_pis)):
            try:
                """ Somehow dom.devMgrs is not being updated fully when nodes join/leave"""
                lat, lon, valid = self._getNodeLatLon(node)
            except:
                lat, lon, valid = 0.0, 0.0, False
            self.update_map(node.name, 'update', lat, lon)
                    
    """ Simple function to pull all nodes whose name starts with raspberry_pi """
    """ Node are sorted according to whether they are receiver or transmitter nodes """
    def _getPisList(self):
        rx_list = []
        tx_list = []
        for node in self.dom.devMgrs:
            if node.name.startswith('raspberry_pi'):
                for dev in node.devs:
                    if 'rtl_sdr' in dev.name.lower():
                        rx_list.append(node)
                        break
                    if 'transmit_control' in dev.name.lower():
                        tx_list.append(node)
                        break
        return rx_list, tx_list

    """ Fetch lat, lon, and validity of information from node. """
    def _getNodeLatLon(self, node):        
        for dev in node.devs:
            if (dev.name == 'gps_receiver'):
                gps_port = dev.getPort('GPS_idl')
                pos = gps_port._get_gps_time_pos().position
                return pos.lat, pos.lon, pos.valid

    """ Poll the LOB components """
    def _pollLobComponents(self):
        if len(self.dom.apps) > 0:
            for wf in self.dom.apps:
                for comp in wf.comps:
                    if 'lobCalc' in comp.name:
                        comp_dict = comp._query()
                        if comp_dict['valid']:
                            angle = int(comp_dict['lob'])
                            # TODO: This can be hardcoded for testing only
                            #piNum = comp_dict['streamID_prop'][-2:]
                            piNum = 87
                            adjusted_angle = self._nearestFive(angle)
                            print("INFO: raspberry_pi%s, LOB %d degrees (%d)" % (piNum, angle, adjusted_angle))
                            self.update_map('raspberry_pi'+str(piNum), 'addLob', 0, 0, adjusted_angle)
                        else:
                            #print("DEBUG: LOB valid for pi %s is not valid" % comp_dict['streamID_prop'][-2:])
                            pass
        else:
            print("No DF waveforms available")

    def _nearestFive(self, value):
        mod = value % 5
        if mod < 3:
            return value - mod
        else:
            return value + (5-mod)

 
class Application(tornado.web.Application):
    def __init__(self, ipaddr, port, lat, lon):
        handlers = [
            (r'/',           MapHandler,    {'ipaddr':ipaddr, 'port':port, 'lat':lat, 'lon':lon}),
            (r'/wsmap',      WebSocketMapHandler),
        ]
 
        settings = {
            'static_path': os.path.join(os.path.dirname(__file__), "static"),
            'template_path': 'templates',
            'debug'        : True,
        }
        tornado.web.Application.__init__(self, handlers, **settings)
 
 
if __name__ == '__main__':
    # Get command line arguments
    cfg = _parseInput()
    ipaddr     = cfg['a']
    port       = cfg['p']
    laptop_lat, laptop_lon, pos_valid = getLaptopLatLon()
    # Set up ODM Listener on first REDHAWK Domain Manager
    pass
    # Set up web server
    ws_app = Application(ipaddr, port, laptop_lat, laptop_lon)
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(port)
    print("\nNow serving on port %s of address %s....\n" % (port, ipaddr))
    print("\n****** REMOVE HARDCODED POSITION VALUES BEFORE RELEASING *****\n\n")
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nReceived KeyboardInterrupt, shutting down server.")
