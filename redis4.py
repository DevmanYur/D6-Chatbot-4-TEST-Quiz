from pprint import pprint

import redis



host = "redis-19445.c52.us-east-1-4.ec2.redns.redis-cloud.com"
port = 19445
password = 'kx7oAwxlp7JMLjhpzzUyOEz1hFuqUQKe'
r = redis.Redis(host=host, port=port, password=password, decode_responses=True)

print(r.ping())



pprint(r.keys())
pprint(r.get('1076073346'))
