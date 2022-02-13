# nw-rearr-db
Database to store phylogenetic network rearrangement move sequences.
The domain is https://phylofun.remiejanssen.nl


Development
-----------

To run the app in a docker container, install `docker` and `docker-compose`, and run::

    $ ln -s docker-compose.development.yml docker-compose.override.yml
    $ docker-compose build
    $ docker-compose up

The first time you start up the app, make sure to run migrations:

    $ docker-compose run web bin/python3 manage.py migrate


Bumping package versions
------------------------

If you want to upgrade all package versions, use pip-compile::

    (docker) $ bin/pip-compile --upgrade requirements/requirements.in

If you want to selectively upgrade a package version (e.g. django)::

    (docker) $ bin/pip-compile --upgrade-package django requirements/requirements.in
    

Deploy
------

To deploy a new version, run::

    $ ansible-playbook -i ansible/inventory ansible/deploy.yml

Tis deploys the current main branch, but a specific github tag can be set in ansible/deploy.yml
