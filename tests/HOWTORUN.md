coverage erase

coverage run -m unittest discover -p "*_tests.py" tests
coverage run -m unittest discover -p "*_tests.py" -s tests

coverage report

test