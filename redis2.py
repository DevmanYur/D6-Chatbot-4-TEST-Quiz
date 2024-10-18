from pprint import pprint

import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query


host_info2 = "redis-16093.c62.us-east-1-4.ec2.redns.redis-cloud.com"
r = redis.Redis(host=host_info2, port=16093, password='qCmdpTD842pCU8HpPxWb6AvNY4Mv9zgz')

user1 = {
    "user":{
        "name": "Paul John",
        "email": "paul.john@example.com",
        "age": 42,
        "city": "London"
    }
}
user2 = {
    "user":{
        "name": "Eden Zamir",
        "email": "eden.zamir@example.com",
        "age": 29,
        "city": "Tel Aviv"
    }
}
user3 = {
    "user":{
        "name": "Paul Zamir",
        "email": "paul.zamir@example.com",
        "age": 35,
        "city": "Tel Aviv"
    }
}

user4 = {
    "user":{
        "name": "Sarah Zamir",
        "email": "sarah.zamir@example.com",
        "age": 30,
        "city": "Paris"
    }
}
# r.json().set("user:1", Path.root_path(), user1)
# r.json().set("user:2", Path.root_path(), user2)
# r.json().set("user:3", Path.root_path(), user3)
# r.json().set("user:4", Path.root_path(), user4)

# schema = (TextField("$.user.name", as_name="name"),
#           TagField("$.user.city", as_name="city"),
#           NumericField("$.user.age", as_name="age"))
#
# r.ft().create_index(schema,
#                     definition=IndexDefinition(prefix=["user:"],
#                                                index_type=IndexType.JSON))

pprint(r.keys())

print()

# Простой поиск
q = r.ft().search("Paul")
print('Простой поиск :', q)
print()

# Фильтрация результатов поиска
q1 = Query("Paul").add_filter(NumericFilter("age", 30, 40))
rez = r.ft().search(q1)
print('Фильтрация результатов поиска :', rez)
print()

# Разбивка на страницы и упорядочивание результатов поиска
# Search for all users, returning 2 users at a time and sorting by age in descending order
offset = 0
num = 2
q = Query("*").paging(offset, num).sort_by("age", asc=False) # pass asc=True to sort in ascending order
rez = r.ft().search(q)
print('Разбивка на страницы и упорядочивание результатов поиска :', rez)
print()


# Подсчет общего количества элементов / Counting the total number of Items
q = Query("*").paging(0, 0)
rez = r.ft().search(q).total
print('Подсчет общего количества элементов :', rez)
print()




