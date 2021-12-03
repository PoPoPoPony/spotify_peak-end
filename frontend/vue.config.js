module.exports={
    devServer: {
        host: 'localhost',
        port: 8080,
        proxy: {
            '/api': {
                target: 'http://localhost:8000/',
                changeOrigin: true,
                secure: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    }
}