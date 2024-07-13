<template>
    <div v-if="isVisible" class="small-popup-notification" :class="{ show: isVisible, success: isSuccess, danger: isError }">
      {{ message }}
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isVisible: false,
        isSuccess: false,
        isError: false,
        message: '',
      };
    },
    methods: {
      showSuccess(message) {
        this.isVisible = true;
        this.isSuccess = true;
        this.isError = false;
        this.message = message;
  
        setTimeout(() => {
          this.isVisible = false;
        }, 1500);
      },
      showError(message) {
        this.isVisible = true;
        this.isSuccess = false;
        this.isError = true;
        this.message = message;
  
        setTimeout(() => {
          this.isVisible = false;
        }, 2000);
      },
    },
  };
  </script>
  
  <style scoped>
  .small-popup-notification {
  position: fixed;
  top: 20px;
  right: -300px; 
  padding: 10px;
  border-radius: 5px;
  color: #fff;
  font-weight: bold;
  transition: right 2s ease-in-out;
  z-index: 1000;
}

.small-popup-notification.success {
  background-color: #28a745;
}

.small-popup-notification.danger {
  background-color: #dc3545; 
}

.small-popup-notification.show {
  right: 20px;
}
  </style>
  