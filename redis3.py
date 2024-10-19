from pprint import pprint

import redis

host_info2 = "redis-16093.c62.us-east-1-4.ec2.redns.redis-cloud.com"
r = redis.Redis(host=host_info2, port=16093, password='qCmdpTD842pCU8HpPxWb6AvNY4Mv9zgz', decode_responses=True, db = 0)

pprint(r.ping())
print()