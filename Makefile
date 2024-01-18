# current git branch
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

js-init:
	npm install

python-init::
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

init:: python-init js-init
	bundle install

serve::
	bundle exec jekyll serve

build::
	bundle exec jekyll build --watch

generate::
	bundle exec jekyll build

black:
	black .

black-check:
	black --check .

flake8:
	flake8 .

isort:
	isort --profile black .

lint: black-check flake8

build-css:
	npm run build:css

fetch-backlog-data: 
	python _bin/fetch_backlog.py

pages: 
	python _bin/generate_roadmap.py

stage-count:
	python3 _bin/planningconsiderations.py

status:
	git status --ignored

commit-roadmap::
	git add what-we-are-working-on
	git diff --quiet && git diff --staged --quiet || (git commit -m "Rebuilt roadmap $(shell date +%F)"; git push origin $(BRANCH))

commit-data::
	git add _data
	git diff --quiet && git diff --staged --quiet || (git commit -m "Fetched latest backlog data $(shell date +%F)"; git push origin $(BRANCH))
