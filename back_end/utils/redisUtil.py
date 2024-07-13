from flask_redis import FlaskRedis

redis = FlaskRedis()


def addToCart(user_id, item_id, count):
    cart_key = f"cart:{user_id}"
    redis.hset(cart_key, item_id, count)

def getCart(user_id):
    cart_key = f"cart:{user_id}"
    return redis.hgetall(cart_key)

def getCartItem(user_id,item_id):
    cart_key = f"cart:{user_id}"
    return redis.hget(cart_key,item_id)

def deleteCart(user_id):
    cart_key = f"cart:{user_id}"
    redis.delete(cart_key)

def deleteFromCart(user_id, item_id):
    cart_key = f"cart:{user_id}"
    redis.hdel(cart_key, item_id)

def add(key, value):
    redis.set(key, value)

def remove(key):
    redis.delete(key)

def update(key, new_value):
    if redis.exists(key):
        redis.set(key, new_value)
        return True
    return False

def get(key):
    value = redis.get(key)
    return value
