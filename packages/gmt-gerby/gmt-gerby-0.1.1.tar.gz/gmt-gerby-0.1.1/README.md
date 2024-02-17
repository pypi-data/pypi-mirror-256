# repositories

* https://github.com/gerby-project/plastex/
* https://github.com/gerby-project/gerby-website
* https://gerby-project.github.io/stacks-instructions
* https://github.com/stacks/stacks-project

forks:

* https://github.com/paolini/pybtex-gerby


# setup static files

```bash
pushd gerby/static
git clone https://github.com/sonoisa/XyJax.git
sed -i -e 's@\[MathJax\]@/static/XyJax@' XyJax/extensions/TeX/xypic.js
git clone https://github.com/aexmachina/jquery-bonsai
cp jquery-bonsai/jquery.bonsai.css css/
popd
```

# start development server

prepare virtual environment once:

```bash
python -m venv venv
. venv/bin/activate
git clone https://github.com/paolini/pybtex-gerby.git
python -m pip install ./pybtex-gerby
rm -fr pybtex-gerby
git clone https://github.com/paolini/mdx_bleach
python -m pip install ./mdx_bleach
rm -fr mdx_bleach
python -m pip install -e .
```

or activate it if already prepared:

```bash
. venv/bin/activate
```

# update database

You need the WEB directory built from the gmt-book project with the `build_web.sh` script. Use this command to create the databases.

```bash
pushd WEB
python ../gerby/tools update.py
popd
```

# run locally

```
python -m flask --app gerby run
```

# build pypi package

```bash
python -m build
python -m pip install --upgrade twine
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-yourSecretToken
python -m twine upload dist/*

```

# systemctl service configuration

In `/etc/systemd/system/gerby.service`

```
[Unit]
#  specifies metadata and dependencies
Description=Gunicorn instance to serve gerby gmt-project
After=network.target
# tells the init system to only start this after the networking target has been reached
# We will give our regular user account ownership of the process since it owns all of the relevant files
[Service]
# Service specify the user and group under which our process will run.
User=root
# give group ownership to the www-data group so that Nginx can communicate easily with the Gunicorn processes.
Group=www-data
# We'll then map out the working directory and set the PATH environmental variable so that the init system knows where our the executables for the process are located (within our virtual environment).
WorkingDirectory=/root/gmt/gerby-website/gerby/tools
Environment="PATH=/root/gmt/gerby-website/gerby/tools"
# We'll then specify the commanded to start the service
ExecStart=/root/gmt/gerby-website/venv/bin/gunicorn --workers 3 --bind unix:app.sock -m 007 wsgi:app
# This will tell systemd what to link this service to if we enable it to start at boot. We want this service to start when the regular multi-user system is up and running:
[Install]
WantedBy=multi-user.target
```