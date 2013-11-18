from fabric.api import *
from fabric.colors import green, red

from os import path

# the initial clone has to be performed by hand, as the copying of script/creation of a virtualenv

#expects the following directory configuration on the server:
# /var/www/peas_shop/    base dir
#   ./code/       where the repo is cloned to
#   ./run/        working directory from where stuff is started
#       copy here: start.sh, stop.sh, uwsgi.ini (from server/internals)
#   ./env/        directory with virtual environment for the project

base_dir = "/var/www/peas_shop" #TODO: adjust server folder (also in uwsgi.ini)
run_dir = os.path.join(base_dir, "run")
code_dir = os.path.join(base_dir, "code")
workon = "source {}".format(path.join(base_dir,"env/bin/activate"))

def update():
    env.host_string = "TODO" #TODO: adjust, .ssh/config name of your server
    env.use_ssh_config = True

    print(red("Beginning Update:"))
    with cd(code_dir):
            print(green("Git"))
            run("git fetch --all")
            run("git pull --all")
            run("git checkout master") #TODO: you can specify a branch here
            print(green("Update virtualenv"))
            run("{} && pip install -r requirements.txt".format(workon), )

    print(red("Restart:"))
    with cd(run_dir):
        print(green("Restarting uWSGI"))
        with settings(warn_only=True): #can fail, we don't care
            run("{} && ./stop.sh".format(workon))
        run("{} && ./start.sh".format(workon))
