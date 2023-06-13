# Data standards team site

This is a Jekyll site hosted on github pages.

## Getting started
The site is hosted on github pages. The instructions below are for running the site locally.

### Dependencies

To get it running on your machine you'll need these installed

* Ruby
* Bundler
* Node (if working on it locally)

### Running locally

Install required gems
```
bundle install
```

Run the site with

```
bundle exec jekyll serve
```

### Running python build locally

To fetch the latest data from the tracker spreadsheet you'll need to create a `.env` file and include the credentials. For example:

```
GOOGLE_PRIVATE_KEY_ID=...
GOOGLE_PRIVATE_KEY=...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_EMAIL=...
```
