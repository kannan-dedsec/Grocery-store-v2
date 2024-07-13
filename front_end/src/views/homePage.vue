<template>
    <navbar :isNotLoginPage="isNotLoginPage" :allowSearching="allowSearching" :isAuthenticated="auth" @search="search" style="z-index: 999;" ></navbar>
    
    <loading v-if="loading"></loading>
    <div v-else>
     
      <ProductList :viewMode="viewMode" sliderId="topProducts" title="Products" :isHomepage="isHomepage" :editMode="editMode" @filter="filter" :products="productData"></ProductList>
      <br><br>
      
    </div>
</template>
  
  <script>
  import navbar from '@/components/navbar.vue'
  import categoryList from '@/components/categoryList.vue'
  import ProductList from '@/components/ProductList.vue'
  import request from '@/services/apiService'


  import {GET_GUEST_DATA,GET,POST,AUTH} from '@/services/constants.js'

  export default {
    data(){
      return {
        auth : true,
        isNotLoginPage: true,
        allowSearching:true,
        isHomepage:true,
        editMode:false,
        productData:[],
        viewMode:false
      }
    },
    mounted()  
    {
      this.isAuthenticated()
      if(this.productData.length <= 0 )
      {
        this.getData()
      }
      
    },
    methods: {
      async getData()
      {
        var body = {type:2,offset:0,search_type:1,limit:10000}
        const {success, data, error} = await request(GET_GUEST_DATA,POST,body)
        
        if(success)
        {
           this.productData = data.products
        }
        
      },
      async isAuthenticated()
      {
        const {success, data, error} = await request(AUTH)
        this.auth = success
      },
      async search({ option, query })
      {
        if(option === "Product")
        {
          var body = {type:2,offset:0,search_type:1,params:query,limit:10000}
          const {success, data, error} = await request(GET_GUEST_DATA,POST,body)
          
          if(success)
          {
            this.productData = data.products
          }
        
        }
        else if (option === "Category")
        {
          var body = {type:2,offset:0,search_type:12,params:query,limit:10000}

          const {success, data, error} = await request(GET_GUEST_DATA,POST,body)
          
          if(success)
          {
            this.productData = data.products
          }
         
        }
      
      },
      filter(filter) 
      {
        console.log("in emit "+filter.filter)
          this.productData = filter.filter
      },
     
      
    },
    components: {
      navbar,
      categoryList,
      ProductList
    }
  }
  </script>
  