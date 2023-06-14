install:
	pip install -r requirements.txt

test:
	py.test src/server/test.py -vv -n auto
clear:
	python src/server/main.py clear $(filter-out $@,$(MAKECMDGOALS))
create:
	python src/server/main.py create $(filter-out $@,$(MAKECMDGOALS))
list:
	python src/server/main.py list $(filter-out $@,$(MAKECMDGOALS))
server:
	python src/server/server.py

%:
	@: