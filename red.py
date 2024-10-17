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

r10 = redis.Redis(db=10)

# with r10.pipeline() as pipe:
#     for h_id, hat in hats.items():
#         pipe.hmset(h_id, hat)
#     print(pipe.execute())

pprint(r10.hgetall("hat:56854717"))
print()
pprint(r10.keys())
print()


r10.hincrby("hat:56854717", "quantity", -1)
pprint(r10.hgetall("hat:56854717"))


# 199
# >>> r.hget("hat:56854717", "quantity")
# b'199'
# >>> r.hincrby("hat:56854717", "npurchased", 1)
# 1

