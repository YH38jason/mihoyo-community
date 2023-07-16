<template>
  <div class="main">
    <RouterLink id="title" :to=url >{{ title }}</RouterLink>
    <RouterLink class="cpv" :to=url>{{ content }}</RouterLink>
    <div class="btns">
      <button @click="like" id="like">赞同 {{ likes }}</button>
    </div>
  </div>
</template>

<script>
import global from '../global'
import axios from 'axios'
export default {
  data(){
    return{
      content:"",
      title:"",
      likes:0,
      url:'/read/' + this.post_id,
      // post_id:1,
      uid:0,
    }
  },
  beforeMount(){
    axios.get(global.url + '/post/' + 
    this.post_id + "/content").then(res => {
      // console.log(res.data.content)
      // console.log()
      let content = res.data.content
      if (content.length > 30){
        // console.log(content.length > 30)
        this.content = '全文' + content.length + '字'
      }else{
        this.content = content
      }
      this.title = res.data.title
      this.likes = res.data.likes
    }).catch()
    if (this.logged){
      this.uid = this.$cookies.get('uid')
    }    
  },
  props:['post_id','logged','er'],
  methods:{
    like(){
    // 是否登录
    // if (!this.logged){
    //   return
    // }
    global.popup('还没点进去就赞，你搁这刷赞呢',1)
    
    }
  }
}

</script>

<style scoped>
  a{
    display: block;
    text-decoration: none;
  }
  #title{
    margin: 0 0 15px 0;
    font-size: 18px;
    text-decoration: none;
    color:black;
    font-weight: bold;
    /* transition: all 0.1s ease; */
  }
  #title:hover{
    color: rgb(79,164,219);
  }
  .cpv{
    font-size: 15px;
    color: #000000;
    /* transition: 0.1s all ease; */
  }
  .cpv:hover{
    color:#8a94a9
  }
  .main{
    border-bottom: solid rgb(240,242,247) 1px;
    background-color: rgb(255, 255, 255);
    margin: 0 28% 0 28%;
    padding: 10px;
    z-index: 9999;
}
  .btns{
    margin: 20px 5px 5px 0px;
  }
  #like{
    border-radius: 1px;
    border: none;
    /* transition: all 0.1s ease; */
    height: 30px;
    width: 50px;
    color: rgb(42, 148, 218);
    background-color: rgb(230,240,253);
    cursor: pointer;
    /* transition: all 0.2s ease; */
  }
  #like:hover{
    background-color: rgb(201, 225, 255);
  }
  /* .btns button img{
    height: 20px;
    width: 20px;
    transition: all 0.1s ease;
  } */
  /* .btns button img:hover{
     content: url("../assets/like-act.png"); 
  } */
</style>
