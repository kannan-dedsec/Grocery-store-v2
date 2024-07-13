<template>
      <div class="container box"> 
        <div class="card"  style="z-index: -999;"> 
          <div class="card-header">
            {{ title }} <a v-if="editMode" @click="editProduct(title,id)" style="display:inline;margin-left: 10px;" data-toggle="modal" data-target="#categoryModal" class="btn btn-outline-primary">Edit</a>
          </div>
          <div class="card-body">
            <div v-if="image"> 
                <img class="grid-image border" :src="image"  alt="Category Image" />
            </div>
            <div v-else> 
                <img class="grid-image border" :src="require(`@/assets/category.png`)" alt="Category Image" />
            </div>
          </div>
        </div> 
    </div>

  <popUpNotification ref="notification"></popUpNotification>
</template>

<script>
  import request from '@/services/apiService'
  import {ADD_DATA,GET,POST,AUTH,PUT_DATA,GET_GUEST_DATA,GET_DATA_ROUTE,REMOVE_DATA} from '@/services/constants.js'
  import popUpNotification from '@/components/popUpNotification.vue'


export default {
  data(){
    return{
      categoryName:this.title
    }
  },
  props: {
    id:String,
    title: String,
    image: String,
    editMode:Boolean
  },
  components:{
    popUpNotification
  },
  methods:{
   
    editProduct(title,id)
    {
      this.$emit('editCatModal',{name:title,id:id}); 
    }
  }

};
</script>

<style scoped>


.card { 
    width: 20rem;
    height : 15rem;
    overflow: hidden; 
} 

.card img{
  width: 100%; 
      height: 100%; 
      object-fit: cover;
}

.image-grid-container
{ 
    display: grid;  
    grid-template-columns: repeat(2, 1fr); 
} 

.box {
  transition: transform 0.3s ease; 
}

.box:hover {
  transform: scale(1.1);
}

.grid-image
{ 
    width: 100%; 
} 

.category {
  border: 1px solid #ddd;
  padding: 15px;
  margin: 10px;
  
}

</style>
