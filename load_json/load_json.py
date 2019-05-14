import json
with open("medical.json","r") as file:
    tmp_file = file.read().split("\n")
    for file in tmp_file:
        tmp = json.loads(file)
        print("s")
print("s")