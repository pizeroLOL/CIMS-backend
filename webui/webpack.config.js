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
        proxy: [
            {
                context: '/api', // 指定代理的上下文路径，以 /api 开头的请求会被代理
                target: 'http://localhost:50050', // 目标服务器地址
                changeOrigin: true, // 改变请求头中的 Origin 字段，通常设置为 true
            },
            {
                context: '/command', // 指定代理的上下文路径，以 /command 开头的请求会被代理
                target: 'http://localhost:50052', // 目标服务器地址
                changeOrigin: true, // 改变请求头中的 Origin 字段，通常设置为 true
            }
        ],
        historyApiFallback: true,
    },
};