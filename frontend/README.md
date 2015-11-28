# KCDC frontend build tools

## Project layout

- `gulp/` _Frontend build config_
- `gulpfile.js` _Frontend build script_
- `../kcdc3/public/` _Files for web server root_
	- `static/` _Static files (CSS, JavaScript, images, and fonts), output from 	Gulp_
- `node_modules/` _Gulp build support, not under version control_
- `package.json` _Node.js packages for gulp_
- `README.md`
- `src/` _HTML, SASS, JavaScript, and images (processed through Gulp)_

Compiled CSS and JavaScript files are at `htdocs/static/`.

## Frontend development tooling

This project uses Gulp for frontend development automation. Build scripts are based on [gulp-starter](https://github.com/greypants/gulp-starter). 

Theme styles are written in SASS, compiled to CSS, and minified for production. Similarly, JavaScript files are concatenated and minified.

The Gulp tools use node-sass, which doesn’t support:
- Compass
- Suffix selectors, i.e. for BEM notation

## Contacts and contributors

[David Ramos](http://imaginaryterrain.com/)


