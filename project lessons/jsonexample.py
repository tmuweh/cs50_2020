import json

x = '{"name":"Tangue", "age":"25", "city":"Bamenda" }'
w = {"name":"Tangue", "age":"25", "city":"Bamenda" }

y = json.loads(x)
z = json.dumps(w)

print(y)
print(z)