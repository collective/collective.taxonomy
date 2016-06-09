var path = require('path')
var webpack = require('webpack')

module.exports = {
  devtool: '#cheap-module-eval-source-map', // http://webpack.github.io/docs/configuration.html#devtool
  entry: {
    edittaxonomydata: ['webpack-hot-middleware/client?path=http://localhost:3000/__webpack_hmr',
    './src/js/index'],
  },
  output: {
    path: path.join(__dirname, 'build'),
    filename: '[name].js',
    publicPath: 'http://localhost:3000/static/'
  },
  plugins: [
    new webpack.IgnorePlugin(/^(buffertools)$/), // unwanted "deeper" dependency
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('development')
    }),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin()
  ],
  module: {
    loaders: [{
      test: /\.js$/,
      loaders: ['babel'],
      exclude: /node_modules/,
      include: path.join(__dirname, 'src'),
    }]
  }
}
