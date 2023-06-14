install:
	pip install -r requirements.txt

test:
	py.test server/test.py -vv -n auto
clear:
	python server/main.py clear $(filter-out $@,$(MAKECMDGOALS))
create:
	python server/main.py create $(filter-out $@,$(MAKECMDGOALS))
list:
	python server/main.py list $(filter-out $@,$(MAKECMDGOALS))

%:
	@: