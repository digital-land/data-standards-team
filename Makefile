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
