<template>
  <div>
    <input style="margin-top: 35px!important;" placeholder="用户名" v-model="userName">
    <input type="password" placeholder="密码" v-model="password">
    <a @click="switchReg" title="点我注册">没有账号?注册一个ヾ(≧▽≦*)o</a>
    <button class="confirm" @click="login">确定</button>
  </div>
</template>

<script>
import global from '@/global'
import axios from 'axios';
import { Md5 } from 'ts-md5';
// import login from '@/components/login.vue'
export default {
  methods:{
    login(){
      if (!this.userName || !this.password) {
      global.popup("怎么还带留空的￣へ￣",0)}
      // MD5加密
      const md5 = new Md5()
      md5.appendStr(this.password)
      this.passwordMD5 = md5.end()
      axios.post(global.url + '/api/login', 
      JSON.stringify({'username':this.userName, 'password':this.passwordMD5})).then(res => {
        if (res.data.status){
         global.popup("用户名或密码错误(¬_¬ ):" + res.data.status) 
        }else{
          global.popup("登录成功,请等待q(≧▽≦q)",1)
            this.$cookies.set("uid", res.data.uid)
            this.$cookies.set('token',res.data.token)
            this.$router.go(0)
        }
      })
    },
    switchReg(){
      this.$emit('switchstatus')
    }
  },
  data(){
    return{
      userName:"",
      password:"",
      passwordMD5:'',
    }
  },
}

</script>

<style scoped>
a{
  color: rgb(0, 145, 255);
  font-size: 5px;
  cursor: pointer;
  display: block;
  text-align: center;
  user-select: none;
}
a:hover{
  color:#00448e;
}
input {
  /* margin: 10px 0 10px 20px; */
  margin: 10px auto;
  padding-right: 5%;
  width: 240px;
  height: 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  font-size: 16px;
  color: #333;
  background-color: #f5f5f5;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  display: block;
  transition: 0.2s all ease;
}

input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.confirm{
  position: absolute;
  left: 50%;
  bottom: 10px;
  transform: translate(-50%, 0);
  height: 30px;
  width: 120px;
  border-radius: 5px;
  outline: none;
  border: none;
  cursor: pointer;
  background-color: rgb(240,240,240);
}
.confirm:hover{
  background-color: rgb(221, 221, 221);
}
.confirm:active{
  background-color: rgb(240,240,240);
}


</style>
