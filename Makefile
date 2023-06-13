# current git branch
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

init::
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
	bundle install
	npm install

serve::
	bundle exec jekyll serve

build-css:
	npm run build:css

fetch-backlog-data: 
	python _bin/fetch_backlog.py

roadmap-page: 
	python _bin/generate_roadmap.py

status:
	git status --ignored

commit-roadmap::
	git add what-we-are-working-on
	git diff --quiet && git diff --staged --quiet || (git commit -m "Rebuilt roadmap $(shell date +%F)"; git push origin $(BRANCH))
