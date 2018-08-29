
class Graph:
    def __init__(self):
        self.grafo = {}

    #insere Nos    
    def insertNode(self,node):
        self.grafo[node] = []
    
    #insere Aresta
    def insertAresta(self,node1,node2):
        if node2 not in self.grafo[node1]:
            self.grafo[node1].append(node2)
        else:
            return "Aresta ja exite"
        
        if node1 not in self.grafo[node2]:
            self.grafo[node2].append(node1)
        else:
            return "Aresta ja exite"
    
    #deleta Nos     
    def deleteNode(self,node):
        for target in self.grafo:
            self.grafo[target].remove(node)
        self.grafo.pop(node)
    
    #deleta Aresta        
    def deleteAresta(self,node1,node2):
        if node2 in self.grafo[node1]:
            self.grafo[node1].remove(node2)
        else:
            return "aresta nao encontrada"

        if node1 in self.grafo[node2]:
            self.grafo[node2].remove(node1)
        else:
            return "aresta nao encontrada"
    
    #printa o grafo
    def printGraph(self):
        for indice in self.grafo:
            print(str(indice)+": "+str(self.grafo[indice]))
    
    #retorna Ordem do grafo
    def getOrdem(self):
        return len(self.grafo)
    
    #retorna vertices do grafo
    def getVertice(self):
        return self.grafo.keys()

    #def getNos()
    
    #retorna o Grau de um no
    def getGrau(self, node):
        return len(self.grafo[node])

    #retorna lista de nos adjacentes
    def getAdjacentes(self, node):
        return self.grafo[node]

    #retorna se o grafo e conexo ou nao
    def isConexo(self):
        for target in self.grafo:
            tamanho = len(self.grafo[target])
            if  tamanho ==  0:
                return False
        return True
    
    #retorna se o grafo e completo
    def isCompleto(self):
        for target in self.grafo:
            tamanho = len(self.grafo[target])
            if tamanho < tamanho - 1:
                return False
        return True

    #def isArvore()

    #def getFTD()

    #def getFTI()