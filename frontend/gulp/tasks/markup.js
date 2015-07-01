var gulp = require('gulp');
var config = require('../config').markup
var browserSync  = require('browser-sync');
var gulpInclude = require('gulp-include');

gulp.task('markup', function() {
  return gulp.src(config.src)
	.pipe( gulpInclude({ extensions: ['html','js'] }))
    .pipe(gulp.dest(config.dest))
    .pipe(browserSync.reload({stream:true}));
});
