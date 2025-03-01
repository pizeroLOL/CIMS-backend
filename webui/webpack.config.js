// webui/webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: './src/index.tsx',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js',
        publicPath: '/'
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js'],
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.(png|jpe?g|gif|svg)$/i,
                type: 'asset/resource'
              }
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './src/index.html',
        }),
    ],
    devServer: {
        static: {
          directory: path.join(__dirname, 'dist'),
        },
        port: 50053,
        proxy: [ // 修改这里，将 proxy 选项的值改为数组
            {
                '/api': {
                    target: 'http://localhost:50050',
                    changeOrigin: true,
                },
                '/command': {
                    target: 'http://localhost:50052',
                    changeOrigin: true,
                },
            }
        ],
        historyApiFallback: true,
    },
};