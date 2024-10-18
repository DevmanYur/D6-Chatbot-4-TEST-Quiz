from pprint import pprint

import redis
# r = redis.Redis()
# r.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})
#
# print(r.get("Bahamas").decode("utf-8"))

import random

random.seed(444)
hats = {f"hat:{random.getrandbits(32)}": i for i in (
    {
        "color": "black",
        "price": 49.99,
        "style": "fitted",
        "quantity": 1000,
        "npurchased": 0,
    },
    {
        "color": "maroon",
        "price": 59.99,
        "style": "hipster",
        "quantity": 500,
        "npurchased": 0,
    },
    {
        "color": "green",
        "price": 99.99,
        "style": "baseball",
        "quantity": 200,
        "npurchased": 0,
    })
        }
r = redis.Redis(host='localhost', port=6379)
print(r)
pprint(r.keys())
print()

host_info2 = "redis-16093.c62.us-east-1-4.ec2.redns.redis-cloud.com"
redisObj = redis.Redis(host=host_info2, port=16093, password='qCmdpTD842pCU8HpPxWb6AvNY4Mv9zgz')

print(redisObj)
pprint(redisObj.keys())
# r11 = redis.Redis(db=11)
#
# with r11.pipeline() as pipe:
#     for h_id, hat in hats.items():
#         pipe.hmset(h_id, hat)
#     print(pipe.execute())
#
# pprint(r11.hgetall("hat:56854717"))
# print()
# pprint(r11.keys())
# print()
#
#
# r11.hincrby("hat:56854717", "quantity", -1)
# pprint(r11.hgetall("hat:56854717"))
#

# 199
# >>> r.hget("hat:56854717", "quantity")
# b'199'
# >>> r.hincrby("hat:56854717", "npurchased", 1)
# 1

