var dest = "../kcdc3/public/static";
var src = './src';
var server_root = '../kcdc3/public';

module.exports = {
  browserSync: {
    server: {
      // Serve up our build folder
      baseDir: server_root
    },
	port: 4000,
	open: false
  },
  sass: {
    src: src + "/sass/**/*.{sass,scss}",
    dest: dest + '/css',
    settings: {
    		indentedSyntax: true, // Enable .sass syntax!
    		imagePath: 'images', // Used by the image-url helper
		includePaths: require('node-neat').includePaths // add node-bourbon and node-neat
    }
  },
  images: {
    src: src + "/htdocs/**/*.{jpg,jpeg,gif,png,svg}",
    dest: dest
  },
  markup: {
    src: src + "/htdocs/**/*.{html,js,json}",
    dest: dest
  },
  iconFonts: {
    name: 'Gulp Starter Icons',
    src: src + '/icons/*.svg',
    dest: dest + '/fonts',
    sassDest: src + '/sass',
    template: './gulp/tasks/iconFont/template.sass.swig',
    sassOutputName: '_icons.sass',
    fontPath: 'fonts',
    className: 'icon',
    options: {
      fontName: 'Post-Creator-Icons',
      appendCodepoints: true,
      normalize: false
    }
  },
  browserify: {
    // A separate bundle will be generated for each
    // bundle config in the list below
    bundleConfigs: [{
      entries: src + '/javascript/global.coffee',
      dest: dest + '/javascript',
      outputName: 'global.js',
      // Additional file extentions to make optional
      extensions: ['.coffee', '.hbs'],
      // list of modules to make require-able externally
      require: ['jquery', 'backbone/node_modules/underscore']
      // See https://github.com/greypants/gulp-starter/issues/87 for note about
      // why this is 'backbone/node_modules/underscore' and not 'underscore'
    }, {
      entries: src + '/javascript/page.js',
      dest: dest + '/javascript',
      outputName: 'page.js',
      // list of externally available modules to exclude from the bundle
      external: ['jquery', 'underscore']
    }]
  },
  production: {
    cssSrc: dest + '/css/*.css',
    jsSrc: dest + '/javascript/*.js',
    cssDest: dest + '/css',
    jsDest: dest + '/javascript' 
  }
};
