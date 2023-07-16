const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer:{
    allowedHosts: "all",
    // port:8080
    https:false,
    // https:false,
    proxy: {
      '/api': {
          target: 'https://116.10.184.254:65153/',//后端接口地址
          changeOrigin: true,//是否允许跨越
          pathRewrite: {
              '^/api': '/api'//重写,
          },
        
  }}}})
