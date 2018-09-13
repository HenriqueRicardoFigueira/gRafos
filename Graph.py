import sys

class Vertice:
    def __init__(self, name, valor=0.0):
        self.name = name
        self.valor = valor
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
    


    #printa o grafo
    def printGraph(self):
        print("\nGrafo: "+self.getOrdem()+":")
        sys.stdout.write("[")
        for vertice in self.grafo:
            sys.stdout.write("- "+str(vertice)+" ")
        print("]")
    
    #limpagrafo
    def limpaGrafo(self):
        self.grafo = []
        self.vetorDistancia = []
        self.adjacentes = []

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

    def buscaLargura(self, vertInicial):
        self.tempo = 0
        self.vetorDistancia = []

        #coloca os tempos como infinitos
        for i in self.grafo:
            self.vetorDistancia.append(-1)

        for vertice in self.grafo:
            if(vertice != vertInicial):
                vertice.cor = "branco"
                vertice.predecessor = -1

        index = self.grafo.index(vertInicial)
        self.grafo[index].cor = "cinza"
        self.grafo[index].tempDescoberta = self.tempo
        self.grafo[index].predecessor = -1
        self.vetorDistancia[index] = self.tempo

        filaVisitacao = []
        filaVisitacao.append(vertInicial)

        while(len(filaVisitacao) != 0):
            vertFila = filaVisitacao.pop()
            index = self.grafo.index(vertFila)
            vertFilaAdj = self.adjacentes[index][1]

            self.tempo = vertFila.tempDescoberta+1
            for vertAdj in vertFilaAdj:
                if(vertAdj.cor == "branco"):
                    vertAdj.cor = "cinza"
                    vertAdj.tempDescoberta = self.tempo
                    index = self.grafo.index(vertAdj)
                    self.vetorDistancia[index] = self.tempo
                    vertAdj.predecessor = vertFila
                    filaVisitacao.append(vertAdj)
            vertFila.cor = "preto"

    def printAdjacencia(self):
        print("\nAdjacencia "+self.getOrdem()+":")
        for vertice in self.adjacentes:
            sys.stdout.write(str(vertice[0])+" -> ")
            for vertice2 in vertice[1]:
                sys.stdout.write(str(vertice2))
                if(not vertice[1].index(vertice2) == len(vertice[1])-1):
                    sys.stdout.write(" - ")
            print()

    def printVetorDistancia(self):
        sys.stdout.write("[")
        for i in reversed(self.vetorDistancia) :
            if(i!=0):
                    sys.stdout.write(str(i))
                    sys.stdout.write(" ")
        sys.stdout.write("]\n\n")

    def printTempoDescoberta(self):
        print("\nTempos De Descoberta: "+self.getOrdem()+":")
        sys.stdout.write("[")
        for vertice in self.grafo:
            sys.stdout.write("- ("+str(vertice)+")"+str(vertice.tempDescoberta)+","+str(vertice.tempFinalizado)+" ")
        print("]\n")

    #Busca em profundidade
    def buscaProfundidade(self):
        self.tempo = 0

        for vertice in self.grafo:
                vertice.cor = "branco"
                vertice.predecessor = -1

        for vertice in self.grafo:
                if(vertice.cor == "branco"):
                    print("aqui :"+str(vertice))
                    self.buscaProfundidadeVisita(vertice)

    #Busca em prfundidade visita
    def buscaProfundidadeVisita(self,vertice):
        self.tempo +=1
        vertice.tempDescoberta = self.tempo
        vertice.cor = "cinza"
        print("visitando: "+str(vertice)+", tempo: "+str(self.tempo))

        index = self.achaPosicao(vertice)
        print(vertice)
        print(index)
        for vert in self.adjacentes[index][1]:
            vert = self.verificaVertice(vert)
            if(vert.cor == "branco"):
                vert.predecessor = vertice
                self.buscaProfundidadeVisita(vert)

        vertice.cor = "preto"
        self.tempo+=1
        print("finalizado: "+str(vertice)+", tempo: "+str(self.tempo))
        vertice.tempFinalizado = self.tempo