<template>
  <!-- <toppost></toppost> -->
  <div style="z-index: 9999;" id="pv" v-for="i in recm">
      <pv :er="er" :post_id=i :logged=logged></pv>
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
    pv,
  }
  ,
  data(){
    return{
      data:[],
      show:false,
      recm:[],
    }
  },

  methods:{
    trs(){
      this.show = true
    }
  },
  mounted(){
    document.title = "主页" + global.title
    axios.get(global.url + "/hp/com").then(res => {
      this.recm = res.data.posts
    })
  },
  props:['logged']
}
</script>

<style>
#pv{
  transition: all 1ms ease;
}
</style>
