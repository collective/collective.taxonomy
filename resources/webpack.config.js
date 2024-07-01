var path = require('path')
var webpack = require('webpack')

module.exports = {
  devtool: 'eval-cheap-module-source-map', // https://webpack.js.org/configuration/devtool
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
    new webpack.IgnorePlugin(/^(buffertools)$/),
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('development'),
    }),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoEmitOnErrorsPlugin()
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
