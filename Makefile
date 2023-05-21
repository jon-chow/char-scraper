install:
	pip install -r requirements.txt

test:
	python test.py
clear:
	python main.py clear $(filter-out $@,$(MAKECMDGOALS))
create:
	python main.py create $(filter-out $@,$(MAKECMDGOALS))

%:
	@: