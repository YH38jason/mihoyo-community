module.exports = {
  publicPath: './',
  lintOnSave: true,
  configureWebpack: {
      //关闭 webpack 的性能提示
      performance: {
          hints:false
      }
  
  },
  devServer: {
    disableHostCheck:true
  }
}