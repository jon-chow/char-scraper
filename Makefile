install:
	pip install -r requirements.txt

test:
	python test.py
clean:
	python main.py clean $(filter-out $@,$(MAKECMDGOALS))
create:
	python main.py create $(filter-out $@,$(MAKECMDGOALS))

%:
	@: