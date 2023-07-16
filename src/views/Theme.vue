<template>
  <div class="main">
    <img :src="theme_info[1]"  >
    <RouterLink v-if="theme_info[0]" id="title" to="" ><b>{{ theme_info[0][0] }}</b> <span style="font-size: 14px;"
      >{{ theme_info[0][1] }}</span></RouterLink>
  </div>
  <div class="main" v-if="noPost">
    <div class="no-post">
      <h3>前面的区域，以后再来探索吧！</h3>
      <p>该游戏暂无帖子</p>
    </div>
  </div>
  <div id="pv" v-for="i in recm" v-else>
      <pv :post_id=i :logged=logged></pv>
  </div>
</template>

<script>
import global from '@/global'
import axios from 'axios'
import pv from '../components/preview.vue'
// import toppost from '../components/top.vue'
// import gb from '../global'
export default {
  name: 'HomeView',
  components: {
    pv
  }
  ,
  data(){
    return{
      data:[],
      show:false,
      recm:[],
      theme:this.$route.params.theme,
      theme_id:{
        'hksr':0,
        'genshin':1,
        'zzz':3,
        'hk3':2,
        'other':4
      },
      theme_info:[],
      noPost:false
    }
  },
  mounted(){
    // console.log(this.theme_id[this.theme])
    axios.post(global.url + "/hp/theme/" + this.theme).then(res => {
      // console.log(res.data.posts)
      this.recm = res.data.posts
      // console.log(this.recm.length == 0)
      if (this.recm.length == 0){
        this.noPost = !this.noPost
      }
    })
    this.theme_info = 
    this.themes[this.theme_id[this.theme]]
    document.title = this.theme_info[0][0] + global.title
    console.log(this.theme_info)
  },
  props:['logged','themes']
}
</script>

<style scoped>
.no-post{
  position: relative;
  top: 50%;
  left: 50%;
  text-align: center;
  transform: translate(-50%,0);
}
#pv{
  transition: all 1ms ease;
}
.main{
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
}

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
    text-decoration: none;
    color:black;
    /* font-weight: bold; */
    /* transition: all 0.1s ease; */
  }
  /* #title:hover{
    color: rgb(79,164,219);
  } */
</style>
