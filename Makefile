install:
	pip install -r requirements.txt

test:
	python test.py

run:
	python main.py $(filter-out $@,$(MAKECMDGOALS)) 
%:
	@: