<template>
  <div>
    <input style="margin-top: 35px!important;" placeholder="用户名" v-model.trim="userName">
    <input type="password" placeholder="密码" v-model.trim="password">
    <input type="password" placeholder="确认密码" v-model.trim="confirmPwd">
    <button class="confirm" @click="register">确定</button>
  </div>
</template>

<script>
import global from '@/global'
import axios from 'axios';
import { Md5 } from 'ts-md5';
// import login from '@/components/login.vue'
export default {
  methods:{
    register(){
      if (!this.userName || !this.password || !this.confirmPwd) {
        global.popup("怎么还带留空的￣へ￣",0)
        return;
      }
      if (this.confirmPwd != this.password){
        global.popup("两个密码对不上诶(＠_＠;)",0)
        return 
      }
      if (this.password.length < 8 || this.password.length > 16){
        global.popup("密码应在8~16位",0)
        return 
      }
      if (!(this.password.search('1234567890') 
      && this.password.search('qwertyuiopasdfghjklzxcvbnm'))){
        global.popup("密码应包含数字和字母",0)
        console.log(this.password.search('qwertyuiopasdfghjklzxcvbnm'))
        return 
      }
      // MD5加密
      const md5 = new Md5()
      md5.appendStr(this.password)
      this.passwordMD5 = md5.end()
      axios.post(global.url + '/api/reg', 
      JSON.stringify({'username':this.userName, 'password':this.passwordMD5})).then(res => {
        if (res.data.status){
          global.popup("注册失败≡(▔﹏▔)≡",0)
        }else{
          // register successful
          global.popup("注册成功，请重新登录ψ(｀∇´)ψ",1)
          this.$router.go(0)
        }
      })
    }
  },
  data(){
    return{
      userName:"",
      password:"",
      confirmPwd:"",
      passwordMD5:'',
    }
  },
}

</script>

<style scoped>
input {
  margin: 10px 0 10px 20px;
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
