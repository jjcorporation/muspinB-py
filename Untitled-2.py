#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple iohub eye tracker device demo. Shows how monitoring for central
fixation monitoring could be done.
No iohub config .yaml files are needed for this demo.
Demo config is setup for an EyeLink(C) 1000 Desktop System. 
To to use a different eye tracker implementation, change the 
iohub_tracker_class_path and eyetracker_config dict script variables.
"""
from __future__ import absolute_import, division, print_function

from psychopy import core, visual
from psychopy.iohub.client import launchHubServer

# Number if 'trials' to run in demo
TRIAL_COUNT = 2
# Maximum trial time / time timeout
T_MAX = 10.0