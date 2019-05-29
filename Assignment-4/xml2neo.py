import xml.etree.ElementTree as ET
from py2neo import Graph, Node, Relationship

dict = {}
visited = {}
edge = set({})
temp = 0
map = {}
def dfs(x):
    global temp
    cur_dict = {}
    map[x] = temp
    cur_dict["id"] = temp
    cur_dict["type"] = "tag"
    cur_dict["tag"] = x.tag
    cur_dict["text"] = x.text
    cur_dict["value"] = ""
    dict[temp] = cur_dict
    temp1 = temp
    temp+=1
    visited[x] = 1
    for attr,val in x.attrib.items():
        cur_dict = {}
        cur_dict["id"] = temp
        cur_dict["type"] = "attribute"
        cur_dict["tag"] = attr
        cur_dict["value"] = val
        cur_dict["text"] = ""
        dict[temp] = cur_dict
        edge.add((temp1,temp))
        temp += 1
    for i in x:
        if i==x:
            continue
        if i not in visited:
            dfs(i)
        edge.add((map[x], map[i]))

graph = Graph("http://localhost:7474/db/data/")
tx = graph.begin()
tree = ET.parse('try.xml')
root = tree.getroot()
var = 1
# print(root.tag)
dfs(root)

nodes = {}
for node in dict.values():
    nodes[node["id"]] = Node(node["type"], type=node["type"], tag=node["tag"], values=node["value"], text=node["text"])

for i in edge:
    if dict[i[1]]["type"] == "attribute":
        rel = Relationship(nodes[i[0]], "ATTRIBUTE", nodes[i[1]])
    else:
        rel = Relationship(nodes[i[1]], "IS_CHILD_OF", nodes[i[0]])
    graph.create(rel)
print(graph)
