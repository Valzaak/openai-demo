create-r:
	pip freeze > requirements.txt
	@echo "requirements.txt file created with the current environment packages."
