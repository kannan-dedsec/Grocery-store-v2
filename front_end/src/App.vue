<template>
  <router-view/>
</template>

<script>
  import navbar from './components/navbar.vue'
  import request from '@/services/apiService'
  import {AUTH} from '@/services/constants.js'

  export default {
    data(){
      return{
        auth : true
      }
    },
    components: {
      navbar
    },
     mounted() {
        this.isAuthenticated()
    } ,  
    methods: {
      async isAuthenticated()
      {
        const {success, data, error} = await request(AUTH)
        this.auth = success
      }
    }
  };
</script>
  