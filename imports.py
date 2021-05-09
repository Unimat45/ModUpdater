#!/usr/bin/env python3
import os
from Thread import Threader 
from subprocess import run 
from platform import system
from getpass import getuser as user
from shutil import rmtree 
from crontab import CronTab 
from urllib.request import urlretrieve 
from requests import get 
from sys import stdout
from threading import Thread