from string import Template

#APP_NAME
GROCERY_STORE= "grocery_store"

#TableNames
TABLE_USERS = 'users'
TABLE_CARTS_VS_USERS = 'cartvsusers'
TABLE_USERS_VS_PASSWORD = 'uservspassword'
TABLE_USERS_VS_ADDRESS = 'uservsaddress'
TABLE_CARTS = 'carts'
TABLE_MOBILE_NAME = 'mobilenumbers'
TABLE_NOTIFICATIONS = 'notifications'
TABLE_USER_NOTIFICATIONS = 'uservsnotifications'
TABLE_ITEMS = 'items'
TABLE_CATEGORIES = 'categories'
TABLE_UNITS = 'units'
TABLE_STORES = 'stores'
TABLE_SOLD_DATA = 'solddata'

#database
DATA_BASE_URI = 'sqlite:///groceryStore.db'

#redis
REDIS_URI = "redis://localhost:6379"
REDIS_BROKER_URI = "redis://localhost:6379/1"
REDIS_BACKEND_URI = "redis://localhost:6379/2"


#routes
BLUEPRINT_NAME = 'grocery_store_bp'


#admin credentials
ADMIN_USERNAME = "kannan"
ADMIN_PASS = "123321"
ADMIN_EMAIL= "kannansanchez@gmail.com"


#roles
ADMIN = 1
MANAGER = 2
USER = 3
UN_APPROVED_MANAGER = 4

#RESPONSE CODES
SUCCESS = 200
NOT_AUTHORIZED = 401
INTERNAL_SERVER_ERROR = 500
NOT_ALLOWED = 403


#DATA QUERIES TYPE
GET_HOMEPAGE_DATA = 1
GET_SEARCH_DATA = 2
GET_SORT_DATA = 3
GET_RANGE = 4
ORDERS = 5
NOTIFICATIONS = 6
GET_STORE = 7
GET_DASHBOARD = 8

#Query Type
SEARCH = 1
SORT_SELLING = 2
LESS_THAN_PRICE = 3
GREATER_THAN_PRICE = 4
SORT_LOW_HIGH = 5
SORT_HIGH_LOW = 6
BETWEEN_PRICE = 7
SORT_PRODUCT_SELLING = 8
SORT_CATEGORY_SELLING = 9
GET_CART = 10
PRODUCTS_LIST = 11
BY_CAT = 12
DELETE_ITEM = 13


#OBJECT TYPES
PRODUCT = 1
CATEGORY= 2
ORDER = 3
UNIT = 5
NOTIFICATION = 4


#NOTIFICATION TYPES
APPROVAL = 1
INFO = 2

#INSERT DATA
ADD_ITEM = 1
ADD_CATEGORY = 2
ADD_TO_CART = 3
DELETE_CART = 4
DELETE_FROM_CART = 5
ADD_STORE  = 6

#SCHEDULE CONSTANTS
INACTIVITY_EVERYDAY = True
INACTIVITY_MINUTE = False

MONTHLY_REPORT = True
DAILY_REPORT = False
WEEKLY_REPORT = False
EVERY_MINUTE_REPORT = False
MONTHLY_REMAINDER_MINUTE = 1

SEND_EXPORT_ALERT_MAIL = True

DAILY_REMAINDER_MINUTE = 1
DAILY_REMAINDER_HOUR =  9
DAILY_REMAINDER_HOUR_MINUTE =  0
ONEDAY_IN_MILLIS = 24 * 60 * 60 * 1000

MONTHLY_REMAINDER_HOUR =  9
DAY_OF_THE_MONTH =  31


#queries

INACTIVE_USERS_QUERY = "SELECT users.email FROM users LEFT JOIN soldData ON users.user_id = soldData.user_id WHERE soldData.time_in_millis IS NULL OR soldData.time_in_millis < ?"
ALL_MAILS = "SELECT users.email FROM users"
MONTHLY_STATS_QUERY = Template('SELECT u.email, COALESCE(SUM(sd.total_sold_price), 0) AS total_amount_spent, COALESCE(COUNT(sd.cart_id), 0) AS total_items_bought FROM users u LEFT JOIN soldData sd ON u.user_id = sd.user_id AND strftime(\'%Y-%m\', datetime(sd.time_in_millis / 1000, \'unixepoch\')) = \'$month\' GROUP BY u.email ')
OVERALL_STATS_QUERY = 'SELECT u.email, COALESCE(SUM(sd.total_sold_price), 0) AS overall_amount_spent, COALESCE(COUNT(sd.cart_id), 0) AS overall_items_bought FROM users u LEFT JOIN soldData sd ON u.user_id = sd.user_id GROUP BY u.email'
PRODUCTS_EXPORT_QUERY = Template('SELECT items.item_name, categories.category_name, items.quantity, units.unit_name, COALESCE(SUM(items.price * carts.count), 0) AS total_revenue, COALESCE(SUM(carts.count), 0) AS total_selling FROM items JOIN categories ON items.category_id = categories.category_id JOIN units ON items.unit = units.unit_id LEFT JOIN carts ON items.item_id = carts.item_id WHERE  items.store_id = \'$store\' GROUP BY items.item_id;')
PRODUCTS_EXPORT = 'SELECT items.item_name, categories.category_name, items.quantity, units.unit_name, COALESCE(SUM(items.price * carts.count), 0) AS total_revenue, COALESCE(SUM(carts.count), 0) AS total_selling FROM items JOIN categories ON items.category_id = categories.category_id JOIN units ON items.unit = units.unit_id LEFT JOIN carts ON items.item_id = carts.item_id GROUP BY items.item_id;'

#MAIL SERVER CONFIGURATIONS

MAIL_SERVER = 'smtp.gmail.com'
PORT = 587
USE_TLS = True
EMAIL = 'roller2022vs@gmail.com'
PASSWORD = 'dcdhjkdfbyzylalk'
SUBJECT = "Grocery Store"
INACTIVITY_NOTIFICATION_TEMPLATE = Template('<h5>Hello customer,<h5><p style="margin-left:50px">Greetings for the day, It seems that you haven\'t bought anything for past $timeline :)</p><p style="margin-left:50px">Some new products arrived at our store that might be useful to you ...</p><p style="margin-left:50px">write us if have any queries to : <a href="mailto:kannansanchez@gmail.com">kannansanchez@gmail.com</a></p><p>Warm regards</p><p style="color:red">Kannan S</p><p style="color:red">Admin team</p>')
REPORT_NOTIFICATION_TEMPLATE = Template('<h5>Hello customer,<h5><p style="margin-left:50px">Here\'s your monthly report for $month</p><ul style="margin-left:50px"><li>Amount spent : $spent</li><li>Number of Items Bought : $items</li><li>Total Amount spent (all months) : $totalSpent</li><li>Total items bought (all months) : $totalBought</li></ul><br><p style="margin-left:50px">write us if have any queries to :<a href="mailto:kannansanchez@gmail.com">kannansanchez@gmail.com</a></p><br><p>Warm regards</p><p style="color:red">Kannan S</p><p style="color:red">Admin team</p>')
EXPORT_NOTIFICATION_TEMPLATE = Template('<h5>Hello customer,<h5><p style="margin-left:50px"></p><p style="margin-left:50px">Your export was successful, PFA</p><p style="margin-left:50px">Time Took : $time seconds</p><p style="margin-left:50px">write us if have any queries to : <a href="mailto:kannansanchez@gmail.com">kannansanchez@gmail.com</a></p><p>Warm regards</p><p style="color:red">Kannan S</p><p style="color:red">Admin team</p>')


#UPDATE ACTIONS

APPROVE_STORE = 1
APPROVE_CATEGORY = 2
REMOVE_NOTIFICATION = 3


#OPERATIONS
ADD = "ADD"
UPDATE = "UPDATE"
DELETE = "DELETE"
