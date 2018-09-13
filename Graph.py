import sys
class Vertice:
    def __init__(self, name):
        self.name = name
        #self.valor = valor
        self.cor = "branco"
        self.predecessor = None
        self.tempDescoberta = -1
        self.tempFinalizado = -1

    def __str__(self):
        return str(self.name)

class Graph:
    def __init__(self, digrafo=0):
        self.grafo = []
        self.tempo = 0
        self.digrafo = digrafo
        self.vetorDistancia = []
        self.adjacentes = []

    #insere Nos    
    def insertNode(self, vertice):
        if(1 if self.verificaVertice(vertice) == None else 0):
            self.grafo.append(vertice)
            self.adjacentes.append([vertice,[]])

    #nomePosicao
    def achaPosicao(self, vertice):
        aux = -1
        for vert in self.grafo:
            if(vert.name == vertice.name):
                aux = self.grafo.index(vert)
        return aux
    
    #verificar se existe um vertice com esse nome
    def verificaVertice(self, vertice):
        aux = None
        for vert in self.grafo:
            if(vert.name == vertice.name):
                aux = vert
        return aux
    
    
    '''#insere Aresta
    def insertAresta(self,node1,node2):
        if node2 not in self.grafo[node1]:
            self.grafo[node1].append(node2)
        else:
            return "Aresta ja exite"
        
        if node1 not in self.grafo[node2]:
            self.grafo[node2].append(node1)
        else:
            return "Aresta ja exite"
    '''
    #insere aresta
    def insereAresta(self, vertice, vertice2):
        vertice = self.verificaVertice(vertice)
        vertice2 = self.verificaVertice(vertice2)
        index = self.grafo.index(vertice)
        self.adjacentes[index][1].append(vertice2)

        if self.digrafo == 0:
            index2 = self.grafo.index(vertice2)
            self.adjacentes[index2][1].append(vertice)
    
    #deleta Nos     
    def deleteNode(self,vertice):
        if(vertice in self.grafo):
            index = self.grafo.index(vertice)
            self.grafo.remove(vertice)
            self.adjacentes.pop(index)

        for vert in self.adjacentes:
            for vert2 in vert[1]:
                if(vert2 == vertice):
                    vert[1].remove(vertice)
    
    '''#deleta Aresta        
    def deleteAresta(self,node1,node2):
        if node2 in self.grafo[node1]:
            self.grafo[node1].remove(node2)
        else:
            return "aresta nao encontrada"

        if node1 in self.grafo[node2]:
            self.grafo[node2].remove(node1)
        else:
            return "aresta nao encontrada"
    '''
    #printa o grafo
    def printGraph(self):
        print("\nGrafo: "+self.getOrdem()+":")
        sys.stdout.write("[")
        for vertice in self.grafo:
            sys.stdout.write("- "+str(vertice)+" ")
        print("]")
    
    #retorna Ordem do grafo
    def getOrdem(self):
        return str(len(self.grafo))
    
    #retorna vertices do grafo
    def getNos(self):
        return self.grafo

    #def getNos()
    
    #retorna o Grau de um no
    def getGrau(self, node):
        cont = 0
        if(self.digrafo == 0):
            for nos in Graph.adjacentes:
                for vertice2 in nos[1]:
                    if(vertice2 == no):
                        cont+=1
        return cont

    #retorna lista de nos adjacentes
    def getAdjacentes(self, node):
        return self.adjacentes[self.grafo.index(no)][1]

    #retorna se o grafo e conexo ou nao
    def isConexo(self):
        return True if (-1 not in self.vetorDistancia) else False
    
    #retorna se o grafo e completo
    def isCompleto(self):
        cont = 0
        tam = len(self.grafo)
        visita = []

        for nos in self.adjacentes:
            vista.append(nos[0])
            for tam in nos[1]:
                if tam not in visita:
                    cont+=1
                    vista.append(tam)
            
        return True if (tam*(tam-1))/2 == cont else False

    #def isArvore()

    #def getFTD()

    #def getFTI()