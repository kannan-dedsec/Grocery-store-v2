<template>
    <div  class="mt-2">
      <ul class="nav nav-tabs" role="tablist">
        <li class="nav-item" @click="activateTab('mainTab1')">
          <a class="nav-link" :class="{ active: isActiveTab('mainTab1') }" id="mainTab1-tab" data-toggle="tab" href="#mainTab1" role="tab" aria-controls="mainTab1" aria-selected="true">View / Edit </a>
        </li>
        <li class="nav-item" @click="activateTab('mainTab2')">
          <a class="nav-link" :class="{ active: isActiveTab('mainTab2') }" id="mainTab2-tab" data-toggle="tab" href="#mainTab2" role="tab" aria-controls="mainTab2" aria-selected="false">Add</a>
        </li>
      </ul>
      <div class="tab-content mt-2">
        <div class="tab-pane fade show" :class="{ active: isActiveTab('mainTab1') }" id="mainTab1" role="tabpanel" aria-labelledby="mainTab1-tab">
          <ul class="nav nav-pills" role="tablist">
            <li class="nav-item" @click="activateSubTab('subTab1.1')">
              <a class="nav-link" :class="{ active: isActiveSubTab('subTab1.1') }" id="subTab1.1-tab" data-toggle="pill" href="#subTab1.1" role="tab" aria-controls="subTab1.1" aria-selected="true">Dashboard</a>
            </li>
            <li class="nav-item" @click="activateSubTab('subTab1.2')">
              <a class="nav-link" :class="{ active: isActiveSubTab('subTab1.2') }" id="subTab1.2-tab" data-toggle="pill" href="#subTab1.2" role="tab" aria-controls="subTab1.2" aria-selected="false">Products</a>
            </li>
            <li class="nav-item" @click="activateSubTab('subTab1.3')">
              <a class="nav-link" :class="{ active: isActiveSubTab('subTab1.3') }" id="subTab1.3-tab" data-toggle="pill" href="#subTab1.3" role="tab" aria-controls="subTab1.3" aria-selected="false">Categories</a>
            </li>
          </ul>
  
         
          <div class="tab-content mt-2">
            <div class="tab-pane fade show" :class="{ active: isActiveSubTab('subTab1.1') }" id="subTab1.1" role="tabpanel" aria-labelledby="subTab1.1-tab">
              <div class="container-fluid">
                    <br>
                    <div class="border border-light">
                        <br>
                        <h4 style="margin-left:15px;display:inline">Hello {{username}} !!! </h4><p style="display:inline;color:green">({{userType}})</p><p style="display:inline"> (<a style="color:blue"  @click="exportData()" >Export Product Data</a>) </p><br><br>
                        <p style="margin-left:15px">(Store Name : {{store_name}} )</p>
                        <br>
                        <div class = "border border-light">
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-md-4 mb-4">
                                    <div class="bg-light p-3">
                                        <h2>Total Revenue : ${{totalRevenue}}</h2>
                                    </div>
                                    </div>
                                    <div class="col-md-4 mb-4">
                                    <div class="bg-info p-3">
                                        <h2>Total Selling : {{totalSelling}}</h2>
                                    </div>
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="col-md-4 mb-4">
                                    <div class="bg-success p-3">
                                        <h2>Total Products : {{totalProducts}}</h2>
                                    </div>
                                    </div>
                                    <div class="col-md-4 mb-4">
                                    <div class="bg-light p-3">
                                        <h2>Total Customers : {{totalCustomers}}</h2>
                                    </div>
                                    </div>   
                                </div>

                                <div class="row">
                                    <div class="col-md-4 mb-4">
                                    <div class="bg-light p-3">
                                        <h2>Total Categories : {{totalCategories}}</h2>
                                    </div>
                                    </div>
                                </div>
                            </div>
                        </div>    
                    </div>
              </div>
            </div>
  
    
            <div class="tab-pane fade show" :class="{ active: isActiveSubTab('subTab1.2') }" id="subTab1.2" role="tabpanel" aria-labelledby="subTab1.2-tab">
              <div class="container-fluid">
                <ProductList sliderId="topProducts" title="All Products" :isHomepage="isHomepage" :editMode="editMode" :products="productData"></ProductList>
              </div>
            </div>
  
           
            <div class="tab-pane fade show" :class="{ active: isActiveSubTab('subTab1.3') }" id="subTab1.3" role="tabpanel" aria-labelledby="subTab1.3-tab">
              <div class="container-fluid">
                <categoryList :isHomepage="isHomepage" :editMode=editMode title="All Categories" :categories="categoryData" />
              </div>
            </div>
  
            
            <div class="tab-pane fade show" :class="{ active: isActiveSubTab('subTab1.4') }" id="subTab1.4" role="tabpanel" aria-labelledby="subTab1.4-tab">
              <div class="container-fluid">
                Units
              </div>
            </div>
          </div>
        </div>
  
        <div class="tab-pane fade show" :class="{ active: isActiveTab('mainTab2') }" id="mainTab2" role="tabpanel" aria-labelledby="mainTab2-tab">
          <ul class="nav nav-pills" role="tablist">
           
            <li class="nav-item" @click="activateSubTab('subTab2.1')">
              <a class="nav-link" :class="{ active: isActiveSubTab('subTab2.1') }" id="subTab2.1-tab" data-toggle="pill" href="#subTab2.1" role="tab" aria-controls="subTab2.1" aria-selected="true">Product</a>
            </li>
  
          
            <li class="nav-item" @click="activateSubTab('subTab2.2')">
              <a class="nav-link" :class="{ active: isActiveSubTab('subTab2.2') }" id="subTab2.2-tab" data-toggle="pill" href="#subTab2.2" role="tab" aria-controls="subTab2.2" aria-selected="false">Category</a>
            </li>
  
         
            <li class="nav-item" @click="activateSubTab('subTab2.3')">
              <a class="nav-link" :class="{ active: isActiveSubTab('subTab2.3') }" id="subTab2.3-tab" data-toggle="pill" href="#subTab2.3" role="tab" aria-controls="subTab2.3" aria-selected="false">Unit</a>
            </li>
          </ul>
          
          <div class="tab-content mt-2">
            <div class="tab-pane fade show" :class="{ active: isActiveSubTab('subTab2.1') }" id="subTab2.1" role="tabpanel" aria-labelledby="subTab2.1-tab">
              <div class="container">

            <h5 class=" navbar-brand mt-3">Add Product</h5>
            <form @submit.prevent="saveProduct">
              <div class="form-group">
                <label for="productName">Product Name:</label>
                <input v-model="productName" id="productName" class="form-control" required />
              </div>

              <div class="form-group">
                <label for="category">Category:</label>
                <select v-model="category" id="category" class="form-control" required>
                  <option v-for="cat in categories" :key="cat.category_id" :value="cat.category_id">{{ cat.category_name }}</option>
                </select>
              </div>

              <div class="form-group">
                <label for="unit">Unit:</label>
                <select v-model="unit" id="unit" class="form-control" required>
                  <option v-for="u in units" :key="u.unit_id" :value="u.unit_id">{{ u.unit_name }}</option>
                </select>
              </div>

              <div class="form-group">
                <label for="quantity">Quantity:</label>
                <input v-model.number="quantity" id="quantity" type="number" class="form-control" required />
              </div>

              <div class="form-group">
                <label for="price">Price:</label>
                <input v-model.number="price" id="price" type="number" class="form-control" required />
              </div>

              <div class="form-group">
                <label for="image">Image:</label>
                <input @change="handleImageChange" id="image" type="file" class="form-control-file" accept="image/*" />
              </div>

              <div class="modal-footer">
                <button type="submit" class="btn btn-primary">Save</button>
              </div>
            </form>
              </div>
            </div>
  
            <div class="tab-pane fade show" :class="{ active: isActiveSubTab('subTab2.2') }" id="subTab2.2" role="tabpanel" aria-labelledby="subTab2.2-tab">
              <div class="container">
    
            <h5 class=" navbar-brand mt-3">Add Category</h5>
            <form @submit.prevent="saveCategory">
              <div class="form-group">
                <label for="productName">Category Name:</label>
                <input v-model="categoryName" id="productName" class="form-control" required />
              </div>
              <div class="form-group">
                <label for="image">Image:</label>
                <input @change="handleCatImageChange" id="image" type="file" class="form-control-file" accept="image/*" />
              </div>
              <div class="modal-footer">
                <button type="submit" class="btn btn-primary">Save</button>
              </div>
            </form>
              </div>
            </div>          
            <div class="tab-pane fade show" :class="{ active: isActiveSubTab('subTab2.3') }" id="subTab2.3" role="tabpanel" aria-labelledby="subTab2.3-tab">
              <div class="container">
            
                <h5 class=" navbar-brand mt-3">Add Unit</h5>
            <form @submit.prevent="saveUnit">
              <div class="form-group">
                <label for="unitName">Unit Name:</label>
                <input v-model="unitName" id="productName" class="form-control" required />
              </div>
              <div class="modal-footer">
                <button type="submit" class="btn btn-primary">Save</button>
              </div>
            </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <popUpNotification ref="notification"></popUpNotification>
  </template>


  <script>

  import request from '@/services/apiService'
  import {ADD_DATA,GET,POST,AUTH,PUT_DATA,GET_GUEST_DATA,GET_DATA_ROUTE,EXPORT_CSV} from '@/services/constants.js'
  import categoryList from '@/components/categoryList.vue'
  import ProductList from '@/components/ProductList.vue'
  import popUpNotification from '@/components/popUpNotification.vue'
  export default {
    props:{
        isAdmin : Boolean
    },
    components: 
    {
        categoryList,
        ProductList,
        popUpNotification
    },
    data() {
      return {
        isStoreUser:true,
        editMode:true,
        isHomepage: false,
        productData:[],
        categoryData:[],
        categories:[],
        units:[],
        activeTab: 'mainTab1',
        activeSubTab: 'subTab1.1',
        productName: '',
        category: '',
        unit: '',
        quantity: null,
        price: null,
        selectedImage: null,
        categoryName:'',
        catImg:null,
        unitName:'',
        username:'',
        store_name:'',
        totalSelling:null,
        totalCategories:null,
        totalCustomers:null,
        totalProducts:null,
        totalRevenue:null,
        userType:''

      }
    },
    async mounted(){
        this.setCat();
        this.setUnit();
        this.setProduct();
        this.setDashboard();
    },
    methods: 
    {
        activateTab(tab) 
        {
            this.activeTab = tab;
        },
        isActiveTab(tab) 
        {
            return this.activeTab === tab;
        },
        activateSubTab(subTab) 
        {
            this.activeSubTab = subTab;
        },
        exportData()
        {
          let {success, data, error} = request(EXPORT_CSV,GET,null)

          console.log("export data clicked")
        },
        isActiveSubTab(subTab) 
        {
            return this.activeSubTab === subTab;
        },
        async saveProduct() 
        {
        if (!this.productName || !this.category || !this.unit || !this.quantity || !this.price) {
            alert('Please fill in all mandatory fields.');
            return;
        }
        const formData = new FormData();
        formData.append('file', this.selectedImage);
        formData.append('productName', this.productName);
        formData.append('category',this.category);
        formData.append('unit',this.unit);
        formData.append('quantity',this.quantity);
        formData.append('price',this.price);
        formData.append('type',1)
        
        const {success, data, error} = await this.requestFile(ADD_DATA,POST,formData)

        if(success)
        {
            if(data.success)
            {
                this.$refs.notification.showSuccess('product added successfully');
                
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


        },
        async saveCategory()
        {
            if (!this.categoryName) 
            {
                alert('Please fill in all mandatory fields.');
                return;
            }
            const formData = new FormData();
            formData.append('file', this.catImg);
            formData.append('categoryName',  this.categoryName);
            formData.append('type',2)
            const {success, data, error} = await this.requestFile(ADD_DATA,POST,formData)
            if(success)
            {
                if(data.success)
                {
                    this.$refs.notification.showSuccess('Category Request Submitted');
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
        },
        async saveUnit()
        {
            const unitData  = {
                unitName : this.unitName,
                type : 5
            }
            
            if (!this.unitName) 
            {
                alert('Please fill in all mandatory fields.');
                return;
            }

            const {success, data, error} = await request(PUT_DATA,POST,unitData)
            
            if(success)
            {
                if(data.success)
                {
                    this.$refs.notification.showSuccess('unit added successfully');
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
        ,
        handleImageChange(event) 
        {
        
            const file = event.target.files[0];
            if (file) 
            {
                this.selectedImage = file;
            }
        },
        handleCatImageChange(event) 
        {
            const file = event.target.files[0];
            if (file) {
            this.catImg = file;
        }
        },
        async requestFile(url, method = 'GET', data = null) 
        {
            try 
            {  
                const flaskUrl = "http://localhost:5000"
                const jwtToken = localStorage.getItem('jwtToken');
                const headers = {};
            if (jwtToken) 
            {
                headers['Authorization'] = `Bearer ${jwtToken}`;
            }
            const response = await fetch(flaskUrl + url, 
                {
                    method,
                    headers:headers,
                    body: data
                });
                if (!response.ok) 
                {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                const responseData = await response.json();
                return { success: true, data: responseData };
            } 
            catch (error) 
            {
                return { success: false, error: 'Failed to fetch data. '+ error };
            }
         },
         async setCat()
         {
            {
                let dat = { type: 2, search_type:2, offset:0,limit:10000}
                let {success, data, error} = await request(GET_GUEST_DATA,POST,dat)
                this.categories = data.category
      
            }
            {
                let dat = { type: 2, search_type:2, offset:0,limit:10000}
                let {success, data, error} = await request(GET_DATA_ROUTE,POST,dat)
            
                if(data)
                {
                    this.categoryData = data.category
                }
            }
            
         },
         async setUnit()
         {
            let dat = { type: 2, search_type:5, offset:0,limit:10000}
            let {success, data, error} = await request(GET_GUEST_DATA,POST,dat)
            this.units = data.unit
         },
         async setProduct()
         {
            let dat = { type: 2, search_type:1, offset:0,limit:10000}
            let {success, data, error} = await request(GET_DATA_ROUTE,POST,dat)
           
            if(data)
            {
                this.productData = data.products
            }
            console.log(data.products)
         },
         async setDashboard()
         {
            let dat = { type: 8, offset:0,limit:10000}
            let {success, data, error} = await request(GET_DATA_ROUTE,POST,dat)
            console.log(data)
            data = data.dashboard
            this.username = data.username
            this.store_name = data.store_name
            this.totalSelling = data.total_selling
            this.totalCategories = data.total_categories
            this.totalCustomers = data.total_customers
            this.totalProducts = data.total_products
            this.totalRevenue = data.total_revenue
            this.userType = data.userType
         }
    }
  };
  </script>
  
  <style>

  </style>
  