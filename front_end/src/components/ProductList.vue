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
   
    <div class="border border-light">
      <br>
      <h3 class="navbar-brand ml-2 mt-2 mr-1 mb-4 d-inline">{{ title }}</h3>  <button v-if="!cartMode && !editMode" @click="openFilterModal" class="btn btn-link d-inline">( Filter )</button>
      <p v-if="cartMode && !viewMode && hasData" class="d-inline text-primary">
        <a @click="checkOut()">Check out</a>
      </p>

      <br><br>
      <div v-if="hasData" class="inner">
        <div class="row">
          <div v-for="product in products" :key="product.product_id" class="mb-4">
            <product :viewMode="viewMode" :editMode="editMode" :cartMode="cartMode" @editModal="editModal" :product="product"></product>
          </div>
        </div>
      </div>
      <div v-else class="text-center mt-3">
        <p>No data available</p>
      </div>
    </div>
    <popUpNotification ref="notification"></popUpNotification>

    <div class="modal fade" id="filterModal" tabindex="-1" role="dialog">

      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Filter Options</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
        
            <ul class="nav nav-tabs" id="filterTabs" role="tablist">
              <li class="nav-item">
                <a class="nav-link active" id="sortByPriceTab" data-toggle="tab" href="#sortByPrice" role="tab">Sort by Price</a>
              </li>
              <!-- <li class="nav-item">
                <a class="nav-link" id="sortBySellingTab" data-toggle="tab" href="#sortBySelling" role="tab">Sort by Selling</a>
              </li> -->
              <li class="nav-item">
                <a class="nav-link" id="rangeTab" data-toggle="tab" href="#range" role="tab">Range</a>
              </li>
            </ul>

          
            <div class="tab-content">
              
              <div class="tab-pane fade show active" id="sortByPrice" role="tabpanel">
                <br>
                <label for="priceSort">Price Sort:</label>
                <br>
                <select id="priceSort" class="form-control">
                  <option value="5">Low to High</option>
                  <option value="6">High to Low</option>
                </select>
              </div>

            
              <!-- <div class="tab-pane fade" id="sortBySelling" role="tabpanel">
                <br>
                <label for="sellingSort">Selling Sort:</label>
                <br>
                <select id="sellingSort" class="form-control">
                  <option value="8">Product Selling</option>
                  <option value="9">Category Selling</option>
                </select>
              </div> -->

            
              <div class="tab-pane fade" id="range" role="tabpanel">
                <br>
                <label for="rangeOption">Range Option:</label>
                <br>
                <select id="rangeOption" class="form-control">
                  <option value="4">Higher Than</option>
                  <option value="3">Lower Than</option>
                </select>
                <label for="rangeValue">Input:</label>
                <input type="number" id="rangeValue" class="form-control" />
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="filter">Filter</button>
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
      </div>
      
<!--- modal starts-->

      <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Edit Product</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="saveProduct">
          <div class="form-group">
            <label for="productName">Product Name:</label>
            <input v-model="selectedProduct.product_name" id="productName" class="form-control" required />
          </div>

          <div class="form-group">
            <label for="category">Category:</label>
            <select v-model="selectedProduct.category_id" id="category" class="form-control" required>
              <option  v-for="cat in categories" :key="cat.category_id" :value="cat.category_id">{{ cat.category_name }}</option>
            </select>
          </div>

          <div class="form-group">
            <label for="unit">Unit:</label>
            <select v-model="selectedProduct.unit_id" id="unit" class="form-control" required>
              <option v-for="u in units" :key="u.unit_id" :value="u.unit_id">{{ u.unit_name }}</option>
            </select>
          </div>

          <div class="form-group">
            <label  for="quantity">Quantity:</label>
            <input v-model="selectedProduct.quantity_left" id="quantity" type="number" class="form-control" required />
          </div>

          <div class="form-group">
            <label for="price">Price:</label>
            <input v-model="selectedProduct.price_per_quantity"  id="price" type="number" class="form-control" required />
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
<!--- modal ends-->


  </div>
</template>


<script>
    import product from './product.vue'
    import request from '@/services/apiService'
    import {CHECK_OUT,POST,GET_DATA_ROUTE,GET,GET_GUEST_DATA,AUTH,PUT_DATA,UPDATE_DATA} from '@/services/constants.js'
    import popUpNotification from '@/components/popUpNotification.vue'
   
    export default {
        data() { return {
          loading:true,
          selectedProduct:{},
          units:[],
          categories:[]
        };},
        components:{
            product,
            popUpNotification
        },
        props:{
            title: String,
            products:Array,
            isHomepage:Boolean,
            editMode:Boolean,
            cartMode:Boolean,
            viewMode:Boolean
        },
        mounted(){
          this.setCat();
          this.setUnit();
          setTimeout(() => {this.loading = false;}, 500); 
        },
        computed:{
            hasData()
            {
                return this.products.length > 0
            }
        },
        methods:
        {
            async checkOut()
            {
              const {success, data, error} = await request(CHECK_OUT,POST)
              if(success)
              {
                this.$refs.notification.showSuccess('Order Placed : '+data.message);
                setTimeout(() => {location.reload(); }, 1000);
                
              }
              else
              {
                this.$refs.notification.showError('Error : Couldn\'t place the order');
              }

            },
            openFilterModal() 
            {
                $('#filterModal').modal('show');
            },
            async filter() 
            {
              var type = 3;
              var val = '';
              var sortType = null

              const activeTabId = $('#filterTabs .nav-link.active').attr('id');

              if (activeTabId === 'sortByPriceTab') 
              {
                sortType = $('#priceSort').val();
              }
              else if (activeTabId === 'sortBySellingTab') 
              {
                sortType = $('#sellingSort').val();
              }
              else if (activeTabId === 'rangeTab') 
              {
                type = 4
                sortType = $('#rangeOption').val();
                val = $('#rangeValue').val();
              }
              
              var body = {type:type,offset:0,sortType:sortType,params:val,limit:10000}

              const {success, data, error} = await request(GET_GUEST_DATA,POST,body)
                
              console.log(data.products)
              this.$emit('filter', { filter : data.products });

              $('#filterModal').modal('hide');
              
            },
            editModal(editModal) 
            {
            
              this.selectedProduct = this.findProduct(editModal);

              console.log("in editmodal "+this.selectedProduct)

              
            },
            findProduct(product_id)
            {
              product = {};
              for (let i = 0; i < this.products.length; i++) 
              {
                    if(this.products[i].product_id === product_id)
                    {
                      return { ...this.products[i] };
                    }
              }
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
            async saveProduct(product)
            {

                var dat = { 
                  productName: this.selectedProduct.product_name,
                  category: this.selectedProduct.category_id,
                  unit: this.selectedProduct.unit_id,
                  quantity: this.selectedProduct.quantity_left,
                  price: this.selectedProduct.price_per_quantity,
                  type:1,
                  product_id:this.selectedProduct.product_id
                }
                
                let {success, data, error} = await request(PUT_DATA,POST,dat)

                if(success)
                {
                  this.$refs.notification.showSuccess('Updated the Product succesfully');
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

<style>
.slider{
  display: flex;
  justify-content: center;
}
.inner {
  padding: 1em;
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