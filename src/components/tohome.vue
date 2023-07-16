<template>
  <p v-if="!serverError">服务器状态检测</p>
  <div v-if="serverError" class="main">
    <img src="../assets/logo.png">
    <p>服务器异常 {{ serverStatusText }}<br><br><i>TECH OTAKUS SAVE THE WORLD</i></p>
    <!-- <button @click="returnHome">返回主页</button> -->
  </div>
</template>

<script>
import global from '@/global'
import axios from 'axios'
export default {
  methods:{
    returnHome(){
      this.$router.push("/")
    }
  },
  mounted(){
    document.title = "System initializing" + global.title
    // axios.post(global.url + '/').then(res => {
    //   console.log(0)
    //   if (res.data.status){
    //     this.$router.push('/error')
    //     this.serverError = true;
    //     this.serverStatusText = res.data.message;
    //     this.$emit('hidnav')
    //     return
    //   }else{
    //     this.$router.push('/home')
    //   }
    //   // this.$router.push('/home')
    // }).catch(
    //   ()=>{
    //     this.$emit('hidnav')
    //     this.serverError = true;
    //     this.serverStatusText = 'IP address of Server Not Found.'
    //   }
    // )
    this.$router.push('/home')
  },
  // props:['et'],
  data(){
    return{
      serverError:false,
      serverStatusText:'',
    }
  }
}

</script>

<style scoped>

img{
  display: block;
  margin: 30px auto;
  padding-top: 30px;
  height: 80px;
}
p{
  text-align: center;
  color: black;
}
button{
  background-color: rgb(79,164,219);
  margin: 0 auto;
  border: none;
  padding: 4px;
  border-radius: 4px;
  display: block;
  /* text-decoration: none; */
  /* text-align: center; */
  color: black;
  transition: all 0.1s ease;
}
button:hover{
  background-color: rgb(86, 187, 255);
}
button:active{
  transform: scale(0.9);
}
.main{
  border-radius: 20px;
  border-bottom: solid rgb(240,242,247) 1px;
  background-color: rgba(255, 255, 255,0.7);
  margin: 0 28% 0 28%;
  padding: 10px;
  z-index: 9999;
  padding-bottom: 30px;
}

</style>
