from Graph import Graph


def main():

    grafo = Graph()
    grafo.insertNode(1)
    grafo.insertNode(2)
    grafo.insertNode(3)
    grafo.insertNode(4)
    grafo.insertNode(5)

    grafo.insertAresta(1,2)
    grafo.insertAresta(1,3)
    grafo.insertAresta(2,3)

    grafo.insertAresta(3,4)

    grafo.insertAresta(4,5)


    grafo.printGraph()

main()