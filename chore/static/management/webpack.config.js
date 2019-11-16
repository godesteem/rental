var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,
  entry: './src/index.js',
  output: {
      path: path.resolve(__dirname, 'build'),
      filename: "[name]-[hash].js"
  },

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      },
      {
          test:/\.css$/,
          use:['style-loader','css-loader']
      },
      {
          test: /\.svg$/,
          loader: 'svg-inline-loader'
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'})
  ]
}
