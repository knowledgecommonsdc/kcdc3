## About this project

This is a site for running a free school, written to fit the needs of [Knowledge Commons DC](http://knowledgecommonsdc.org) ([contact@knowledgecommonsdc.org](mailto:contact@knowledgecommonsdc.org)).

See [this repository's wiki](https://github.com/knowledgecommonsdc/kcdc3/wiki) for information about plans, structure, installation, and use.


## Directory structure

- kcdc3/
	- config.rb  _Compass config for old site_
	- kcdc3/  _Django_
		- apps/  _apps_
		- public/ 
			-	media/  _user uploads, served from `MEDIA_URL`_
			-	static/  _application static files, served from `STATIC_URL`_
		-	settings/  _configuration_
		-	templates/  _base templates and overrides for apps_
		-	tmp/
			-	django.db  _location for sqlite test database_
		- urls.py
		- wsgi.py
	- readme.md
	- requirements/  _Django dependencies_
	- requirements.txt  _Django dependencies_
	- frontend/  _Yeoman/Grunt/Bower dev environment for CSS/JS_
		- app/  _work_
		- bower.json
		- dist/  _output of Grunt build_
			-	assets/  _CSS/JavaScript/fonts, to be served from `ASSET_URL`_
		- Gruntfile.js
		- node_modules/  _Grunt plugins_
		- package.json
		- test/  _JS testing (not used)_
	- virtual/  _Python environment_


## Frontend development environment

The frontend environment is built around the [Yeoman](http://yeoman.io) [generator-webapp](https://github.com/yeoman/generator-webapp). It uses Grunt for automation and Bower for managing dependencies.  

The frontend files are inside the `frontend/` folder. None of the files here interact with Django directly, other than one folder that is served as static files. The larger folders contain third-party modules, and they are not under version control.

Editable SASS and JavaScript files are in `frontend/app`. Compiled, minified versions of the same files are gathered in `frontend/dist`, which, in production, will be served statically at `ASSET_URL`. 

To watch files for changes and run a preview server, run `cd frontend` and `grunt watch`. The preview server pulls files from a hidden temporary directory.

To produce deployable files, run `grunt build`. This command outputs concatenated, minified files into `frontend/dist`.


## License

2012-08-20: Original work in this project is copyright Knowledge Commons DC and contributors, and will be available under an open source license. The project is not ready for public release, but email KCDC for details.
