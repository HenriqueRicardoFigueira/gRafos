from Graph import Graph
from Graph import Vertice


def main():
    g = Graph()

    #criacao de vertices
    a = Vertice("a")
    g.insertNode(a)
    b = Vertice("b")
    g.insertNode(b)
    c = Vertice("c")
    g.insertNode(c)
    d = Vertice("d")
    g.insertNode(d)
    e = Vertice("e")
    g.insertNode(e)
    f = Vertice("f")
    g.insertNode(f)
    gr = Vertice("g")
    g.insertNode(gr)
    h = Vertice("h")
    g.insertNode(h)

    g.digrafo=1
    
    #insere adjascencia
    g.insereAresta(a,b)
    g.insereAresta(a,f)
    g.insereAresta(b,gr)
    g.insereAresta(b,c)
    g.insereAresta(b,d)
    g.insereAresta(d,e)
    g.insereAresta(gr,h)
    

    #teste busca
    g.buscaLargura(a)
    g.printTempoDescoberta()
    g.buscaProfundidade()


    # teste print
    g.printGraph()
    g.printAdjacencia()   
    g.printVetorDistancia()
    g.printTempoDescoberta()


main()