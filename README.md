# Data standards team site

This is a Jekyll site hosted on github pages.

## Getting started
The site is hosted on github pages. The instructions below are for running the site locally.

### Dependencies

To get it running on your machine you'll need these installed

* Ruby
* Bundler
* Node (if working on it locally)
* Python

### Running locally

Install required gems
```
bundle install
```

Run the site with

```
bundle exec jekyll serve
```

If you want to generate the latest backlog pages you'll need to run the python scripts. We recommend using a [virtual env](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

If you haven't yet install all the dependencies with `make init` run
```
make python-init
```

Fetch the latest planning concern data you first need to create a `.env` file and include the following credentials.
```
GOOGLE_PRIVATE_KEY_ID=...
GOOGLE_PRIVATE_KEY=...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_EMAIL=...
```

Then fetch the latest data with
```
make fetch-backlog-data
```

Generate the pages with
```
make roadmap-page
```
