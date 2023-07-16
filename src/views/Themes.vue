<template>
  <div>
    <div class="main" v-for="i in themes">
    <img class="ico" :src="i[1]"  >
    <span class="message">{{ i[3][Math.floor(Math.random()*i[3].length)] }}</span>
    <RouterLink :title="i[3][Math.floor(Math.random()*i[3].length)]" 
    id="title" :to="'theme/' + i[2]" ><b>{{ i[0][0] }}</b> <span style="font-size: 14px;">{{ i[0][1] }}</span></RouterLink>
    </div>
  </div>
</template>

<script>
import global from '@/global'
export default {
  data(){
    return{

    }
    
  },
  props:['themes'],
  methods:{
    getImgUrl(img){
      // console.log('../assets/' + img)
      return '../assets/' + img  
    },
  },
  mounted(){
    console.log()
    document.title = "米游" + global.title
    // document.getElementById('title')
    // .addEventListener('mouseenter',)
  }
}

</script>

<style scoped>
  a{
    display: inline-block;
    text-decoration: none;
    margin-left: 10px;
    vertical-align: top;
    position: relative;
    left: 25px;
  }
  #title{
    margin: 0 0 15px 0;
    font-size: 18px;
    text-decoration: ·none;
    color:black;
    /* font-weight: bold; */
    /* transition: all 0.1s ease; */
  }
  #title:hover{
    color: rgb(79,164,219);
  }
  .main{
    position: relative;
    background-color: rgb(255, 255, 255);
    margin: 0 28% 0 28%;
    padding: 15px 25px 15px 25px;
    border-bottom: solid rgb(240,242,247) 1px;
}
  img{
    display: inline-block;
    width: 100px;
    height: 100px;
    border-radius: 15px;
    margin: 0 0 0 10px;
    cursor: pointer;
  }
  .message{
    position: absolute;
    bottom: 20px;
    left: 160px;
    opacity: 0;
    transition: opacity .2s ease;
    color: gray;
  }
  .ico:hover+.message{
    opacity: 1;
  }
  #title:hover+.message{
    opacity: 1;
  }

</style>
