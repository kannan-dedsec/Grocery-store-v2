<template>
    <nav class="navbar  navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="/">Grocery Store</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
  <div v-if="isNotLoginPage" class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="/myOrders">My Orders <span class="sr-only">(current)</span></a>
      </li>
    </ul>
    <ul v-if="allowSearching" class="navbar-nav mr-auto">
       <li class="nav-item">
        <form class="form-outline mx-auto long-search-input" @submit.prevent="search">
                <div class="input-group">
                    <div class="input-group-prepend">
                        <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                          {{ this.selectedOption }}
                        </button>
                        <div class="dropdown-menu">
                            <a class="dropdown-item" @click="selectOption('Product')" href="#">Product</a>
                            <a class="dropdown-item" @click="selectOption('Category')" href="#">Category</a>
                        </div>
                    </div>
                    <input v-model="searchQuery" class="form-control long-search-input" type="search" placeholder="Search Something" aria-label="Search">
                    
                    <div class="input-group-append">
                        <span class="input-group-text">
                          <button class="btn btn-outline-secondary" type="submit">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                                <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="2">
                                    <path stroke-dasharray="16" stroke-dashoffset="16" d="M10.5 13.5L3 21"><animate fill="freeze" attributeName="stroke-dashoffset" begin="0.4s" dur="0.2s" values="16;0"/></path>
                                    <path stroke-dasharray="40" stroke-dashoffset="40" d="M10.7574 13.2426C8.41421 10.8995 8.41421 7.10051 10.7574 4.75736C13.1005 2.41421 16.8995 2.41421 19.2426 4.75736C21.5858 7.10051 21.5858 10.8995 19.2426 13.2426C16.8995 15.5858 13.1005 15.5858 10.7574 13.2426Z"><animate fill="freeze" attributeName="stroke-dashoffset" dur="0.4s" values="40;0"/></path>
                                </g>
                            </svg>
                          </button>
                        </span>
                    </div>
                </div>
            </form>
      </li>
    </ul>
    <ul class="navbar-nav " style="margin-right: 50px;">  
      <li class="nav-item dropdown">
        <a  style="padding-bottom:0px;margin-right: 10px;" class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 20 20"><path fill="currentColor" d="M9.993 10.573a4.5 4.5 0 1 0 0-9a4.5 4.5 0 0 0 0 9ZM10 0a6 6 0 0 1 3.04 11.174c3.688 1.11 6.458 4.218 6.955 8.078c.047.367-.226.7-.61.745c-.383.045-.733-.215-.78-.582c-.54-4.19-4.169-7.345-8.57-7.345c-4.425 0-8.101 3.161-8.64 7.345c-.047.367-.397.627-.78.582c-.384-.045-.657-.378-.61-.745c.496-3.844 3.281-6.948 6.975-8.068A6 6 0 0 1 10 0Z"/></svg>
        </a>
        <div v-if="isAuthenticated" class="dropdown-menu" aria-labelledby="navbarDropdown">
          <router-link class="dropdown-item" to="/settings" >My Store</router-link>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#" @click="logOut">Log out</a>
        </div>
        <div v-else class="dropdown-menu" aria-labelledby="navbarDropdown">
          <router-link class="dropdown-item" to="/login" >Log In</router-link>
        </div>
      </li>
      <li class="nav-item">
        <a class="nav-link" style="padding-bottom:0px;margin-right: 10px;" href="/myCart"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24"><path fill="currentColor" d="M17 18a2 2 0 0 1 2 2a2 2 0 0 1-2 2a2 2 0 0 1-2-2c0-1.11.89-2 2-2M1 2h3.27l.94 2H20a1 1 0 0 1 1 1c0 .17-.05.34-.12.5l-3.58 6.47c-.34.61-1 1.03-1.75 1.03H8.1l-.9 1.63l-.03.12a.25.25 0 0 0 .25.25H19v2H7a2 2 0 0 1-2-2c0-.35.09-.68.24-.96l1.36-2.45L3 4H1V2m6 16a2 2 0 0 1 2 2a2 2 0 0 1-2 2a2 2 0 0 1-2-2c0-1.11.89-2 2-2m9-7l2.78-5H6.14l2.36 5H16Z"/></svg></a>
      </li>
      <li  class="nav-item dropdown" >
          <a class="nav-link  hidden-arrow " style="padding-bottom:0px;margin-right: 10px;" href="#" id="notificationDropDown" role="button" data-toggle="dropdown" aria-expanded="false"><svg xmlns="http://www.w3.org/2000/svg" width="26" height="27" viewBox="0 0 16 16"><path fill="currentColor" d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zM8 1.918l-.797.161A4.002 4.002 0 0 0 4 6c0 .628-.134 2.197-.459 3.742c-.16.767-.376 1.566-.663 2.258h10.244c-.287-.692-.502-1.49-.663-2.258C12.134 8.197 12 6.628 12 6a4.002 4.002 0 0 0-3.203-3.92L8 1.917zM14.22 12c.223.447.481.801.78 1H1c.299-.199.557-.553.78-1C2.68 10.2 3 6.88 3 6c0-2.42 1.72-4.44 4.005-4.901a1 1 0 1 1 1.99 0A5.002 5.002 0 0 1 13 6c0 .88.32 4.2 1.22 6z"/></svg>
            <span class="badge rounded-pill badge-notification bg-danger">{{ notifications.length }}</span>
          </a>
          <ul class="dropdown-menu dropdown-menu-right" aria-labelledby="notificationDropDown" >
              <li v-for="(notification, index) in notifications" :key="index">
                <div >
                  <a @click="handleApprovalClick(notification)" class="dropdown-item">
                    {{ notification.message }}
                  </a>
                </div>
              </li>
          </ul>
      </li> 
    </ul>
   
  </div>
    </nav>
    
    <div v-if="selectedNotification" class="modal fade" id="approvalModal" tabindex="-1" role="dialog" aria-labelledby="approvalModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="approvalModalLabel">Approval Notification</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          {{ selectedNotification.message }}<br><br>
          <p class="d-inline font-weight-bold ml-2">Name : </p> {{ selectedNotification.name }} <br><br>
          <p class="d-inline font-weight-bold ml-2">User : </p> {{ selectedNotification.user }}
        </div>
        <div class="modal-footer">
          <div v-if="selectedNotification.approval">
            <button type="button" class="btn btn-success mr-2" @click="handleApproval(true,selectedNotification.action,selectedNotification.notification_id)">Accept</button>
            <button type="button" class="btn btn-danger" @click="handleApproval(false,electedNotification.action,selectedNotification.notification_id)">Reject</button>
          </div>
          <div v-else>
            <button type="button" class="btn btn-danger" @click="clearNotification(selectedNotification)">Clear</button>
          </div>
      </div>
      </div>
    </div>
  </div>


</template>

<script>
import request from '@/services/apiService'
import {GET_DATA_ROUTE,GET,POST,AUTH,PUT_DATA,UPDATE_DATA} from '@/services/constants.js'

export default { props: { isAuthenticated: Boolean, isNotLoginPage : Boolean,allowSearching:Boolean}, data(){return{ selectedOption: 'Product', searchQuery: '',notifications:[],auth:false, selectedNotification: null,}},
methods: {
  logOut() {
      localStorage.removeItem('jwtToken');
      this.redirectToHomePage()
    },
  redirectToHomePage() {
      const currentRoute = this.$route.path;
      if (currentRoute !== '/') {
        this.$router.push('/');
        setTimeout(() => {
          location.reload();
        }, 1000);
      } else {
        location.reload();
      }
    },
    selectOption(option) {
        this.selectedOption = option;
    },
    search() {
      console.log(this.selectOption+" "+this.searchQuery)
      this.$emit('search', { option: this.selectedOption, query: this.searchQuery });
    },
    async getNotifications()
    {
      {
        const {success, data, error} = await request(AUTH)
        this.auth = success
      }
      if(this.auth)
      {
        var body = {type:6,offset:10000,limit:10000}

        const {success, data, error} =  await request(GET_DATA_ROUTE,POST,body)
        this.notifications = data.notifications
      }
      
    },
    handleApprovalClick(notification) {
      this.selectedNotification = notification;
      $('#approvalModal').modal('show');
    },
    async clearNotification(notification) {
     
      var body = {type:3,notificationId:notification.notification_id}
    
      const {success, data, error} = await request(UPDATE_DATA,POST,body)

      const index = this.notifications.indexOf(notification);
      if (index !== -1) {
        this.notifications.splice(index, 1);
      }
      
      $('#approvalModal').modal('hide');

    },
    async handleApproval(isApproved,action,id) {

    
    var body = {type:action,isApproved:isApproved,notificationId:id}
    
    const {success, data, error} = await request(UPDATE_DATA,POST,body)
    
    if(data.success)
    {
      this.clearNotification(this.selectedNotification);
    }

    $('#approvalModal').modal('hide');
  }
  },
  mounted()
  {
    this.getNotifications()
  }

};
</script>


<style>
.navbar {
    background-color: rgba(255, 255, 255, 0.2); 
    backdrop-filter: blur(5px); 
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}
.long-search-input {
    width:600px;
}
.stick-top {
  position: fixed;
  top: 0;
  width: 100%;
}

</style>
