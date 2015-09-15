/*eslint no-var:[2, {"args": "none"}]*/
var gulp = require('gulp')
var babelify = require('babelify')
var browserify = require('browserify')
var through2 = require('through2')
var runSequence = require('run-sequence')
var eslint = require('gulp-eslint')
var merge = require('merge-stream')

var APP = 'index'
var inputDir = './src/js/'
var outputDir = './build/'
var mapFile = APP + '.map.json'
var mapOutput = outputDir + mapFile
var env = process.env.NODE_ENV || 'development'

var optional = [
  'runtime',
]


// browserify debug:true to generate sourcemaps
// no need to have reactify transform, babelify takes care of jsx transform
gulp.task('browserify', function() {
  return gulp.src(inputDir + APP + '.js')
    .pipe(through2.obj(function(file, enc, next) {
      var bundler = browserify(file.path, { debug: true })

        .transform(babelify.configure({
          optional: optional
        }))

      if (env === 'production') {
        bundler.plugin('minifyify', { map: mapFile, output: mapOutput })
      }
      bundler.bundle(function(err, res) {
        if (err) {
          return next(err)
        }
        file.contents = res
        next(null, file)
      })
    }))
    .on('error', function(error) {
      console.log(error.stack)
      this.emit('end')
    })
    .pipe(gulp.dest(outputDir))
})


// copy some files that we need
gulp.task('copy', function() {
  return merge(
    gulp.src('node_modules/react-treeview/react-treeview.css')
        .pipe(gulp.dest('build/css/'))
  )
})

gulp.task('lint', function() {
  return gulp.src([inputDir + '**/*.js'])
    // eslint() attaches the lint output to the eslint property
    // of the file object so it can be used by other modules.
    .pipe(eslint())
    // eslint.format() outputs the lint results to the console.
    // Alternatively use eslint.formatEach() (see Docs).
    .pipe(eslint.format())
    // To have the process exit with an error code (1) on
    // lint error, return the stream and pipe to failOnError last.
    .pipe(eslint.failOnError())
})

gulp.task('build', function(callback) {
  runSequence('lint', 'browserify', 'copy', callback)
})

gulp.task('watch', function() {
  gulp.watch(inputDir + '**/*.js', ['build'])
})

gulp.task('default', function(callback) {
  runSequence('build', 'watch', callback)
})
