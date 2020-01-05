tree:
	@ # @ tree -I '*.csv|*.pyc|*.html|out|__pycache__|old' > edit
	tree -I "__pycache__|*.pyc|out|*.csv|*.gz|__init__.py|stuff|*.json|build|dist|LICENSE|README.md|Makefile|logs|PyQuantum.egg-info|sink_single_out|setup.py|install_python*" > edit_tree

setup:
	@ rm dist/* 2>/dev/null || true;
	# $('perl -ne 's/(\d+)\.(\d+)\.(\d+)/$1.".".$2.".".(0+$3+1)/e; print $_' -i setup.py');
	@ perl -ne 's/(\d+)\.(\d+)\.(\d+)/$$1.".".$$2.".".(0+$$3+1)/e; print' -i setup.py
	@ python3 setup.py sdist bdist_wheel;

send_test:
	@ twine upload --repository-url https://test.pypi.org/legacy/ dist/*

send:
	@ twine upload dist/*

test:
	python3 -c 'import PyQuantum.Common'
	python3 -c 'import PyQuantum.Bipartite'

	@ # @ python3 -c 'import pyquantum.quanttest; pyquantum.quanttest.print_quantum()'

upgrade:
	sudo pip3 install --upgrade pyquantum

all:
	make setup && make send;
	sudo pip3 install --upgrade pyquantum

ls:
	ls /usr/local/lib/python3.6/dist-packages/PyQuantum

push:
	git add .
	git commit -m 'init'
	git push

# -------------------------------------------------------------------------------------------------
bp:
	python3 run_bp.py

bpl:
	python3 run_bpl.py

tc:
	python3 run_tc.py
# -------------------------------------------------------------------------------------------------
clean:
	@ find . -type f -name '*.html' -delete
	@ find . -type f -name '*.csv' -delete
