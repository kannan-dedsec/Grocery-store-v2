<template>
    <div class="card" style="z-index: 1;">
      <div class= "image-squish">
        <div  v-if="product.image_url">
            <img class="card-img-top"  :src="product.image_url"  alt="Card image cap">
        </div>
        <div v-else>
          <img class="card-img-top"  :src="require(`@/assets/product.png`)"  alt="Card image cap">
        </div>
      </div>
        <div class="card-body">
        <h5 v-if="this.product.quantity_left > 0" class="card-title">{{product.product_name}} ( Stock : {{ product.quantity_left}} left )</h5>
        <h5 v-else class="card-title">{{product.product_name}}(Out of Stock)</h5>
        <p class="card-text">{{product.category_name}} ( Price :{{product.price_per_quantity}}$ )</p>
        <div v-if="editMode">
          <a @click="editProduct(product)" style="display:inline" data-toggle="modal" data-target="#myModal" class="btn btn-outline-primary">Edit</a>
          <a @click="DeleteProduct" style="display:inline; margin-left:150px" class="btn btn-outline-danger">Delete</a>
        </div>
        <div v-else-if="cartMode">
          <a @click="removeFromCart" style="display:inline" class="btn btn-outline-primary">Remove From cart</a><input id="quantity" min=1 max=20000 type="number" v-model="quantity" style="margin-left:20px;padding-top:2px;display:inline;width:22%;height:36.2px" disabled/>
        </div>
        <div v-else>
          <a @click="addToCart" style="display:inline" class="btn btn-outline-primary">Add to Cart</a><input id="quantity" type="number" min=1 max=20000 v-model="quantity"  style="margin-left:20px;padding-top:2px;display:inline;width:22%;height:36.2px"/>
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
                    return {
                      auth : true,
                      quantity: this.product.selected_count ? this.product.selected_count :  0,
                      categories:[],
                      units:[],
                    }
            },
            props:{
                product : Object,
                editMode: Boolean,
                cartMode: Boolean,
                viewMode:Boolean
            },
            mounted(){
              this.isAuthenticated();
              this.setCat();
              this.setUnit();
            },
            methods: 
            {
                async addToCart() 
                {
                  if(this.auth)
                  {
                    if (!isNaN(this.quantity))
                    {
                      if (this.quantity > 0) 
                      {
                        const dat = {type:3, item_id:this.product.product_id, count:this.quantity}
                        const {success, data, error} = await request(PUT_DATA,POST,dat)
                        if(success)
                        {
                            if(data.success)
                            {
                              this.$refs.notification.showSuccess('added to cart successfully !!');
                              this.quantity = 0
                            }       
                            else
                            {
                              this.$refs.notification.showError('Selected number of stocks are currently not available.');
                            }
                        }    
                      }
                      else
                      {
                        this.$refs.notification.showError('Kindly add a valid input');
                      }   
                    }
                    else
                    {
                      this.$refs.notification.showError('Kindly add a valid input');
                    }
                  }
                  else
                  {
                    this.$refs.notification.showError('Error : Can\'t add to cart Kindly login');
                  }  
                },
                async removeFromCart()
                {
                  if(this.auth)
                  {
                    const dat = {type:5, item_id:this.product.product_id}

                    const {success, data, error} = await request(REMOVE_DATA,POST,dat)
                    
                    this.$refs.notification.showSuccess('removed from cart successfully');
                    
                    location.reload()
                  }
                  else
                  {
                    this.$refs.notification.showError('Error : Can\'t remove from cart Kindly login');
                  }

                },
                async isAuthenticated()
                {
                  const {success, data, error} = await request(AUTH)
                  this.auth =  success
                },
                async DeleteProduct()
                {
                  var result = window.confirm("Are you sure you want to delete this item?");
                  if (result) 
                  {
                    var dat = {item_id: this.product.product_id,type:13}
                    let {success, data, error} = await request(REMOVE_DATA,POST,dat)
                    if(success)
                    {
                      this.$refs.notification.showSuccess('Product deleted successfully ');
                      location.reload()
                    }
                    else
                    {
                      this.$refs.notification.showError('Error : Contact support');
                    }
                  } 
                  else 
                  {
                    alert("Deletion canceled.");
                  }
                  
                },
                editProduct(product)
                {
                  this.$emit('editModal',product.product_id);           
                },
                async setCat()
                {
                    {
                        let dat = { type: 2, search_type:2, offset:0,limit:10000}
                        let {success, data, error} = await request(GET_GUEST_DATA,POST,dat)
                        this.categories = data.category
              
                    }
                
                },
                async setUnit()
                {
                    let dat = { type: 2, search_type:5, offset:0,limit:10000}
                    let {success, data, error} = await request(GET_GUEST_DATA,POST,dat)
                    this.units = data.unit
                },
            },
            components:{
              popUpNotification
            }
    };
</script>
<style>
.card img {
  max-width: 100%;
  max-height: 100%;
}
.card {
  margin: 0 0.5em;
  box-shadow: 2px 6px 8px 0 rgba(22, 22, 26, 0.18);
  border: none;
  border-radius: 0;
}

.image-squish { 
    width: 20rem;
    height : 15rem;
    overflow: hidden; 
} 

.image-squish img{
      width: 100%; 
      height: 100%; 
      object-fit: cover;
}


</style>