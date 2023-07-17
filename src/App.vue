<template>


<!--            
                                                                                                                         |___/ 
              _   _    _          __     __                                
             (_) | |  | |         \ \   / /                                
  _ __ ___    _  | |__| |   ___    \ \_/ /    ___                          
 | '_ ` _ \  | | |  __  |  / _ \    \   /    / _ \                         
 | | | | | | | | | |  | | | (_) |    | |    | (_) |                        
 |_| |_| |_| |_| |_|  |_|  \___/     |_|     \___/                         
                                                                           
                                                                           
   _____                                                   _   _           
  / ____|                                                 (_) | |          
 | |        ___    _ __ ___    _ __ ___    _   _   _ __    _  | |_   _   _ 
 | |       / _ \  | '_ ` _ \  | '_ ` _ \  | | | | | '_ \  | | | __| | | | |
 | |____  | (_) | | | | | | | | | | | | | | |_| | | | | | | | | |_  | |_| |
  \_____|  \___/  |_| |_| |_| |_| |_| |_|  \__,_| |_| |_| |_|  \__|  \__, |
                                                                      __/ |
                                                                     |___/ 
                                                                                                                         
-->


<div style="z-index: 9999;" v-if="!serverError">
  <div class="navbar" id="nav" v-if="!serverError">
    <nav>
      <router-link title="返回上一页面" id="return" to="" @click="back"><img class="logo" 
        src="./assets/return.png"></router-link>
      <router-link title="技术宅拯救世界！" id="logo" to="/"><img class="logo" 
        src="./assets/logo.png"></router-link>
      <div id="pages">
        <!--主页-->
        <router-link title="米の游戏" to="/themes">米游</router-link> 
        <!-- <router-link title='原神：星穹六号' to="/live/genshin">直播</router-link>        -->
        <router-link title="给钱！" to="/support">赞助</router-link>
        <a title="米哈游官网，mihoyo吧拒绝评分" href="http://www.mihoyo.com" target="_blank">MIHOYO.COM</a>
        <!-- <router-link title="王の宝库" to="/user" v-if="key">{{ user }}</router-link> -->
        <router-link title="快点！这还要我说？" to="" @click="login" v-if="!logged">登录</router-link>
        <router-link title="王の宝库" to="" class="me" @click="panel" 
        v-else>我的主页</router-link>
      </div>
    </nav>
  </div>
  <div class="login hide" id="l" v-show="showTag">
    <h3>{{tagtitle}}</h3>
    <a class="close-login" @click="closeTag">关闭</a>

    <!--Tag主体部分-->
    <login @switchstatus="switchregister" v-if="tagPage == 0"></login>
    <reg v-if="tagPage==1"></reg>
    <me v-if="tagPage == 2" :logged="logged" 
    :username="username" :uid="uid" :token=token :mic="mic"></me>
    <!---------->

  </div>
  <div id="p"></div>
  <!--Body-->
  <router-view @hidnav="hidnav" @error="error" :logged=logged 
  :username=username :uid=uid :reason=reason
  :themes=themes :et=serverStatusText>
  </router-view>
  <!----------------------------------------------->
</div>
<error :reason="reason" v-else></error>
</template>

<script>
// import { nextTick } from 'vue'
import './assets/font.scss'
import global from './global'
import login from './components/tags/login.vue'
import reg from '@/components/tags/reg.vue'
import axios from 'axios'
import me from './components/tags/me.vue'
import error from '@/components/error.vue'
export default{
  components:{
    login,reg,me,error
  },
  data(){
    return{
      // presentPage:0,
      key:false,
      user:"匿名用户",
      showTag:false,
      // comStatus:true,
      tagtitle:"用户登录",
      uid:0,
      logged:false,
      userInfo:[],
      username:"",
      showPanel:false,
      tagPage:0,
      tagTitles:["用户登录",'用户注册','我的面板'],
      // ip:'',
      reason:'',
      token:'',
      serverStatusText:null,
      serverStatus:null,
      serverError:false,
      themes:[[
    ['崩坏:星穹铁道','Honkai:Star Rail'],
    require('./assets/ico/honkaisr.jpg'),
    'hksr',
    ['你游把隔壁问卷拿来优化','悲观地讲，后面忘了']
    ],
    [
    ['原神','Genshin Impact'],
    require('./assets/ico/genshin.jpg'),
    'genshin',
    ['谁是大慈树王？','你游问卷全优化到隔壁']
  ],
  [
    ['崩坏3','Honkai Impact 3rd'],
    require('./assets/ico/hk3.png'),
    'hk3',
    ['Fight for all the beauty in the world!',
    'Stay alive, Kiana.',
    'May all the beauty be blessed.',
    'This is the last lesson.']
  ],
  [
    ['绝区零','Zenless Zone Zero'],
    require('./assets/ico/zzz.jpg'),
    'zzz',
    ['给我二测资格','16+了，心理承受能力肯定上来了对吧']
  ],
  [
    ['未定事件簿', 'Tears of Themis'],
    require('@/assets/ico/tot.jpg'),
    'tot',
    ['你是?', '米哈游还有这游戏?']
  ],
  [
    ['杂谈','Other'],
    require('./assets/ico/myj.png'),
    'other',
    ['米游姬可爱捏','论坛讲究的就是个多元化'],
  ]
],
// 到这这不是themes了
    mic:0,

// Data End-----------------
}},
   beforeMount(){
    async function test(){
      this.serverError = true
      document.title = "System initializing" + global.title
      await axios.post(global.url + '/').then(res => {
      console.log(0)
      if (res.data.status){
        this.$router.push('/error')
        this.serverError = true;
        this.reason = res.data.message;
        // this.$emit('hidnav')
        return
      }else{
        this.serverError = false
        // this.$router.push('/home')
      }
      
    }).catch(
      ()=>{
        // this.$emit('hidnav')
        this.serverError = true;
        this.reason = 'IP address of Server Not Found.'
      }
    )
    }
    // test()
    
    let message = document.createElement('div');
    message.style.position = 'fixed';
    message.style.top = '30%';
    message.style.left = '50%';
    message.style.transform = 'translate(-50%, -50%)';
    message.style.backgroundColor = "rgba(255,0,0,0.5)";
    message.style.padding = '10px';
    message.style.borderRadius = '5px';
    message.id = 'message'
    message.style.transition = "opacity ease 0.3s"
    message.style.opacity = '0'
    message.style.userSelect = 'none'
    document.body.appendChild(message);

    console.log('Backend URL:' + global.url  )
    // this.logged = this.$cookies.isKey('uid')
    this.logged = this.$cookies.isKey('token')
    console.log('Is Logged In:' + this.logged)
    if (this.logged){
      this.token = this.$cookies.get('token')
      console.log('Token: ' + this.token)
    }
    if (this.logged){
      // 如果已经登录
      // this.uid = this.$cookies.get('uid')
      console.log('UID:'+this.uid)
      axios.post(global.url + '/api/user/token',
      JSON.stringify({'token':this.token.toString()}))
      .then(res => {
        if (res.data.exp){
          this.logged = false
          this.$cookies.remove('token')
          this.token = null
          global.popup('登录过期,请重新登录')
          return
        }
        // 获取用户信息
        this.userInfo = res.data.info
        this.username = this.userInfo[1]
        this.uid = this.userInfo[0]
        this.mic = this.userInfo[3]
        console.log("Username:"+this.username)
      })
    }
//----------------------------------------------------Mounted
  },
  methods:{
    hidnav(){
      this.serverError = true;
    },
    error(r){
      console.error(r)
      this.reason = r
      this.$router.push('/error')
    },
    back(){
      this.$router.go(-1)
    },
    login(){
      // console.log("///")
      this.showTag = true
      // nextTick(() => {
        let l = document.getElementById("l")
        l.style.display = "block"
      this.tagPage = 0
      // })
    },
    closeTag(){
      // let l = document.getElementById("l")
      // l.style.display = "none"
      this.showTag = false
    },
    switchregister(){
      this.tagPage = 1
      this.tagtitle = this.tagTitles[this.tagPage]
    },
    panel(){
      this.showTag = true
      this.tagPage = 2
      this.tagtitle = this.tagTitles[this.tagPage]
    },
  },
}
</script>

<style>
.user-panel{
  border: none;
  border-radius: 5px;
  box-shadow: 0 0 1px;
  /* opacity: 0; */
  background-color: rgb(251, 251, 251);
  height: 140px;
  width: 200px;
  transition: all .3s ease;
  position: absolute;
  top: 150px;
  right: -100%;
  transform: translate(-50%,-50%);
  pointer-events: none;
  z-index: 9999;
  /* margin-top:; */
}
.me{
  position: absolute;
  /* right: 28%; */
}
 /* .me:hover .user-panel{
  opacity: 1;
} */
.login{
  text-align: left;
  /* display: ; */
  position: fixed;
  height: 430px;
  width: 300px;
  background-color:rgb(251, 251, 251);
  right: -12.2%;
  top: 50%;
  z-index: 9999;
  transform: translate(-0%, -50%);
  /* border-radius: 10px; */
  /* box-shadow: 0 0 2; */
  -webkit-transition: all .5s ease;
  transition: all .1s ease;
}
.login h3{
  margin-left: 20px;
}
.login:hover{
  box-shadow: 0 0 2px;
  right: 0;
  /* transform: translate(-50%, -50%); */
}
.close-login{
  position: absolute;
  top: 23px;
  right: 15px;
  color: rgb(0, 145, 255);
  cursor: pointer;
  transition: all .3s ease;
  /* display: none; */
}
.close-login:hover{
  color: red;
}

body{
  /* background-color: rgb(246,246,246);*/
  background-image: url('./assets/bk/b2.png');
  background-size: cover;
}

body::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(246,246,246, 0.8);
  z-index: -1;
  /* display: none; */
}

#p{
  /* top: 0; */
  height: 30px;
  margin-bottom:30px;
}

.navbar{
  /* display: none;  */
  position: fixed;
  top:0;
  left: 0;
  right: 0;
  background-color: white;
  height: 50px;
  box-shadow: 0 0 3px rgb(160, 159, 159);
  /* margin: 0; */
  text-align: center;
}
#pages a{
  display: inline-block;
  margin: 0 auto;
  /* height: 50px; */
  /* text-align: center; */
  color: inherit;
  text-decoration: none;
  /* position: absolute;
  top: 20px; */
  padding-top: 15px;
  padding-left: 20px;
  padding-right: 20px;
  padding-bottom: 0;
  font-size: 10;
  color: rgb(138,148,169);
  transition: all 0.3s ease;
}
#pages a:hover{
  color: black;
}
#logo{
  /* all: unset !important; */
  position: relative;
  margin-left: 20px;
  margin-right: 20px;
}
#return{
  /* all: unset !important; */
  position: relative;
  right: 100px;
  bottom: 5px;
  margin-left: 20px;
  margin-right: 20px;
}
.logo{
  /* display: inline-block;
  margin: 0 auto;
  margin-top: 10px;*/
  padding-right: 20px;
  height: 30px;
  position: absolute;
  top:-3px;
  right: -35px;
  cursor: pointer;
  transition: all 0.1s ease
}
.logo:hover{
  transform: scale(1.05);
}
.logo:active{
  transform: scale(0.99);
}
#pages{
  display: inline-block;
}
/* .navbar svg rect{
  position: absolute;
  height: 2px;
  width: 40px;
  color: #ADD8E6;
} */
.rect{
  position: absolute;
  height: 2px;
  width: 40px;
  color: #ADD8E6;
}
/* .light{

} */
.light::before{
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.5); 
  z-index: 1; 

}
/* .fade-leave-active {
  transition: opacity 0.1s ease;
}
.fade-leave-to {
  opacity: 0;
}
.fade-enter-active{
  transition: opacity 0.1s ease;
}
.fade-enter-from{
  opacity: 0;
}
.fade-enter-to{
  opacity: 1;
} */
</style>
