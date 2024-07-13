<template>
  <div class="border border-light">
    <br />
    <h3 class="navbar-brand ml-2 mt-2 ">{{title}}</h3>
    <br>
    <div v-if="hasData" class="inner">
      <div class="row">
        <div v-for="cat in categories" :key="cat.category_id" class=" mb-4">
          <Category @editCatModal="editCatModal" :id=cat.category_id :editMode=editMode :title="cat.category_name" :image="cat.image" />
        </div>
      </div>
      <popUpNotification ref="notification"></popUpNotification>
      <!-- modal start -->

      <div class="modal fade" id="categoryModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Edit Category</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveProduct">
              <div class="form-group">
                <label for="productName">Category Name:</label>
                <input v-model="this.categoryName" id="productName" class="form-control" required />
              </div>
              <button type="submit"  class="btn btn-primary">Save</button>
              <button type="button" class="btn btn-secondary" style="margin-left:308px" data-dismiss="modal">Cancel</button>
            </form>
          </div>
          <div class="modal-footer">
          </div>
        </div>
      </div>
    </div>

      <!-- modal ends -->
    </div>
    <div v-else class="text-center mt-3">
        <p>No data available</p>
      </div>
  </div>
</template>

<script>
import Category from './category.vue';
import request from '@/services/apiService'
import {CHECK_OUT,POST,GET_DATA_ROUTE,GET,GET_GUEST_DATA,AUTH,PUT_DATA,UPDATE_DATA} from '@/services/constants.js'
import popUpNotification from '@/components/popUpNotification.vue'

export default {
  components: {
    Category,
    popUpNotification
  },
  data(){
    return{
      categoryName:''
    }
  },
  props: {
    categories: Array,
    title:String,
    isHomepage:Boolean,
    editMode:Boolean
  },
  computed:{
    hasData(){
      return this.categories.length > 0
    }
  },
  methods :{
    editCatModal(editCatModal) 
    {
      this.categoryName = editCatModal.name
      this.categoryId = editCatModal.id
  
    },
    async saveProduct()
    {
      var dat = { categoryName: this.categoryName, category_id:this.categoryId,type:2 }
                    
      let {success, data, error} = await request(PUT_DATA,POST,dat)

      if(success)
      {
        this.$refs.notification.showSuccess('Updated the category succesfully');
        setTimeout(() => {location.reload()  }, 1000);
      }
      else
      {
        this.$refs.notification.showError('Error : Contact support');
      }
    }
  }
 };
</script>

<style scoped>

.inner {
  padding: 1em;
}

.slider{
  display: flex;
  justify-content: center;
}

@media (max-width: 767px) {
  .col-md-3 {
    flex: 0 0 100%;
    max-width: 100%;
  }
}

@media (min-width: 768px) {
  .col-md-3 {
    flex: 0 0 25%;
    max-width: 25%;
  }
}

</style>
