from py2neo import Graph, Node, Relationship

class Neo4j():
	graph = None
	def __init__(self):
		print("create neo4j class ...")

	def connectDB(self):
		self.graph = Graph("http://localhost:7474", username="neo4j", password="zhanghao666666")
		print('connect successed')

	def matchItembyTitle(self,value):
		answer = self.graph.find_one(label="Item",property_key="title",property_value=value)
		return answer

	# 根据title值返回entity1item
	def matchentity1ItembyTitle(self,value):
		answer = self.graph.find_one(label="entity1Item",property_key="title",property_value=value)
		return answer

	# 根据entity的名称返回关系
	def getEntityRelationbyEntity(self,value):
		answer = self.graph.data("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.title = \"" +value +"\" RETURN rel,entity2")
		return answer

	#查找entity1及其对应的关系（与getEntityRelationbyEntity的差别就是返回值不一样）
	def findRelationByEntity(self,entity1):
		answer = self.graph.data("MATCH (n1:entity1Item {title:\""+entity1+"\"})- [rel] -> (n2) RETURN n1,rel,n2" )
		if(len(answer) == 0):
			answer = self.graph.data("MATCH (n1:NewNode {title:\""+entity1+"\"})- [rel] -> (n2) RETURN n1,rel,n2" )
		return answer

	#查找entity2及其对应的关系
	def findRelationByEntity2(self,entity1):
		answer = self.graph.data("MATCH (n1)- [rel] -> (n2:entity1Item {title:\""+entity1+"\"}) RETURN n1,rel,n2" )
		if(len(answer) == 0):
			answer = self.graph.data("MATCH (n1)- [rel] -> (n2:NewNode {title:\""+entity1+"\"}) RETURN n1,rel,n2" )
		return answer

	#根据entity1和关系查找enitty2
	def findOtherEntities(self,entity,relation):
		answer = self.graph.data("MATCH (n1:entity1Item {title:\"" + entity + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2) RETURN n1,rel,n2" )
		if(len(answer) == 0):
			answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2) RETURN n1,rel,n2" )

		return answer

	#根据entity2和关系查找enitty1
	def findOtherEntities2(self,entity,relation):
		answer = self.graph.data("MATCH (n1)- [rel:RELATION {type:\""+relation+"\"}] -> (n2:entity1Item {title:\"" + entity + "\"}) RETURN n1,rel,n2" )
		if(len(answer) == 0):
			answer = self.graph.data("MATCH (n1)- [rel:RELATION {type:\""+relation+"\"}] -> (n2:NewNode {title:\"" + entity + "\"}) RETURN n1,rel,n2" )

		return answer

	#根据两个实体查询它们之间的关系
	def findRelationByEntities(self,entity1,entity2):
		answer = self.graph.data("MATCH (n1:entity1Item {title:\"" + entity1 + "\"})- [rel] -> (n2:entity1Item{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		if(len(answer) == 0):
			answer = self.graph.data("MATCH (n1:entity1Item {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		if(len(answer) == 0):
			answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:entity1Item{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		if(len(answer) == 0):
			answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )

		return answer

	#查询数据库中是否有对应的实体-关系匹配
	def findEntityRelation(self,entity1,relation,entity2):
		answer = self.graph.data("MATCH (n1:entity1Item {title:\"" + entity1 + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2:entity1Item{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		if(len(answer) == 0):
			answer = self.graph.data("MATCH (n1:entity1Item {title:\"" + entity1 + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		if(len(answer) == 0):
			answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2:entity1Item{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		if(len(answer) == 0):
			answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )

		return answer

	def matchforeveryone(self,mycypher):
		answer = self.graph.run(mycypher)
		return answer


test = Neo4j()
test.connectDB()
print(test.matchforeveryone(mycypher='MATCH p=()-[r:RELATION]->() RETURN p '))
# a = test.getLabeledHudongItem('labels.txt')
# print(a[10].openTypeList)