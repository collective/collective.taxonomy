var path = require('path')
var webpack = require('webpack')

module.exports = {
  devtool: 'cheap-module-source-map', // https://webpack.js.org/configuration/devtool
  entry: {
    edittaxonomydata: ['./src/js/index'],
  },
  output: {
    path: path.join(__dirname, 'build'),
    filename: '[name].js',
  },
  plugins: [
    new webpack.IgnorePlugin(/^(buffertools)$/),
    new webpack.optimize.OccurrenceOrderPlugin(),
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production')
    }),
    new webpack.optimize.UglifyJsPlugin({
      compressor: {
        pure_getters: true,
        unsafe: true,
        unsafe_comps: true,
        screw_ie8: true,
        warnings: false
      }
    })
  ],
  module: {
    loaders: [{
      test: /\.js$/,
      loaders: ['babel-loader'],
      exclude: /node_modules/,
      include: path.join(__dirname, 'src'),
    }]
  }
}
