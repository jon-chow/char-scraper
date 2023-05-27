install:
	pip install -r requirements.txt

test:
	py.test test.py -n auto
clear:
	python main.py clear $(filter-out $@,$(MAKECMDGOALS))
create:
	python main.py create $(filter-out $@,$(MAKECMDGOALS))
list:
	python main.py list $(filter-out $@,$(MAKECMDGOALS))

%:
	@: