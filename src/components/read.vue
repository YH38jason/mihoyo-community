<template>
  <div class="main">
    <h2>{{ post_title }}</h2>
    <audio v-if="Boolean(audioURL)" 
    :src='audioURL' controls
    style="width: 300px;height: 30px;">
    </audio>
    <br><br>
    <span class="scrnav">
      <a id="imgnum" class="func" title="点击查看图片" @click="scrolltoimg"
      >{{ imageNum }}张图片 </a>
      <a id="imgnum" class="func" title="点击查看评论" @click="scrolltocom"
      >{{ comment_list.length }}条评论<br><br></a>
    </span>
    <div class="content text-content">
      {{ content }}
    </div>
    <br>
    <span id="images" class="images"></span>
    <div class="btns">
      <button id="like" :disabled="!logged" @click="likebtn">赞同 {{ likes }}</button>
      <br>
      <p>发帖人 Poster: <span class="new-post">{{ poster }}</span></p>
    </div>
    <div>
      <input class="comment" id="in" :placeholder="commenthp" v-model.trim="comment" :disabled="!logged">
      <button @click="commit_com" class="commit" :disabled="!logged">提交</button>
      <h3 style="font-weight: normal; padding-bottom: 10px;"> {{comment_list.length}} 评论♪</h3>
    </div>
    <div v-if="key">
      <div class="comment-block" v-for="comment in comment_list">
      <p class="user">{{ comment[3] }}</p><br>
      <p class="time">{{ comment[4] }}</p><br>
      <p class="content">{{ comment[2] }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import global from '@/global'
import axios from 'axios'
import { nextTick } from 'vue'
// import { nextTick } from 'vue'
export default {
  // mounted(){
  props:['username'],
  // },
  data(){
    return{
      content:"",
      post_title:"",
      likes:0,
      comment:"",
      post_id:this.$route.params.id,
      comment_list:[],
      key:true,
      // logged:false,
      commenthp:'发表评论',
      user_id:0,
      _temp:'',
      liked:false,
      poster:'',
      images:[],
      imgaeNum:0,
      imagesPos:0,
      audioURL:'',
      audioFn:'',
    }
  },
  props:['logged','uid','username'],
  beforeMount(){
    // 请求帖子
    axios.get(global.url + '/post/' + 
      this.post_id + "/content").then(res => {
      if (res.data.status){
        global.popup('帖子不存在或已被删除~')
        setTimeout(() => {
          this.$router.go(-1)
        },1500)
        return
      }
      this.content = res.data.content
      this.post_title = res.data.title
      this.likes = res.data.likes
      this.poster = res.data.poster
      let images = res.data.images
      images = eval(images)
      // console.log(images)
      for (let i of images){
        let img = document.createElement('img')
        img.style.height = '160px';
        img.style.marginRight = '20px'
        img.style.cursor = 'pointer'
        let a =document.createElement('a')
        a.href = global.url + '/api/file/get/' + i
        img.src = a.href
        a.target = '_blank'
        a.appendChild(img)
        let s = document.getElementById('images')
        s.appendChild(a)
        this.$nextTick(() => {
          setTimeout(() => {
            let targetbox= document.getElementById('imgnum');
            this.imagesPos = targetbox.offsetTop;        
        })
        })
      }
      let audio = res.data.audio
      if (audio != null){
        this.audioURL = global.url + '/api/file/get/' + audio
      }
      // console.log(images.length)
      this.imageNum = images.length
    })
    document.title = "浏览帖子" + global.title
    this.quary_comment()
    // console.log(this.logged)
    if (!this.logged){
      this.commenthp = '请先登录以发表评论'
    }else{
      this.user_id = this.uid
    }
  },
  methods:{
    scrolltoimg(){
      document.getElementById('images').scrollIntoView()
    },
    scrolltocom(){
      document.getElementById('in').scrollIntoView()
    },
    openLargeImage(event){
      window.open(event.src)
    },
    getTime(){
      return new Date()
    },
    com_user(uid){
      // let username = ''
      if (uid == 0){
        return "匿名用户"
      }
      axios.get(global.url + "/api/user/uid/" + uid).then(res=>{
        this._temp = res.data.info[1]
      })
      return this._temp
    },
    commit_com(){
      if (this.comment == ""){
        return
      }
      if (!this.logged){
        return
      }
      axios.post(global.url + "/post/"+this.post_id
      +"/comment/commit", JSON.stringify(
        {'content':this.comment, "id":this.post_id,'uid':this.user_id, 
        'time':this.getTime()}),
      {headers:{"Content-Type":"application/json"}}).then(res => {
        if (res.data.status){
          global.popup("评论提交异常:" + res.data.status)
        }
      })

      this.comment_list.unshift(
        [0, this.post_id, this.comment, this.username,this.getTime()])
      this.comment = ""
      console.log(this.comment_list)
      this.fresh()
    },
    quary_comment(){
      axios.get(global.url + '/post/' + 
    this.post_id + "/comment").then(res => {
      this.comment_list = res.data.comments
      // console.log(res.data.comments)
    })
    
    },
    fresh(){
      this.key = false
      nextTick(()=>{
        this.key = true
      })
    },
    likebtn(){
    // 是否登录
    if (!this.logged){
      return
    }
    axios.post(global.url + '/post/' + this.post_id + '/like', 
    JSON.stringify({'uid':this.uid})).then(res => {
      let status = res.data.status
      if (status){
        if (status == 2){
          global.popup('自己给自己点赞,搁这卡bug?', 1)
        }else{
          global.popup('这个帖子已经赞过了哦~不如去给站长打赏:)')
        }
      }else{
        console.log(this.uid)
        this.likes += 1
        global.popup("点赞成功,帖子有可能会被推荐哦~",1)
      }
    })
    
    },
    },
  }

</script>

<style scoped>
.scrnav a{
  display: inline;
}
.images{
  margin-top: 30px;
}
#imgnum{
  cursor: pointer;
  /* margin-bottom: 30px; */
}

.time{
  font-size: 5px;
  font-weight: lighter;
  margin-bottom: 20px;
  border-bottom: 1px black solid;
}
.main{
    /* box-shadow:  0 0 3px rgb(160, 159, 159); */
    /* text-align: center; */
    background-color: rgb(255, 255, 255);
    /* border-radius: 6px; */
    margin: 0 28% 0 28%;
    /* height: 200px; */
    padding: 15px 25px 15px 25px;
    margin-bottom: 30px;
}

/* .btns{
  margin: 5px;
} */
.func{
  color: rgb(0, 145, 255);
  cursor: pointer;
  transition: all .3s ease;
  display: inline;
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
.comment{
  background-color: rgb(255, 255, 255);
  border: solid rgb(215, 214, 214) 1px;
  height: 35px; 
  width: 85%;
  /* margin-left: ; */
  margin-top: 20px;
  display: inline-block;
  border-radius: 5px;
  transition: all 0.1s ease;
  padding-left:10px
}
.comment:focus{
  outline: none;
  background-color: rgb(239, 239, 239);
  border: none;
}
.comment:disabled{
  cursor: pointer;
}
.commit{
  display: inline-block;
  height: 35px;
  border-radius: 5px;
  margin-left: 16px;
  width: 10%;
  outline: none;
  border: none;
  background-color: rgb(79,164,219);
  cursor: pointer;
}
.commit:hover{
  background-color: rgb(105, 174, 221);
}
.comment-block{
  white-space: pre;
  margin-bottom: 16px;
  cursor: pointer;
  background-color: white;
  transition: background-color .1s ease;
  padding: 10px;
}
.comment-block:hover{
  background-color: rgb(239, 239, 239);
}
.user{
  font-weight: normal;
}
#text{
  margin-bottom: 40px;
}
.content{
  font-weight: lighter;
  white-space: pre;
  word-wrap:break-word;  
  word-break:break-all;
  width: 95%; 
  
}
.text-content{
  white-space: pre;
  overflow:scroll;
  overflow-y:hidden;
  word-wrap:break-word;  
  word-break:break-all;
  padding-bottom: 25px;
}
.comment-block p{
  margin: 0;
  display: inline-block;
  white-space: pre;
}
.new-post{
  color: rgb(0, 145, 255);
  cursor: pointer;
  transition: all .3s ease;
}
.new-post:hover{
  color: #61baff;
}
.func:hover{
  color: #61baff;
}
</style>
