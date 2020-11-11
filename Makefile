setup:
				poetry install

update:
				poetry update

.requirements:
				poetry export -f requirements.txt --output requirements.txt --without-hashes

requirements: .requirements
