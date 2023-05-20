install:
	pip install -r requirements.txt

test:
	python test.py
cleanup:
	python main.py clean $(filter-out $@,$(MAKECMDGOALS))
run:
	python main.py $(filter-out $@,$(MAKECMDGOALS))

%:
	@: