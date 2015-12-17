#!/bin/bash
# Launcher for the RasHawk PI.
gpio export 17 output
gpio export 18 output
gpio export 24 output
gpio export 27 input
gpio export 22 input
gpio export 23 input

nodeBooter -d /nodes/raspberry_pi/DeviceManager.dcd.xml
