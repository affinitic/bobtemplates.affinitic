bin/pip:
	virtualenv-2.7 .

build-dev: bin/pip
	ln -f -s dev.cfg buildout.cfg
	bin/pip install -I -r requirements.txt
	bin/buildout

build-prod: bin/pip
	ln -f -s prod.cfg buildout.cfg
	bin/pip install -I -r requirements.txt
	bin/buildout
