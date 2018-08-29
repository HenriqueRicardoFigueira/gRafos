
class Graph:
    def __init__(self):
        self.grafo = {}
        
    def insertNode(self,node):
        self.grafo[node] = []
    
    def insertAresta(self,node1,node2):
        if node2 not in self.grafo[node1]:
            self.grafo[node1].append(node2)
        else:
            return "Aresta ja exite"
        
        if node1 not in self.grafo[node2]:
            self.grafo[node2].append(node1)
        else:
            return "Aresta ja exite"
         
    def deleteNode(self,node):
        for target in grafo:
            self.grafo[target].remove(node)
        self.grafo.pop(node)
            
    def deleteAresta(self,node1,node2):
        if node2 in self.grafo[node1]:
            self.grafo[node1].remove(node2)
        else:
            return "aresta nao encontrada"

        if node1 in self.grafo[node2]:
            self.grafo[node2].remove(node1)
        else:
            return "aresta nao encontrada"

    def printGraph(self):
        for indice in self.grafo:
            print(str(indice)+": "+str(self.grafo[indice]))