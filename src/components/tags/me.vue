<template>
  <div>
    <p>用户:{{ username }}</p>
    <p>UID:{{ uid }}</p>
    <p>我的miCoin:{{ mic }}</p>
    <RouterLink to="/newpost" class="func" style="margin-bottom: 15px;">我要发帖</RouterLink>
    <RouterLink to="Dev Infomation"></RouterLink>
    <a @click="unregister" class="close">退出登录</a>
  </div>
</template>

<script>
import global from '@/global'
import axios from 'axios'
export default {
  data(){
    return{
      
    }
  },
  props:['username','uid','logged','token','mic'],
  methods:{
    unregister(){
      global.popup("退出登录中(●'◡'●)",1)
      if (this.logged){
        this.$cookies.remove('token')
        axios.post(global.url + '/api/token/remove'
        ,JSON.stringify({'token':this.token}))
        this.$router.go(0)
      }
    },
    
  }
}

</script>

<style scoped>

a{
  display: block;
  text-decoration: none;
}
div{
  padding: 20px;  
}
p{
  margin: 0;
  /* display: block; */
}
.close{
  /* position: absolute; */
  /* top: 23px;
  right: 15px; */
  color: rgb(0, 145, 255);
  cursor: pointer;
  transition: all .3s ease;
  /* display: none; */
}
.close:hover{
  color: red;
}
.func{
  color: rgb(0, 145, 255);
  cursor: pointer;
  transition: all .3s ease;
}
.func:hover{
  color: #61baff;
}
</style>
