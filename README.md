PeasShop
========

GET YO OUTFIT

Install
=======
Lib dependency (manual python installation commands, use requirements.txt instead):

* sudo apt-get install libevent-dev
* pip install flask
* pip install Flask-Sockets
* pip install gunicorn
* pip install gevent
* pip install gevent-websocket

Running on the server
=====================

For now, just `python main.py`, and *not*
`gunicorn -k flask_sockets.worker --debug main:app` as debug doesn't seem to work.

*TODO*: Actually make it run correctly on the PRODACTIAN server using stuff below.


##Server
###Install
Choose a destination which is going to be the base directory of the project.
Create the following folder structure:
```
/var/www/peas_shop/     base dir
  code/                 clone this repository to this destination
  run/                  working directory from where stuff is started
  env/                  directory with virtual environment for the project
```
Clone the github repository to *code/*.
Create a python2 virtualenv in *env/*.
Copy start.sh, stop.sh and uwsgi.ini from *code/server/internals* to *run/*

Adjust the **base_dir** value in the fabfile, *base* in uwsgi.ini, and various paths in the nginx snippet (if in use).
Append the nginx snippet to */etc/nginx/sites-available/default*.

###Update/Run
On your local machine (from the *code/server* directory) execute:
```
fab update
```
This command should update the repository, install all dependencies and (re)start the uwsgi server in one go.

Messages
========
