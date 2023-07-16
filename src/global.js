export default {
popup:(text, msgtype=0) => {
  let message = document.getElementById('message')
  message.innerText = text
  // message.style.transition = 'none'
  if (!msgtype){
    message.style.backgroundColor = "rgba(255,0,0,0.5)";
  }else{
    message.style.backgroundColor = "rgba(127,255,0,0.5)";
  }
  // message.style.transition = 'transition: all .3s ease;'
  message.style.opacity = '1'
  setTimeout(() => {
    message.style.opacity = '0'
  }, 1000);
},

title:"-米哈游交流站 TECH OTAKUS SAVE THE WORLD",
url:"http://127.0.0.1:5000",
// url:"http://192.168.3.5:5000",
// url:"https://116.10.184.254:65153"

// @app.route()
}