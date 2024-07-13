<template>
    <navbar :isNotLoginPage="isNotLoginPage" :allowSearching="allowSearching" :isAuthenticated="auth" style="z-index: 1000;" ></navbar>
 
    <ProductList sliderId="topProducts" title="Cart Items" :isHomepage="isHomepage" :editMode="editMode" :cartMode="cartMode"  :products="productData"></ProductList>
</template>

<script>
  import navbar from '@/components/navbar.vue'
  import ProductList from '@/components/ProductList.vue'
  import request from '@/services/apiService'
  import {GET_DATA_ROUTE,GET,POST,AUTH} from '@/services/constants.js'

  export default {
    data(){
      return {
        auth : true,
        isNotLoginPage: true,
        allowSearching:false,
        isHomepage:true,
        editMode:false,
        cartMode:true,
        productData:[]
      }
    },
    mounted()  
    {
      this.isAuthenticated()
      this.getData()
    },
    methods: {
      async getData()
      {
        var body = {type:10,offset:0,limit:10000}
        const {success, data, error} = await request(GET_DATA_ROUTE, POST, body)
        if(success)
        {
           this.productData = data.cart_items
        }
        
      },
      async isAuthenticated()
      {
        const {success, data, error} = await request(AUTH)
        this.auth = success
      }
    },
    components: {
      navbar,
      ProductList
    }
  }

</script>