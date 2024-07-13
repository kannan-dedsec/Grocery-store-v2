<template>
 <navbar :isNotLoginPage="isNotLoginPage" :isAuthenticated="auth" style="z-index: 999;" ></navbar>

 <div class="container" style="margin-top:7rem!important">
    <div class="row justify-content-center">
    <div class="col-md-5">
    <div class="card">
      <div class="card-header bg-white">
        <ul class="nav nav-tabs card-header-tabs">
          <li class="nav-item" @click="switchTab('login')">
            <a class="nav-link" :class="{ active: currentTab === 'login' }">Login</a>
          </li>
          <li class="nav-item" @click="switchTab('signup')">
            <a class="nav-link" :class="{ active: currentTab === 'signup' }">Signup</a>
          </li>
        </ul>
      </div>
      <div class="card-body bg-light">
        <form @submit.prevent="submitForm">
          <div v-if="currentTab === 'login'">
            <h5 class="card-title text-dark">Login</h5>
            <div class="form-group">
              <label for="loginUsername">Username</label>
              <input type="text" class="form-control" id="loginUsername" v-model="loginData.uname" required>
            </div>
            <div class="form-group">
              <label for="loginPassword">Password</label>
              <input type="password" class="form-control" id="loginPassword" v-model="loginData.passwd" required>
            </div>
          </div>
          <div v-else-if="currentTab === 'signup'">
            <h5 class="card-title text-dark">Signup</h5>
            <div class="form-group">
              <label for="signupUsername">Username</label>
              <input type="text" class="form-control" id="signupUsername" v-model="signupData.username" required>
            </div>
            <div class="form-group">
              <label for="signupEmail">E-mail</label>
              <input type="text" class="form-control" id="signupEmail" v-model="signupData.email" required>
            </div>
            <div class="form-group">
              <label for="signupPassword">Password</label>
              <input type="password" class="form-control" id="signupPassword" v-model="signupData.password" required>
            </div>
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </div>
  </div>
</div>
<popUpNotification ref="notification" />
</template>

<script>
  import navbar from '@/components/navbar.vue'
  import popUpNotification from '@/components/popUpNotification.vue'
  import request from '@/services/apiService'
  import {AUTH, LOGIN,POST,REGISTER} from '@/services/constants.js'

  export default {
    data(){
      return {
        auth : true,
        isNotLoginPage : false,
        currentTab: 'login',
        loginData: {
            uname: '',
            passwd: '',
        },
        signupData: {
            username: '',
            email:'',
            password: '',
        }
      }
    },
    components: {
      navbar,
      popUpNotification
    },
    methods: {
    switchTab(tab) {
      this.currentTab = tab;
    },
    async submitForm() {
      const req = this.currentTab === 'login' ? this.loginData : this.signupData;
      console.log('data submitted:', req);
      if(this.currentTab === 'login')
      {
        const {success, data, error} = await request(LOGIN, POST, req)
        if(success)
        {
            if(data.authenticated)
            {
                const jwtToken = data.token;

                localStorage.setItem('jwtToken', jwtToken);
                
                this.$refs.notification.showSuccess('Logged in successfully');
                setTimeout(() => {this.$router.push('/'); }, 1000);
            }
            else
            {
                this.$refs.notification.showError('Error : '+ data.message);
            } 
            
        }
        else
        {
            
        }
      }
      else
      {
        const {success, data, error} = await request(REGISTER, POST, req)
        if(success)
        {
            if(data.success)
            {
                this.$refs.notification.showSuccess(' Successfully registered kindly log-in !!');
            }
            else
            {
                this.$refs.notification.showError('Error : '+ data.message);
            }
        }
        else
        {
            this.$refs.notification.showError('Error : Contact Support ');
        }

      }



    },
  }
  };
</script>

<style>

</style>
  