<template>
    <navbar :isNotLoginPage="isNotLoginPage" :allowSearching="allowSearching" :isAuthenticated="auth" style="z-index: 1000;" ></navbar>
<br>
    <div v-if="loading" class="loading-overlay">
    <div class="spinner-container">
      <svg
        class="spinner bi bi-hourglass"
        width="50px"
        height="50px"
        viewBox="0 0 16 16"
        fill="currentColor"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M1 0h14a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V1a1 1 0 0 1 1-1zm1 2a1 1 0 0 1 1 1v4.755l1.574-1.574a1 1 0 0 1 1.45.11l1 1a1 1 0 0 1 .108 1.341l-1.158 2.316a4.982 1 90 0 0-.108.157 2 2 0 1 0 3.978 0 4.982 1 90 0 0-.108-.157l-1.158-2.316a1 1 0 0 1 .108-1.341l1-1a1 1 0 0 1 1.45-.11L14 7.755V3a1 1 0 0 1 1-1H2z" />
      </svg>
      <p>Loading...</p>
    </div>
  </div>

  <div class="ml-2" v-else>
      <h2>Order List</h2>
      <table class="table">
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Items</th>
            <th>Purchased On</th>
            <th>Total Price</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(order, index) in orders" :key="index">
            <td>{{ order.order_id }}</td>
            <td>
              <ul>
                <li v-for="(item, i) in order.items" :key="i">
                  {{ item.item_name }} ({{ item.count }} x ${{ item.price }})
                </li>
              </ul>
            </td>
            <td>{{ order.purchased_on }}</td>
            <td>${{ order.total_price }}</td>
          </tr>
        </tbody>
      </table>
    </div>
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
        isHomepage:true,
        editMode:false,
        cartMode:true,
        allowSearching:false,
        orders:[],
        viewMode:true,
        loading:true
      }
    },
    mounted()  
    {
      setTimeout(() => {this.loading = false;}, 500); 
      this.isAuthenticated()
      this.getData()
    },
    methods: {
      async getData()
      {
        var body = {type:5,offset:0,limit:10000}
        const {success, data, error} = await request(GET_DATA_ROUTE, POST, body)
        if(success)
        {
           this.orders = data.products
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