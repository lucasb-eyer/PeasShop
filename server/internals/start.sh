#!/bin/bash
rm sock.file pid.file
uwsgi --ini uwsgi.ini
