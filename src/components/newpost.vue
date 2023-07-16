<template>
  <div class="main">
    <input class="title-input" placeholder="标题" style="margin-left: 30px" v-model.trim="title">
    <textarea style="
    width: 80%;
    margin-left:30px;
    height: 300px;" 
    placeholder="说点什么吧..." v-model.trim="content"></textarea>
    <p style="margin-left: 30px;user-select: none;">我的UID: {{ uid }}</p>
    <div class="radios">
      <input type="radio" v-model="picked" value="hksr" id="hksr">
      <label for="hksr">崩坏：星穹铁道</label>
      <input type="radio" v-model="picked" value="genshin" id="genshin">
      <label for="genshin">原神</label>
      <input type="radio" v-model="picked" value="hk3" id="hk3">
      <label for="hk3">崩坏3</label>
      <input type="radio" v-model="picked" value="zzz" id="zzz">
      <label for="zzz">绝区零</label>
      <input type="radio" v-model="picked" value="other" id="other" checked="true">
      <label for="other">其他</label>
    </div>
    <span style="position: relative;">
      <!--Image-->
      <span style="border: 1px solid #ccc;
            padding: 2px;
            padding-bottom: 5px;
            margin: 0 10px 15px 30px;">
        <input class="file" type="file" id="upload"
          @change="handleFile">
      </span>
      <button style="margin-right: 10px;" @click="sendFile(0)">插入</button>
      <!--Audio-->
      <span><button @click="clearImages">清除</button></span>
      已插入{{ images.length }}张
      <br>
        <span style="border: 1px solid #ccc;
            padding: 2px;
            padding-bottom: 5px;
            margin: 0 10px 15px 30px;">
        <input class="file" type="file" id="uploadaudio" :disabled="Boolean(audioFileName)"
          @change="handleAudio">
        </span>
        插入音频&nbsp;&nbsp;&nbsp;
        <span v-show="audioFileName"><button @click="clearAudio">清除</button></span>
    </span>
    <button class="send" @click="send">发表</button>
  </div>
</template>

<script>
import axios from 'axios';
import global from '@/global';
// import router from '@/router';

export default {
  data(){
    return{
      title:'',
      content:'',
      picked:'other',
      selected:false,
      selectedFile:null,
      selectedAudio:null,
      url:global.url,
      images:[],
      audioFileName:'',   
}
  },
  methods:{
    clearAudio(){
      this.audioFileName = ''
    },
    handleFile(event){
      this.selectedFile = event.target.files[0];
      // console.log(this.selectedFile.name)
      // global.popup('不是音频！')
    },
    handleAudio(event){
      this.selectedAudio = event.target.files[0];
      console.log("Insert Audio")
      this.sendFile(1)
    },
    sendFile(type = 0){
      if (type){
        
        var audioTypes = ['.mp3']
        if (this.checkType(audioTypes,0) == -1){
          global.popup('不是音频！')
          return
        }
        global.popup('文件校验成功',1)
        let formData = new FormData();
        formData.append('file',this.selectedAudio)
        axios.post(global.url + '/api/file/upload',formData,{
          headers:{"Content-Type":'multipart/form-data'},
        }).then(res => {
          if (res.data.status){
            global.popup('Upload失败' + res.data.status);
          }else{
            global.popup('音频上传成功',1)
            // this.insertImage(res.data.fn)
            this.audioFileName = res.data.fn
            this.selectedAudio = null
            let upload = document.getElementById('uploadaudio')
            upload.type = 'text'
            upload.value = ''
            upload.type = 'file'
        }
      })
        return
      }
      if (this.selectedFile == null){
        return
      }
      let imglist = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".jfif"];
      let result = null
      result = this.checkType(imglist,1)
      if (result == -1){
        // console.log(result)
        global.popup('不是图片！')
        return
      }      
      global.popup('文件校验成功,Uploading...',1)
      this.selected = true
      // 上传图片
      let formData = new FormData();
      formData.append('file',this.selectedFile)
      axios.post(global.url + '/api/file/upload',formData,{
        headers:{"Content-Type":'multipart/form-data'},
      }).then(res => {
        if (res.data.status){
          global.popup('Upload失败' + res.data.status);
        }else{
          global.popup('上传成功*^____^*',1)
          this.insertImage(res.data.fn)
          this.selectedFile = null
          let upload = document.getElementById('upload')
          upload.type = 'text'
          upload.value = ''
          upload.type = 'file'
        }
      }).catch(this.er)
    },
    clearImages(){
      this.images = []
    },
    insertImage(filename){
      this.images.push(filename)
    },  
    checkType(items, file){
      let typeOK = false
      if (file){
        for (let i of items){
        typeOK = this.selectedFile.name.toLowerCase().search(i)
        if (typeOK != -1){
          return typeOK
        }
        // console.log(typeOK)
        }
        // console.log(typeOK)
        return typeOK
      }else{
        for (let i of items){
        typeOK = this.selectedAudio.name.toLowerCase().search(i)
        if (typeOK != -1){
          return typeOK
        }
        // console.log(typeOK)
        }
        // console.log(typeOK)
        return typeOK
      }
    },
    send(){
      // console.log(this.picked)
      if (!this.title || !this.content){
        global.popup('不能发送空内容￣へ￣')
        return
      }
      axios.post(global.url + '/api/newpost',
      JSON.stringify({'title':this.title,'content':this.content,
          'uid':this.uid,
          'theme':this.picked,
          'images':this.images,
          'audio':this.audioFileName,
        }))
          .then(res=>{
        if (!res.data.status){
          global.popup('发表成功(●\'◡\'●)',1)
          this.$router.push('/')
        }else{
          global.popup('发表失败:' + res.data.status)
        }
      }).catch(this.er)
    }
  },  
  props:['logged','uid','er'],
  mounted(){
    document.title = '发帖' + global.title
    if (!this.logged){
      // console.log(this.logged)
      this.$router.push('/')
    }
    // console.log(this.picked)
  }
}

</script>

<style scoped>
.file{
  margin:0 10px 15px 0px;
}
.file+button{
  display: inline;
  /* position: absolute; */
  /* right: 100px; */
}
.radios{
  margin: 15px;margin-left: 30px;
  border: 1px solid #ccc;border-radius: 3px;
  margin-right: 40%;padding: 5px;
}
.radios input{
  cursor: pointer;
}
.title-input {
  /* margin: 10px 0 10px 20px; */
  margin: 10px;
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

.title-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

label{
  cursor: pointer;
}

.main{
    /* border-bottom: solid rgb(240,242,247) 1px; */
  background-color: rgb(255, 255, 255);
  margin: 0 28% 0 28%;
  padding: 10px;
}

textarea{
  margin: 10px;
  padding-right: 5%;
  width: 240px;
  height: 12px;
  border: 1px solid #ccc;
  /* border-radius: 5px; */
  padding: 10px;
  font-size: 16px;
  color: #333;
  display: block;
  transition: 0.2s all ease;
  resize: none;
  outline: none;
  /* border: none; */
}
/* textarea:focus{
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
} */
.send{
  background-color: rgb(79,164,219);
  /* margin: 0 auto; */
  border: none;
  padding: 4px;
  border-radius: 4px;
  display: block;
  /* text-decoration: none; */
  /* text-align: center; */
  color: black;
  transition: all 0.1s ease;
  margin-left: 30px;
}
.send:hover{
  background-color: rgb(86, 187, 255);
}
.send:active{
  transform: scale(0.9);
}
</style>
