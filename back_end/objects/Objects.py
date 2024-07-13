from flask_sqlalchemy import SQLAlchemy
import globalConstants

ORM_BASE = SQLAlchemy()

class User(ORM_BASE.Model):
    __tablename__ = globalConstants.TABLE_USERS
    user_id = ORM_BASE.Column(ORM_BASE.String, primary_key=True)
    username = ORM_BASE.Column(ORM_BASE.String, unique=True, nullable=False)
    email = ORM_BASE.Column(ORM_BASE.String, unique=True, nullable=False)
    user_role = ORM_BASE.Column(ORM_BASE.Integer, nullable=False)
    def __init__(self, user_id, username, email, user_role):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.user_role = user_role

class UserPassword(ORM_BASE.Model):
    __tablename__ = globalConstants.TABLE_USERS_VS_PASSWORD

    user_id = ORM_BASE.Column(ORM_BASE.String, ORM_BASE.ForeignKey('users.user_id'), primary_key=True)
    password = ORM_BASE.Column(ORM_BASE.String, nullable=False)

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password


class CartVsUser(ORM_BASE.Model):
    __tablename__ =  globalConstants.TABLE_CARTS_VS_USERS

    cart_id = ORM_BASE.Column(ORM_BASE.String, ORM_BASE.ForeignKey('carts.cart_id'), primary_key=True)
    user_id = ORM_BASE.Column(ORM_BASE.String, ORM_BASE.ForeignKey('users.user_id'))

    def __init__(self, cart_id, user_id):
        self.cart_id = cart_id
        self.user_id = user_id


class Cart(ORM_BASE.Model):
    __tablename__ = globalConstants.TABLE_CARTS
    unique_id = ORM_BASE.Column(ORM_BASE.String, primary_key=True)
    cart_id = ORM_BASE.Column(ORM_BASE.String)
    item_id = ORM_BASE.Column(ORM_BASE.String, ORM_BASE.ForeignKey('items.item_id'), nullable=False)
    count = ORM_BASE.Column(ORM_BASE.Integer, nullable=False)
    def __init__(self, unique_id, cart_id, item_id, count):
        self.unique_id = unique_id
        self.cart_id = cart_id
        self.item_id = item_id
        self.count = count


class Item(ORM_BASE.Model):
    __tablename__ = globalConstants.TABLE_ITEMS
    item_id = ORM_BASE.Column(ORM_BASE.String, primary_key=True)
    item_name = ORM_BASE.Column(ORM_BASE.String, nullable=False)
    category_id = ORM_BASE.Column(ORM_BASE.String, ORM_BASE.ForeignKey('categories.category_id'), nullable=False)
    price = ORM_BASE.Column(ORM_BASE.Integer, nullable=False)
    quantity = ORM_BASE.Column(ORM_BASE.Integer, nullable=False)
    unit = ORM_BASE.Column(ORM_BASE.Integer, ORM_BASE.ForeignKey('units.unit_id'), nullable=False)
    store_id = ORM_BASE.Column(ORM_BASE.String, ORM_BASE.ForeignKey('stores.store_id'), nullable=False)
    image_url = ORM_BASE.Column(ORM_BASE.String, nullable=True)

    def __init__(self, item_id, item_name, category_id, price, quantity, unit, store_id, image_url):
        self.item_id = item_id
        self.item_name = item_name
        self.category_id = category_id
        self.price = price
        self.quantity = quantity
        self.unit = unit
        self.store_id = store_id
        self.image_url = image_url

class Category(ORM_BASE.Model):
    __tablename__ = globalConstants.TABLE_CATEGORIES

    category_id = ORM_BASE.Column(ORM_BASE.String, primary_key=True)
    category_name = ORM_BASE.Column(ORM_BASE.String, unique=True, nullable=False)
    image_url = ORM_BASE.Column(ORM_BASE.String, nullable=True)
    store_id = ORM_BASE.Column(ORM_BASE.String, ORM_BASE.ForeignKey('stores.store_id'), nullable=False)
    is_approved = ORM_BASE.Column(ORM_BASE.Boolean, nullable=False, default=False)
    def __init__(self, category_id, category_name, image_url, store_id,is_approved):
        self.category_id = category_id
        self.category_name = category_name
        self.store_id = store_id
        self.image_url = image_url
        self.is_approved = is_approved

class Unit(ORM_BASE.Model):
    __tablename__ = globalConstants.TABLE_UNITS

    unit_id = ORM_BASE.Column(ORM_BASE.String, primary_key=True)
    unit_name = ORM_BASE.Column(ORM_BASE.String, unique=True, nullable=False)
    store_id = ORM_BASE.Column(ORM_BASE.String, ORM_BASE.ForeignKey('stores.store_id'), nullable=False)

    def __init__(self, unit_id, unit_name, store_id):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.store_id = store_id

class Store(ORM_BASE.Model):
    __tablename__ = globalConstants.TABLE_STORES

    store_id = ORM_BASE.Column(ORM_BASE.String, primary_key=True)
    store_name = ORM_BASE.Column(ORM_BASE.String, unique=True, nullable=False)
    manager_id = ORM_BASE.Column(ORM_BASE.String, ORM_BASE.ForeignKey('users.user_id'), nullable=False)
    is_approved =  ORM_BASE.Column(ORM_BASE.Boolean, nullable=False, default=False)

    def __init__(self, store_id, store_name, manager_id, is_approved):
        self.store_id = store_id
        self.store_name = store_name
        self.manager_id = manager_id
        self.is_approved = is_approved

class SoldData(ORM_BASE.Model):
    __tablename__ = globalConstants.TABLE_SOLD_DATA

    cart_id = ORM_BASE.Column(ORM_BASE.String, ORM_BASE.ForeignKey('carts.cart_id'), primary_key=True)
    user_id = ORM_BASE.Column(ORM_BASE.String, ORM_BASE.ForeignKey('users.user_id'), nullable=False)
    time_in_millis = ORM_BASE.Column(ORM_BASE.Integer, nullable=False)
    total_sold_price = ORM_BASE.Column(ORM_BASE.String, nullable=False)
    def __init__(self, cart_id, user_id, time_in_millis,total_sold_price):
        self.cart_id = cart_id
        self.user_id = user_id
        self.time_in_millis = time_in_millis
        self.total_sold_price = total_sold_price

class Notification(ORM_BASE.Model):
    __tablename__ = globalConstants.TABLE_NOTIFICATIONS

    notification_id = ORM_BASE.Column(ORM_BASE.String, primary_key=True)
    notification_data = ORM_BASE.Column(ORM_BASE.String, nullable=False)
    type = ORM_BASE.Column(ORM_BASE.Integer, nullable=False)
    is_manadatory = ORM_BASE.Column(ORM_BASE.Boolean, nullable=False,default=False)

    def __init__(self, notification_id, notification_data, type, is_manadatory):
        self.notification_id = notification_id
        self.notification_data = notification_data
        self.type = type
        self.is_manadatory = is_manadatory


class NotificationVsUser(ORM_BASE.Model):
    __tablename__ = globalConstants.TABLE_USER_NOTIFICATIONS
    notification_id = ORM_BASE.Column(ORM_BASE.String, primary_key=True)
    user_id = ORM_BASE.Column(ORM_BASE.String, ORM_BASE.ForeignKey('users.user_id'), nullable=False)
    def __init__(self, notification_id, user_id):
        self.notification_id = notification_id
        self.user_id = user_id

