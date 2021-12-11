help:
	@echo "Run "
	@echo "  'make lint' to validate your yaml."
	@echo "  'make build-collection' to build a new version of the Ansible collection"
	@echo " "

lint:
	yamllint .

build-collection:
	ansible-galaxy collection build
