import hashlib as encryptor

import globalConstants
from objects.Objects import ORM_BASE as db
from objects.Objects import User,UserPassword,Store,Item,Category,Unit,Cart,SoldData,NotificationVsUser,Notification
import uuid
from sqlalchemy import func,update
from sqlalchemy.orm import aliased
import globalConstants as gc
from datetime import datetime
from flask import jsonify
import sqlite3
import os
import csv
import time
import json

def encrypt(text):
    return encryptor.sha256(text.encode('UTF-8')).hexdigest()

def authenticated(username,password):
    user = getUser(username)
    if(user != None):
        if(matchPasswd(user.user_id,encrypt(password))):
            return True
    else:
        return False

def getUser(username):
    return db.session.query(User).filter_by(username=username).first()

def getUserByMail(email):
    return db.session.query(User).filter_by(email=email).first()

def getStore(store):
    return db.session.query(Store).filter_by(store_name=store).first()

def getStoreById(storeId):
    return db.session.query(Store).filter_by(store_id=storeId).first()

def getStoreFromUser(user):
    return db.session.query(Store).filter(Store.manager_id==user).filter(Store.is_approved == True).first()

def getAllStoreFromUser(user):
    return db.session.query(Store).filter(Store.manager_id==user).first()

def sendNotification(type,id,data,operation,notificationType,user_id):
    notiId = getGuid()
    if(type == gc.CATEGORY):
        db.session.add(Notification(notification_id=notiId, notification_data=json.dumps({'category_id': id, 'category_name': data, 'type':type}), type= notificationType, is_manadatory=True))
        db.session.add(NotificationVsUser(notification_id=notiId, user_id=user_id))
        db.session.commit()
    elif(type == gc.ADD_STORE):
        db.session.add(Notification(notification_id=notiId, notification_data=json.dumps({'store_id': id, 'type': type}), type=notificationType, is_manadatory=True))
        db.session.add(NotificationVsUser(notification_id=notiId, user_id=user_id))
        db.session.commit()


def addStore(name,manager):
    storeid = getGuid()
    db.session.add(Store(store_id=storeid, store_name=name, manager_id=manager,is_approved=( manager == getAdmin()) ))
    db.session.commit()
    return storeid

def matchPasswd(userId,password):
    return db.session.query(UserPassword).filter_by(user_id=userId).first().password == password

def addUser(username,password,email,role):
    userid = getGuid()
    db.session.add(User(user_id=userid, username=username, email=email, user_role=role))
    db.session.add(UserPassword(user_id= userid,password=encrypt(password)))
    db.session.commit()
    return userid

def getGuid():
    return str(uuid.uuid4())


def convertRawToJsonArray(type,raw):
    arr = []
    if(type == gc.PRODUCT):
        for item, category, unit, store in raw:
            data = {}
            data["product_id"] = item.item_id
            data["product_name"] = item.item_name
            data["unit_id"] = item.unit
            data["store_id"] = item.store_id
            if(item.image_url is None):
                data["image_url"] = item.image_url
            else:
                data["image_url"] = "http://localhost:5000/uploads/"+item.image_url

            data["quantity_left"] = item.quantity
            data["price_per_quantity"] = item.price
            data["category_id"] = item.category_id
            data["category_name"] = category.category_name
            data["unit_name"] = unit.unit_name
            data["store_name"] = store.store_name
            arr.append(data)
    if(type == gc.CATEGORY):
        for category_id, category_name, image_url in raw:
            if image_url is not None:
                image_url = "http://localhost:5000/uploads/"+image_url
            category_dict = {
                'category_id': str(category_id),
                'category_name': category_name,
                'image': image_url
            }
            arr.append(category_dict)
    if(type == gc.ORDER):
        order_items_dict = {}
        for cart_id, item_id, item_name, price, count, time_in_millis,total_sold_price in raw:
            if cart_id not in order_items_dict:
                order_items_dict[cart_id] = {
                    'order_id': str(cart_id),
                    'items': [],
                    'purchased_on': datetime.utcfromtimestamp(time_in_millis / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                    'total_price': 0
                }
            order_items_dict[cart_id]['items'].append({
                'item_name': item_name,
                'price': price,
                'count': count
            })
            order_items_dict[cart_id]['total_price'] = total_sold_price
        arr = list(order_items_dict.values())
    if(type == gc.NOTIFICATION):
        arr = [{'notification_id': notification.notification_id,'notification_data': notification.notification_data,'type':notification.type,'is_manadatory': notification.is_manadatory} for notification in raw]
    if(type == gc.UNIT):
        arr = [{'unit_id': unit.unit_id,'unit_name': unit.unit_name} for unit in raw]

    return arr


def getProducts(type,param,offset,limit):
    if(type == gc.SEARCH):
        raw = db.session.query(Item, Category, Unit, Store).join(Category, Item.category_id == Category.category_id).join(Unit, Item.unit == Unit.unit_id).join(Store, Item.store_id == Store.store_id).filter(Item.item_name.like(f'%{param}%')).offset(offset).limit(limit).all()
    elif(type == gc.BY_CAT):
        raw = db.session.query(Item, Category, Unit, Store).join(Category,Item.category_id == Category.category_id).join(Unit,Item.unit == Unit.unit_id).join(Store, Item.store_id == Store.store_id).filter(Category.category_name.like(f'%{param}%')).offset(offset).limit(limit).all()
    elif(type == gc.SORT_SELLING):
        raw = db.session.query(Item, Category, Unit, Store).join(Category, Item.category_id == Category.category_id).join(Unit, Item.unit == Unit.unit_id).join(Store, Item.store_id == Store.store_id).join(Cart,Item.item_id == Cart.item_id).filter(Item.item_name.like(f'%{param}%')).group_by(Cart.item_id).order_by(func.sum(Cart.count).desc()).offset(offset).limit(limit).all()
        if raw is None or len(raw) <= 0:
            raw = db.session.query(Item, Category, Unit, Store).join(Category,Item.category_id == Category.category_id).join(Unit, Item.unit == Unit.unit_id).join(Store, Item.store_id == Store.store_id).filter(Item.item_name.like(f'%{param}%')).offset(offset).limit(limit).all()
    elif(type == gc.LESS_THAN_PRICE):
        raw = db.session.query(Item, Category, Unit, Store).join(Category,Item.category_id == Category.category_id).join(Unit,Item.unit == Unit.unit_id).join(Store, Item.store_id == Store.store_id).filter(Item.item_name.like(f'%%')).filter(Item.price <= param).offset(offset).limit(limit).all()
    elif(type == gc.GREATER_THAN_PRICE):
        raw = db.session.query(Item, Category, Unit, Store).join(Category,Item.category_id == Category.category_id).join(Unit,Item.unit == Unit.unit_id).join(Store, Item.store_id == Store.store_id).filter(Item.item_name.like(f'%%')).filter(Item.price >= param).offset(offset).limit(limit).all()
    elif(type == gc.SORT_HIGH_LOW):
        raw = db.session.query(Item, Category, Unit, Store).join(Category,Item.category_id == Category.category_id).join(Unit,Item.unit == Unit.unit_id).join(Store, Item.store_id == Store.store_id).filter(Item.item_name.like(f'%{param}%')).order_by(Item.price.desc()).offset(offset).limit(limit).all()
    elif(type == gc.SORT_LOW_HIGH):
        raw = db.session.query(Item, Category, Unit, Store).join(Category,Item.category_id == Category.category_id).join(Unit,Item.unit == Unit.unit_id).join(Store, Item.store_id == Store.store_id).filter(Item.item_name.like(f'%{param}%')).order_by(Item.price.asc()).offset(offset).limit(limit).all()
    elif(type == gc.PRODUCTS_LIST):
        raw = db.session.query(Item, Category, Unit, Store).join(Category, Item.category_id == Category.category_id).join(Unit, Item.unit == Unit.unit_id).join(Store, Item.store_id == Store.store_id).filter(Item.item_id.in_(param)).offset(offset).limit(limit).all()
    return convertRawToJsonArray(gc.PRODUCT,raw)


def getStoreProducts(param, offset, limit,store):
    raw = db.session.query(Item, Category, Unit, Store).join(Category,Item.category_id == Category.category_id).join(Unit,Item.unit == Unit.unit_id).join(Store, Item.store_id == Store.store_id).filter(Item.item_name.like(f'%{param}%')).filter(Item.store_id == store).offset(offset).limit(limit).all()
    return convertRawToJsonArray(gc.PRODUCT, raw)


def getCategories(type,param,offset,limit):
    if (type == gc.SEARCH):
        raw = db.session.query(Category.category_id, Category.category_name, Category.image_url).filter(Category.category_name.like(f'%{param}%')).filter(Category.is_approved == True).offset(offset).limit(limit).all()
    elif (type == gc.SORT_SELLING):
        raw =   db.session.query(Category.category_id, Category.category_name, Category.image_url).join(Item, Category.category_id == Item.category_id).join(Cart, Item.item_id == Cart.item_id).filter(Category.category_name.like(f'%{param}%')).filter(Category.is_approved==True).group_by(Category.category_id).order_by(func.sum(Cart.count).desc()).all()
        if raw is None  or len(raw) <= 0:
            raw = db.session.query(Category.category_id, Category.category_name, Category.image_url).filter(Category.is_approved==True).offset(offset).limit(limit).all()
    return convertRawToJsonArray(gc.CATEGORY, raw)

def getStoreCategories(param,offset,limit,store):
    raw = db.session.query(Category.category_id, Category.category_name, Category.image_url).filter(Category.category_name.like(f'%{param}%')).filter(Category.store_id==store).filter(Category.is_approved == True).offset(offset).limit(limit).all()
    return convertRawToJsonArray(gc.CATEGORY, raw)

def getUnits(value, offset, limit):
    raw = db.session.query(Unit.unit_id, Unit.unit_name).filter(Unit.unit_name.like(f'%{value}%')).offset(offset).limit(limit).all()
    return convertRawToJsonArray(gc.UNIT, raw)

def getStoreUnits(value, offset, limit,store):
    raw = db.session.query(Unit.unit_id, Unit.unit_name).filter(Unit.unit_name.like(f'%{value}%')).filter(Unit.store_id==store).offset(offset).limit(limit).all()
    return convertRawToJsonArray(gc.UNIT, raw)

def getOrders(username, offset, limit):
    current_user = getUser(username).user_id
    raw = db.session.query(SoldData.cart_id, Cart.item_id, Item.item_name, Item.price, Cart.count,SoldData.time_in_millis,SoldData.total_sold_price).join(Cart, SoldData.cart_id == Cart.cart_id).join(Item, Cart.item_id == Item.item_id).filter(SoldData.user_id == current_user).order_by(SoldData.time_in_millis.desc()).offset(offset).limit(limit).all()
    return convertRawToJsonArray(gc.ORDER, raw)

def getNotifications(username,offset,limit):
    current_user = getUser(username).user_id
    raw = (db.session.query(Notification).join(NotificationVsUser,Notification.notification_id == NotificationVsUser.notification_id).join(User,NotificationVsUser.user_id == User.user_id).filter(User.user_id == current_user).all())
    notificationArr = processNotification(convertRawToJsonArray(gc.NOTIFICATION,raw))
    return notificationArr

def getUserById(id):
    return db.session.query(User).filter_by(user_id=id).first()

def getCategory(id):
    return db.session.query(Category).filter_by(category_id=id).first()


def processNotification(notf):
    processed = []

    for notification in notf:
        notType = notification["type"]
        notfdata = json.loads(notification["notification_data"])
        msgType = notfdata["type"]
        message = ""
        name = ""
        user = ""
        hasConfirmation= False
        action_type = None

        if msgType == globalConstants.ADD_CATEGORY:

            if notType == globalConstants.APPROVAL:

                message = "Category Approval Request "
                category = getCategory(notfdata["category_id"])
                store = getStoreById(category.store_id)
                name = category.category_name
                user = store.store_name
                hasConfirmation = True
                action_type = globalConstants.APPROVE_CATEGORY

            elif notType == globalConstants.INFO:

                message = "Your Category Request Approved !!"
                name = getCategory(notfdata["category_id"]).category_name
                user = "Admin"

        elif msgType == globalConstants.ADD_STORE:

            if notType == globalConstants.APPROVAL:

                message = "Store Approval Request "
                store = getStoreById(notfdata["store_id"])
                name = store.store_name
                user = getUserById(store.manager_id).username
                hasConfirmation = True
                action_type = globalConstants.APPROVE_STORE

            elif notType == globalConstants.INFO:
                message = "Your Store Request Approved !!"
                name =  getStoreById(notfdata["store_id"]).store_name
                user = "Admin"

        data = {'notification_id': notification["notification_id"],'message': message,'name': name,'user': user,'approval': hasConfirmation,'action':action_type}
        processed.append(data)
    return processed



def getCategory(catId):
    return (db.session.query(Category).filter_by(category_id=catId).first())

def getProductStock(itemId):
    return (db.session.query(Item.quantity).filter_by(item_id=itemId).first()).quantity

def getSingleProduct(itemId):
    return (db.session.query(Item).filter_by(item_id=itemId).first())

def getInactiveMails(millis):
    connection = getSqliteConnection()
    cursor = connection.cursor()
    query = gc.INACTIVE_USERS_QUERY
    cursor.execute(query, (millis,))
    result = cursor.fetchall()
    emails = [row[0] for row in result]
    cursor.close()
    connection.close()
    return emails

def getMonthlyUserStatistics():
    connection = getSqliteConnection()
    cursor = connection.cursor()

    cursor.execute(gc.MONTHLY_STATS_QUERY.substitute(month=(cursor.execute("SELECT strftime('%Y-%m', 'now')").fetchone()[0])))

    monthlyStats = cursor.fetchall()

    cursor.execute(gc.OVERALL_STATS_QUERY)
    overallStats = cursor.fetchall()

    userStats = {}
    for email, monthly_amount_spent, monthly_items_bought in monthlyStats:
        userStats[email] = {"amountSpent": monthly_amount_spent, "itemsBought": monthly_items_bought}

    for email, overall_amount_spent, overall_items_bought in overallStats:
        if email in userStats:
            userStats[email]["totalAmountSpent"] = overall_amount_spent
            userStats[email]["totalItemBought"] = overall_items_bought
        else:
            userStats[email] = {"totalAmountSpent": overall_amount_spent, "totalItemBought": overall_items_bought,"amountSpent": 0,"itemsBought": 0}

    cursor.close()
    connection.close()

    return userStats


def exportStoreProductStats(storeId, tmpFolder):
    fileName = f'Product_details_{storeId}_{int(time.time())}.csv'
    filePath = os.path.join(tmpFolder, fileName)
    with open(filePath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Item Name', 'Category Name', 'Quantity', 'Unit Name', 'Total Revenue Made', 'Total Selling'])
        items = executeQuery(gc.PRODUCTS_EXPORT_QUERY.substitute(store=storeId))
        for item_name, category_name, quantity, unit_name, total_revenue, total_selling in items:
            writer.writerow([item_name, category_name, quantity, unit_name, total_revenue or 0, total_selling or 0 ])
    print(f'CSV file exported successfully: {fileName}')
    return filePath

def exportProductStats(tmpFolder):
    fileName = f'Product_details_{int(time.time())}.csv'
    filePath = os.path.join(tmpFolder, fileName)
    with open(filePath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Item Name', 'Category Name', 'Quantity', 'Unit Name', 'Total Revenue Made', 'Total Selling'])
        items = executeQuery(gc.PRODUCTS_EXPORT)
        for item_name, category_name, quantity, unit_name, total_revenue, total_selling in items:
            writer.writerow([item_name, category_name, quantity, unit_name, total_revenue or 0, total_selling or 0 ])
    print(f'CSV file exported successfully: {fileName}')
    return filePath

def addItem(product_id,productName,category,unit,quantity,price,image,store):

    db.session.add(Item(item_id=product_id, item_name=productName, category_id=category, price=price, quantity=quantity, unit=unit, store_id=store, image_url=image))
    db.session.commit()

    return product_id

def addCategory(category_id,category_name,fileName,store,userId):
    db.session.add(Category(category_id=category_id, category_name=category_name, image_url=fileName, store_id=store,is_approved=(userId == getAdmin())))
    db.session.commit()
    return category_id

def executeQuery(query):
    connection = getSqliteConnection()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result

def getSqliteConnection():
    cd = os.path.dirname(os.path.abspath(__file__))
    dbPath = os.path.join(cd, '..', 'instance', 'groceryStore.db')
    print(cd,dbPath)
    connection = sqlite3.connect(dbPath)
    return connection

def getIdByNotification(notification_id):
    notification = db.session.query(Notification).filter_by(notification_id=notification_id).first()
    if notification:
        try:
            notification_data = json.loads(notification.notification_data)
            store_id = notification_data.get('store_id')
            if store_id:
                return store_id
            category_id = notification_data.get('category_id')
            if category_id:
                return category_id
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    return None


def approveCategory(catId):
    db.session.execute(update(Category).where(Category.category_id == catId).values(is_approved=True))
    cat = getCategory(catId)
    store = getStoreById(cat.store_id)
    sendNotification(globalConstants.ADD_CATEGORY, cat.category_id , cat.category_name , None, globalConstants.INFO, store.manager_id)

def approveStore(storeId):
    db.session.execute(update(Store).where(Store.store_id == storeId).values(is_approved=True))
    db.session.commit()
    userId = changeRole(storeId)
    store = getStoreById(storeId)
    sendNotification(globalConstants.ADD_STORE, storeId, store.store_name, None, globalConstants.INFO, userId)

def deleteNotification(id):
    db.session.query(Notification).filter_by(notification_id=id).delete()
    db.session.commit()

def rejectStore(storeId):
    db.session.query(Store).filter(Store.store_id == storeId).delete()
    db.session.commit()
    return storeId

def rejectCategory(id):
    db.session.query(Category).filter(Category.category_id == id).delete()
    db.session.commit()
    return storeId

def changeRole(storeId):
    userId = getStoreById(storeId).manager_id
    db.session.execute(update(User).where(User.user_id == userId).values(user_role=globalConstants.MANAGER))
    db.session.commit()
    return userId

def isAdminUser(user):
    return getUser(user).user_role == globalConstants.ADMIN

def getAdmin():
    return db.session.query(User).filter_by(user_role=globalConstants.ADMIN).first().user_id

def isManagerOrAdmin(user):
    role = getUser(user).user_role
    return role == globalConstants.ADMIN or role == globalConstants.MANAGER

def addUnit(unitName,storeId):
    unitId = getGuid()
    db.session.add(Unit(unit_id=unitId, unit_name=unitName, store_id=storeId))
    db.session.commit()
    return unitId

def addSoldData(cartId, user_id, time,totalAmount):
    db.session.add(SoldData(cart_id=cartId, user_id=user_id, time_in_millis=time,total_sold_price=totalAmount))
    db.session.commit()
    return cartId

def addCart(cartId, item, count):
    uniqId = getGuid()
    db.session.add(Cart(unique_id=uniqId, cart_id=cartId, item_id=item, count=count))
    db.session.commit()
    return uniqId

def reduceQuantity(item,count):
    db.session.execute(update(Item).where(Item.item_id == item).values(quantity=count))
    db.session.commit()

def updateProduct(productId,data):
    db.session.query(Item).filter(Item.item_id == productId).update(data)
    db.session.commit()

def deleteProduct(itemId):
    db.session.query(Item).filter(Item.item_id == itemId).delete()
    db.session.commit()

def updateCategory(category_id,categoryName):
    db.session.execute(update(Category).where(Category.category_id == category_id).values(category_name=categoryName))
    db.session.commit()

def updateUnit(unit_id,unitName):
    db.session.execute(update(Unit).where(Unit.unit_id == unit_id).values(unit_name=unitName))
    db.session.commit()

def get_store_statistics(store_id,user,isAdmin):
    store_statistics = []

    total_selling = None
    total_categories = None
    total_customers = None
    total_products = None
    total_revenue = None


    store = Store.query.filter_by(store_id=store_id).first()
    if store:
        if(isAdmin):
            total_selling = (db.session.query(func.sum(Cart.count)).join(Item, Cart.item_id == Item.item_id).scalar() or 0)
            total_categories = Category.query.filter_by(is_approved=True).count()
            total_customers = (db.session.query(func.count(func.distinct(SoldData.user_id))).join(Cart,Cart.cart_id == SoldData.cart_id).join(Item, Item.item_id == Cart.item_id).scalar() or 0)
            total_products = Item.query.count()
            total_revenue = (db.session.query(func.sum(SoldData.total_sold_price)).join(Cart,Cart.cart_id == SoldData.cart_id).join(Item, Item.item_id == Cart.item_id).scalar() or 0)
        else:
            total_selling = (db.session.query(func.sum(Cart.count)).join(Item, Cart.item_id == Item.item_id).filter(Item.store_id == store_id).scalar() or 0)
            total_categories = Category.query.filter_by(store_id=store_id, is_approved=True).count()
            total_customers =(db.session.query(func.count(func.distinct(SoldData.user_id))).join(Cart, Cart.cart_id == SoldData.cart_id).join(Item, Item.item_id == Cart.item_id).filter(Item.store_id == store_id).scalar() or 0)
            total_products = Item.query.filter_by(store_id=store_id).count()
            total_revenue = (db.session.query(func.sum(SoldData.total_sold_price)).join(Cart, Cart.cart_id == SoldData.cart_id).join(Item, Item.item_id == Cart.item_id).filter(Item.store_id == store_id).scalar() or 0)


        store_data = {
            'store_name': store.store_name,
            'total_selling': total_selling,
            'total_categories': total_categories,
            'total_customers': total_customers,
            'total_products': total_products,
            'total_revenue': total_revenue,
            'username':user,
            'userType' : 'Admin' if isAdmin else 'Manager'
        }
    return store_data
