import time

from flask import Blueprint,jsonify,request,send_from_directory
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies,unset_jwt_cookies,get_jwt_identity
from flask import current_app as app
from utils import DBUtil,redisUtil,taskListener
import globalConstants
import os

grocery_store_bp = Blueprint(globalConstants.BLUEPRINT_NAME, __name__)

@grocery_store_bp.route('/register', methods=['POST'])
def register():
    success = True
    message = None
    req = request.get_json()
    username = req.get('username')
    email = req.get('email')
    if(DBUtil.getUser(username) == None):
        if(DBUtil.getUserByMail(email)== None):
            DBUtil.addUser(username=username, password=req.get('password'), email=email,role=globalConstants.USER)
        else:
            success = False
            message = "E-Mail Already Exists"
    else:
        success = False
        message = "Username Already Exists"
    if(success):
        return jsonify({'success':success}), globalConstants.SUCCESS
    else:
        return jsonify({'success': success,'message':message}), globalConstants.SUCCESS


@grocery_store_bp.route('/login', methods=['POST'])
def login():
    req = request.get_json()
    username = req.get('uname')
    password = req.get('passwd')
    if(DBUtil.authenticated(username,password)):
        access_token = create_access_token(identity=username)
        response = jsonify({'authenticated': True,'token':access_token})
        #set_access_cookies(response, access_token)
        return response, globalConstants.SUCCESS
    else:
        return jsonify({'authenticated':False,'message': 'Invalid credentials'}), globalConstants.SUCCESS


@grocery_store_bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'logout': True})
    unset_jwt_cookies(response)
    return response, globalConstants.SUCCESS


@grocery_store_bp.route('/getGuestData', methods=['GET','POST'])
def getguestData():
    req = request.get_json()
    type = req.get("type")
    offset = req.get("offset")
    limit = req.get("limit")
    value = req.get("params")

    if (value is None):
        value = ""
    response = None
    if (type == globalConstants.GET_HOMEPAGE_DATA):
        response = jsonify({'products': DBUtil.getProducts(globalConstants.SORT_SELLING, value, offset, limit),'categories': DBUtil.getCategories(globalConstants.SORT_SELLING, value, offset, limit)})
    elif (type == globalConstants.GET_SEARCH_DATA):
        searchType = req.get("search_type")
        if (searchType == globalConstants.PRODUCT):
            response = jsonify({'products': DBUtil.getProducts(globalConstants.SEARCH, value, offset, limit)})
        elif(searchType == globalConstants.BY_CAT):
            response = jsonify({'products': DBUtil.getProducts(globalConstants.BY_CAT, value, offset, limit)})
        elif (searchType == globalConstants.CATEGORY):
            response = jsonify({'category': DBUtil.getCategories(globalConstants.SEARCH, value, offset, limit)})
        elif(searchType == globalConstants.UNIT):
            response = jsonify({'unit': DBUtil.getUnits(value, offset, limit)})
    elif (type == globalConstants.GET_SORT_DATA):

        sortType = int(req.get("sortType"))

        if (sortType == globalConstants.SORT_HIGH_LOW):
            response = jsonify({'products': DBUtil.getProducts(globalConstants.SORT_HIGH_LOW, value, offset, limit)})
        elif (sortType == globalConstants.SORT_LOW_HIGH):
            response = jsonify({'products': DBUtil.getProducts(globalConstants.SORT_LOW_HIGH, value, offset, limit)})
        elif (sortType == globalConstants.SORT_PRODUCT_SELLING):
            response = jsonify({'products': DBUtil.getProducts(globalConstants.SORT_SELLING, value, offset, limit)})
        elif (sortType == globalConstants.SORT_CATEGORY_SELLING):
            response = jsonify({'categories': DBUtil.getCategories(globalConstants.SORT_SELLING, value, offset, limit)})
    elif (type == globalConstants.GET_RANGE):
        range = int(req.get("sortType"))
        if (globalConstants.LESS_THAN_PRICE == range):
            print("less than",DBUtil.getProducts(globalConstants.LESS_THAN_PRICE, value, offset, limit))
            response = jsonify({'products': DBUtil.getProducts(globalConstants.LESS_THAN_PRICE, value, offset, limit)})
        elif (globalConstants.GREATER_THAN_PRICE == range):
            print("greater than", DBUtil.getProducts(globalConstants.LESS_THAN_PRICE, value, offset, limit))
            response = jsonify({'products': DBUtil.getProducts(globalConstants.GREATER_THAN_PRICE, value, offset, limit)})
    return response, globalConstants.SUCCESS


@grocery_store_bp.route('/getData', methods=['GET','POST'])
@jwt_required()
def getData():
    req = request.get_json()
    type = req.get("type")
    offset = req.get("offset")
    limit = req.get("limit")
    value = req.get("params")
    user =  get_jwt_identity()
    if (value is None):
        value = ''
    response = None
    if(type == globalConstants.ORDERS):
        response = jsonify({'products': DBUtil.getOrders(user, offset, limit)})

    elif(type == globalConstants.NOTIFICATIONS):
        response = jsonify({'notifications': DBUtil.getNotifications(user, offset, limit)})

    elif(type == globalConstants.GET_CART):
        cartData =  redisUtil.getCart(user)
        cartItems = {key.decode('utf-8'): value.decode('utf-8') for key, value in cartData.items()}
        items = cartItems.keys()
        products =  DBUtil.getProducts(globalConstants.PRODUCTS_LIST,items , offset, limit)
        cartProducts = []
        for item in items:
            for product in products:
                if product.get("product_id") == item:
                    product["selected_count"] = cartItems.get(item)
                    cartProducts.append(product)
        print(cartProducts)
        response = jsonify({'cart_items': cartProducts})

    elif (type == globalConstants.GET_SEARCH_DATA):
        user_id = DBUtil.getUser(user).user_id
        store = (DBUtil.getStoreFromUser(user_id))
        if(store is not None):
            searchType = req.get("search_type")
            if (searchType == globalConstants.PRODUCT):
                if(user_id ==  DBUtil.getAdmin()):
                    response = jsonify({'products': DBUtil.getProducts(globalConstants.SEARCH, value, offset, limit)})
                else:
                    response = jsonify({'products': DBUtil.getStoreProducts(value, offset, limit,store.store_id)})
            elif (searchType == globalConstants.CATEGORY):
                if (user_id == DBUtil.getAdmin()):
                    response = jsonify({'category': DBUtil.getCategories(globalConstants.SEARCH, value, offset, limit)})
                else:
                    response = jsonify({'category': DBUtil.getStoreCategories(value, offset, limit,store.store_id)})
            elif(searchType == globalConstants.UNIT):
                if (user_id == DBUtil.getAdmin()):
                    response = jsonify({'unit': DBUtil.getUnits(value, offset, limit)})
                else:
                    response = jsonify({'unit': DBUtil.getStoreUnits(value, offset, limit,store.store_id)})
        else:
            if (searchType == globalConstants.PRODUCT):
                response = jsonify({'products': []})
            elif (searchType == globalConstants.CATEGORY):
                response = jsonify({'category': []})
            elif (searchType == globalConstants.UNIT):
                response = jsonify({'unit': []})

    elif(type == globalConstants.GET_STORE):
        user_id = DBUtil.getUser(user).user_id
        store = (DBUtil.getAllStoreFromUser(user_id))
        if(store is not None):
            response = jsonify({'avail':True,'store_id':store.store_id, 'store_name':store.store_name, 'manager':store.manager_id, 'isApproved':store.is_approved,'isAdmin':store.manager_id == DBUtil.getAdmin()})
        else:
            response = jsonify({'avail':False})
    elif(type == globalConstants.GET_DASHBOARD):
        user = get_jwt_identity()
        user_id = DBUtil.getUser(user).user_id
        store = (DBUtil.getAllStoreFromUser(user_id))
        response = jsonify({'dashboard':DBUtil.get_store_statistics(store.store_id,user,DBUtil.isAdminUser(user))})
    return response, globalConstants.SUCCESS


@grocery_store_bp.route('/putData', methods=['POST'])
@jwt_required()
def putData():
    response = None
    code = None
    req = request.get_json()
    user = get_jwt_identity()
    type = req.get("type")
    user_id = DBUtil.getUser(user).user_id
    if(type == globalConstants.ADD_TO_CART):
        item_id = req.get("item_id")
        count = req.get("count")
        bef = redisUtil.getCartItem(user,item_id)
        if bef is not None:
            count += int(bef.decode('utf-8'))
        if(DBUtil.getProductStock(item_id) >= count):
            redisUtil.addToCart(user,item_id,count)
            response = jsonify({'success':True})
            code = globalConstants.SUCCESS
        else:
            response = jsonify({'success': False, 'message':'stock limit exceeded'})
            code = globalConstants.SUCCESS
    elif(type == globalConstants.ADD_STORE):
        user_id = DBUtil.getUser(user).user_id
        store_id = DBUtil.addStore(req.get("store"),user_id)
        DBUtil.sendNotification(globalConstants.ADD_STORE,store_id,None,None,globalConstants.APPROVAL,DBUtil.getAdmin())
        response = jsonify({'success': True})
    elif(type == globalConstants.UNIT):
        user_id = DBUtil.getUser(user).user_id
        store = DBUtil.getStoreFromUser(user_id)
        unitName = req.get("unitName")
        if(store is not None):
            if (DBUtil.isManagerOrAdmin(user)):
                DBUtil.addUnit(unitName,store.store_id)
                response = jsonify({'success': True})
            else:
                response = jsonify({'success': False, 'message': 'Not authorized to perform this task'})
        else:
            response = jsonify({'success': False, 'message': 'You dont have any registed or approved store'})
    elif(type == globalConstants.ADD_ITEM):
        productName = req.get('productName')
        category_id = req.get('category')
        unit = req.get('unit')
        quantity = req.get('quantity')
        price = req.get('price')
        productId = req.get('product_id')
        data = {
            'item_name': productName,
            'category_id': category_id,
            'price': price,
            'quantity': quantity,
            'unit': unit
        }
        DBUtil.updateProduct(productId,data)
        response = jsonify({'success': True})
    elif(type == globalConstants.ADD_CATEGORY):
        categoryName = req.get('categoryName')
        category_id = req.get('category_id')
        DBUtil.updateCategory(category_id,categoryName)
        response = jsonify({'success': True})

    return response, globalConstants.SUCCESS


@grocery_store_bp.route('/addData', methods=['POST'])
@jwt_required()
def addData():
    user = get_jwt_identity()
    user_id = DBUtil.getUser(user).user_id
    store =  (DBUtil.getStoreFromUser(user_id))
    type = int(request.form.get('type'))
    response = None
    if(store is not None):
        if (type == globalConstants.ADD_ITEM):
            if (DBUtil.isManagerOrAdmin(user)):
                file = None
                try:
                    file = request.files['file']
                except Exception as e:
                    print(e)
                productName = request.form.get('productName')
                category = request.form.get('category')
                unit = request.form.get('unit')
                quantity = request.form.get('quantity')
                price = request.form.get('price')
                product_id = DBUtil.getGuid()
                fileName= None
                if(file is not None):
                    targetDirectory = os.path.join(app.root_path, 'uploads')
                    os.makedirs(targetDirectory, exist_ok=True)
                    originalName , fileExtension = os.path.splitext(file.filename)
                    fileName = f"{product_id}{fileExtension}"
                    file.save(os.path.join(targetDirectory, fileName))
                DBUtil.addItem(product_id,productName,category,unit,quantity,price,fileName,store.store_id)
                response = jsonify({'success': True})
            else:
                response = jsonify({'success': False, 'message': 'Not authorized to perform this task'})

        elif (type == globalConstants.CATEGORY):
            if (DBUtil.isManagerOrAdmin(user)):
                file = None
                try:
                    file = request.files['file']
                except Exception as e:
                    print(e)
                category_name = request.form.get('categoryName')
                category_id = DBUtil.getGuid()
                fileName = None
                if (file is not None):
                    targetDirectory = os.path.join(app.root_path, 'uploads')
                    os.makedirs(targetDirectory, exist_ok=True)
                    originalName, fileExtension = os.path.splitext(file.filename)
                    fileName = f"{category_id}{fileExtension}"
                    file.save(os.path.join(targetDirectory, fileName))
                DBUtil.addCategory(category_id, category_name, fileName,store.store_id,user_id)
                if(user_id != DBUtil.getAdmin()):
                    DBUtil.sendNotification(globalConstants.CATEGORY,category_id,category_name,globalConstants.ADD,globalConstants.APPROVAL,DBUtil.getAdmin())
                response = jsonify({'success': True})
            else:
                response = jsonify({'success': False, 'message': 'Not authorized to perform this task'})
    else:
        response = jsonify({'success': False, 'message': 'You dont have any registed or approved store'})

    return response,globalConstants.SUCCESS


@grocery_store_bp.route('/updateData', methods=['POST'])
@jwt_required()
def updateData():
    response = None
    code = None
    req = request.get_json()
    user = get_jwt_identity()
    type = req.get("type")
    if(type == globalConstants.APPROVE_STORE):
        if(DBUtil.isAdminUser(user)):
            notificationId = req.get("notificationId")
            isApproved = req.get("isApproved")
            id = DBUtil.getIdByNotification(notificationId)
            if(isApproved):
                DBUtil.approveStore(id)
            else:
                DBUtil.rejectStore(id)

            DBUtil.deleteNotification(id)
            response = jsonify({'success': True})
            code = globalConstants.SUCCESS
        else:
            response = jsonify({'success': False,'message':'Not authorized to perform this task'})
            code = globalConstants.SUCCESS
    elif(type == globalConstants.APPROVE_CATEGORY):
        if (DBUtil.isAdminUser(user)):
            notificationId = req.get("notificationId")
            isApproved = req.get("isApproved")
            id = DBUtil.getIdByNotification(notificationId)
            if(isApproved):
                DBUtil.approveCategory(id)
            else:
                DBUtil.rejectCategory(id)
            response = jsonify({'success': True})
            code = globalConstants.SUCCESS
        else:
            response = jsonify({'success': False, 'message': 'Not authorized to perform this task'})
            code = globalConstants.SUCCESS
    elif (type == globalConstants.REMOVE_NOTIFICATION):
        notificationId = req.get("notificationId")
        DBUtil.deleteNotification(notificationId)
        response = jsonify({'success': True})
        code = globalConstants.SUCCESS

    return response, code

@grocery_store_bp.route('/uploads/<filename>')
def serve_file(filename):
    target_directory = os.path.join(app.root_path, 'uploads')
    return send_from_directory(target_directory, filename)


@grocery_store_bp.route('/removeData', methods=['POST'])
@jwt_required()
def removeData():
    response = None
    req = request.get_json()
    user = get_jwt_identity()
    type = req.get("type")
    if(globalConstants.DELETE_FROM_CART == type):
        itemId = req.get("item_id")
        redisUtil.deleteFromCart(user,itemId)
        response = jsonify({'success': True})
    elif(globalConstants.DELETE_ITEM == type):
        itemId = req.get("item_id")
        DBUtil.deleteProduct(itemId)
        response = jsonify({'success': True})
    return response, globalConstants.SUCCESS

@grocery_store_bp.route('/exportCsv', methods=['POST','GET'])
@jwt_required()
def exportCsv():
    response = None
    code = None
    user = DBUtil.getUser(get_jwt_identity())
    store = DBUtil.getStoreFromUser(user.user_id)
    isAdmin = user.user_role == globalConstants.ADMIN
    if store is None:
        response = jsonify({'success': False,'message':'unauthenticated user'})
        code = globalConstants.NOT_AUTHORIZED
    else:
        tmpFolder = os.path.join(app.root_path, 'tmp')
        os.makedirs(tmpFolder, exist_ok=True)
        taskListener.exportCsv.delay(user.email, store.store_id, tmpFolder,isAdmin)
        response =jsonify({'success': True})
        code = globalConstants.SUCCESS
    return response, code

@grocery_store_bp.route('/authenticated', methods=['GET'])
@jwt_required()
def check():
    return jsonify({'success': True}), globalConstants.SUCCESS


@grocery_store_bp.route('/checkOut', methods=['POST'])
@jwt_required()
def checkOut():
    user = DBUtil.getUser(get_jwt_identity())
    cartData = redisUtil.getCart(get_jwt_identity())
    print(cartData)
    message = "successful"
    cartItems = {key.decode('utf-8'): value.decode('utf-8') for key, value in cartData.items()}
    items = cartItems.keys()
    cartId = DBUtil.getGuid()
    totalAmount = 0
    for item in items:
         count = int(cartItems[item])
         product = DBUtil.getSingleProduct(item)
         if(product.quantity >= count):
            DBUtil.addCart(cartId, item, count)
            DBUtil.reduceQuantity(item,(product.quantity - count))
            redisUtil.deleteFromCart(get_jwt_identity(),item)
            totalAmount += (product.price * count)
         else:
            message ="partially successful"

    DBUtil.addSoldData(cartId, user.user_id,  int(time.time() * 1000),totalAmount)

    return jsonify({'success': True,'message':message}), globalConstants.SUCCESS
