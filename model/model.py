import networkx as nx
from itertools import combinations

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._comp = {}
        self._candidati = []
        self._giuriaBest = []
        self._giorniBest = None

    def getGenres(self):
        return DAO.getGenres()

    def getAnni(self):
        return DAO.getAnni()

    # -------------------- PUNTO 1 --------------------

    def buildGraph(self, genere, anno):
        self._grafo.clear()
        self._idMap = {}

        nodi = DAO.getNodi(genere, anno)
        self._idMap = {reg.id: reg for reg in nodi}
        self._grafo.add_nodes_from(nodi)

        # a ogni interprete aggiungo i film del genere/anno in cui ha recitato
        for p, f in DAO.getCoppia(genere, anno):
            if p in self._idMap:
                self._idMap[p].film.add(f)

        # arco se hanno almeno un film in comune, peso = numero di film in comune
        for a, b in combinations(nodi, 2):
            comuni = a.film & b.film
            if len(comuni) > 0:
                self._grafo.add_edge(a, b, weight=len(comuni))

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getGradoMassimo(self):
        interpreti = []
        grado = -1
        for i in self._grafo.nodes():
            if self._grafo.degree(i) > grado:
                grado = self._grafo.degree(i)
                interpreti = [i]
            elif self._grafo.degree(i) == grado:
                interpreti.append(i)
        interpreti.sort(key=lambda x: x.name)
        return interpreti, grado

    def getNumConnesse(self):
        return nx.number_connected_components(self._grafo)

    def getMaxComponente(self):
        componenti = nx.connected_components(self._grafo)
        piuGrande = max(componenti, key=len)
        return len(piuGrande)

    def _dataValida(self, interprete):
        return interprete.date_of_birth is not None and interprete.date_of_birth.year > 1905

    def getGiovaneAnziano(self):
        validi = []
        for n in self._grafo.nodes():
            if self._dataValida(n):
                validi.append(n)
        if len(validi) == 0:
            return None, None
        giovane = max(validi, key=lambda x: x.date_of_birth)
        anziano = min(validi, key=lambda x: x.date_of_birth)
        return giovane, anziano

    # -------------------- PUNTO 2 --------------------

    def getGiuria(self, k):
        # 1. a ogni nodo assegno il numero della sua componente connessa
        self._comp = {}
        for indice, componente in enumerate(nx.connected_components(self._grafo)):
            for nodo in componente:
                self._comp[nodo] = indice

        # 2. candidati: solo date valide, dal più anziano al più giovane
        self._candidati = []
        for nodo in self._grafo.nodes():
            if self._dataValida(nodo):
                self._candidati.append(nodo)
        self._candidati.sort(key=lambda x: x.date_of_birth)

        # 3. soluzione migliore vuota
        self._giuriaBest = []
        self._giorniBest = None

        # 4. provo ogni candidato come primo della giuria
        for i in range(len(self._candidati)):
            self._ricorsione([self._candidati[i]], i, k)

        return self._giuriaBest, self._giorniBest

    def _ricorsione(self, parziale, ultimoIndice, k):
        # caso finale: ho K interpreti
        if len(parziale) == k:
            giorni = (parziale[-1].date_of_birth - parziale[0].date_of_birth).days
            if self._giorniBest is None or giorni < self._giorniBest:
                self._giuriaBest = list(parziale)
                self._giorniBest = giorni
            return

        # provo ad aggiungere un candidato nato dopo l'ultimo scelto
        for j in range(ultimoIndice + 1, len(self._candidati)):
            candidato = self._candidati[j]

            # pruning: troppo lontano dal primo -> anche i successivi lo sono
            if self._giorniBest is not None:
                distanza = (candidato.date_of_birth - parziale[0].date_of_birth).days
                if distanza >= self._giorniBest:
                    break

            # componente già usata da qualcuno della giuria? salto
            trovato = False
            for p in parziale:
                if self._comp[p] == self._comp[candidato]:
                    trovato = True
            if trovato:
                continue

            parziale.append(candidato)
            self._ricorsione(parziale, j, k)
            parziale.pop()


