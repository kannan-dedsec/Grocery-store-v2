<template>
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

  
  <div v-else>
  
    <navbar :isNotLoginPage="isNotLoginPage" :allowSearching="allowSearching" :isAuthenticated="auth" style="z-index: 1000;" ></navbar>
   
    <tabs v-if="(auth && hasStore) || isAdmin "  :isAdmin=isAdmin ></tabs>
    <div v-else-if="auth && created" class="center-container">
        <div class="centered-text">
        <h1>Store Submitted </h1>
        <p>kindly wait till Admin approve your request</p>
        </div>
    </div>
    <div v-else-if="auth ">
        <div class="center-container">
            <div class="centered-text">
                <form @submit.prevent="submitForm">
                <div>
                    <h5 class="card-title text-dark">Set up your Store</h5>
                    <div class="form-group">
                    <label for="loginUsername">Store Name : </label>
                    <input type="text" class="form-control" id="loginUsername" v-model="storeName" required>
                    </div>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
    </div>
    <div v-else-if="!auth" class="center-container">
        <div class="centered-text">
        <h1>Not Authorized :(</h1>
        <p>kindly Login and try again.. </p>
        <a href="/login" target="_blank">login</a>
        </div>
    </div>

    <popUpNotification ref="notification"></popUpNotification>
  </div>
</template>

<script>
import navbar from '@/components/navbar.vue'
import tabs from '@/components/tabs.vue'
import request from '@/services/apiService'
import {GET_DATA_ROUTE,GET,POST,AUTH,PUT_DATA} from '@/services/constants.js'
import popUpNotification from '@/components/popUpNotification.vue'

export default {
  data(){
    return {
      auth : false,
      hasStore: false,
      created: false,
      isNotLoginPage: true,
      allowSearching:false,
      isAdmin: false,
      storeName:"",
      loading:true
    }
  },
  mounted()  
  {
     
    this.isAuthenticated()
    this.getStore()
    setTimeout(() => {this.loading = false;}, 1500); 
  },
  methods: {
    async getStore()
    {
      var body = {type:7}
      const {success, data, error} = await request(GET_DATA_ROUTE,POST,body)
      console.log(data,success,error)
      if(success)
      {
        if(data.avail)
        {
            this.created = true;
            this.hasStore = data.isApproved;
            this.isAdmin = data.isAdmin

        }
        else
        {
            this.hasStore = false;
            this.created = false;
        }
      }
    },
    async isAuthenticated()
    {
      const {success, data, error} = await request(AUTH)
      this.auth = success
    },
    async submitForm()
    {
        const storeData  = {
                store : this.storeName,
                type : 6
            }
            
            if (!this.storeName) 
            {
                alert('Please fill in all mandatory fields.');
                return;
            }

            const {success, data, error} = await request(PUT_DATA,POST,storeData)
            
            if(success)
            {
                if(data.success)
                {
                    this.$refs.notification.showSuccess('store added successfully');
                    this.created = true
                }
                else
                {
                    this.$refs.notification.showError('Error : '+ data.message);
                }
            
            }
            else
            {
                this.$refs.notification.showError('Error : contact support');
            }
    }
  },
  components: {
    navbar,
    tabs,
    popUpNotification
  }
}
</script>

<style>
    .center-container {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 90vh;
    }

    .centered-text {
      text-align: center;
    }

    .loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.8);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .spinner-container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .spinner {
    margin-bottom: 20px;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

</style>
