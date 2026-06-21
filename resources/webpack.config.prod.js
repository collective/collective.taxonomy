const path = require('path')
const webpack = require('webpack')
const TerserPlugin = require('terser-webpack-plugin')

module.exports = () => {
  return {
    mode: 'production',
    devtool: 'cheap-module-source-map', // https://webpack.js.org/configuration/devtool
    entry: {
      edittaxonomydata: ['./src/js/index'],
    },
    output: {
      path: path.join(__dirname, '../src/collective/taxonomy/static/js'),
      filename: '[name].js',
    },
    optimization: {
      minimizer: [new TerserPlugin({ extractComments: false })],
    },
    plugins: [
      new webpack.IgnorePlugin({ resourceRegExp: /^(buffertools)$/ }),
      new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify('production'),
      }),
    ],
    module: {
      rules: [
        {
          test: /\.js$/,
          use: ['babel-loader'],
          exclude: /node_modules/,
          include: path.join(__dirname, 'src'),
        },
      ],
    },
  }
}
