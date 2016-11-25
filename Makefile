css: static/site/index.css

static/site/index.css: templates/styles/index.scss
	sass --update templates/styles/index.scss:static/site/index.css
