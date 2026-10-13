import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self.lista_attori = DAO.getAllActor()
        self.idMapActor = {}

        for attore in self.lista_attori:
            self.idMapActor[attore.id] = attore

        self._grafo = nx.Graph()

    def build_grafo(self, rangeA, rangeB):
        self._grafo.clear()
        #nodi
        lista_nodi = []
        lista_id = DAO.getAllNodes(rangeA, rangeB)
        for id_actor in lista_id:
            nodo = self.idMapActor[id_actor]
            lista_nodi.append(nodo)
        for attore in lista_nodi:
            DAO.getFilmforActor(attore, rangeA, rangeB)

        self._grafo.add_nodes_from(lista_nodi)
        #archi
        #procedura DAO
        #self.add_archi_pesati_from_DAO(rangeA, rangeB)

        #procedura se non riesco a fare la query
        self.add_archi(rangeA, rangeB)

    def add_archi_pesati_from_DAO(self,rangeA, rangeB):
        lista_tuple = DAO.getArchi(rangeA, rangeB) #(u,v,peso)
        for u,v,peso in lista_tuple:
            nodo1 = self.idMapActor[u]
            nodo2 = self.idMapActor[v]
            peso_finale = int(peso)
            if self._grafo.has_edge(nodo1,nodo2):
                print("c'è qualche problema con gli archi")
            self._grafo.add_edge(nodo1, nodo2, peso= peso_finale)

    def ex_crea_dizionario_idActor_idFIlm(self,rangeA, rangeB):
        dizAttoreFilm = {}
        lista_tuple_attore_film = DAO.getAttoreFilm(rangeA, rangeB)
        for tupla in lista_tuple_attore_film:
            id_attore = tupla[0]
            id_film = tupla[1]
            if id_attore not in dizAttoreFilm.keys():
                dizAttoreFilm[id_attore] = []
            dizAttoreFilm[id_attore].append(id_film)
        return dizAttoreFilm

    def ex_crea_dizionario_idFilm_idActor(self, rangeA, rangeB):
        lista_tuple = DAO.getFilmAttore(rangeA, rangeB)
        dizionario = {}
        for id_film, id_actor in lista_tuple:
            if id_film not in dizionario.keys():
                dizionario[id_film] = []
            dizionario[id_film].append(id_actor)
        return dizionario

    def add_archi(self, rangeA, rangeB):
        dizionarioFilmAttori = self.ex_crea_dizionario_idFilm_idActor(rangeA, rangeB)
        for film in dizionarioFilmAttori.keys():
            lista_attori = dizionarioFilmAttori[film]
            for i in range (len(lista_attori)):
                for j in range(i+1, len(lista_attori)):
                    attore1 = self.idMapActor[lista_attori[i]]
                    attore2 = self.idMapActor[lista_attori[j]]
                    if self._grafo.has_edge(attore1, attore2):
                        self._grafo[attore1][attore2]["peso"] += 1
                    else:
                        self._grafo.add_edge(attore1, attore2, peso= 1)




    def attore_grado_maggiore(self):

        numero_ottimo  = 0
        attore_salvato = None
        for attore in list(self._grafo.nodes()):
            numero_collegamenti = self._grafo.degree(attore)
            if numero_collegamenti > numero_ottimo:
                numero_ottimo = numero_collegamenti
                attore_salvato = attore
        return attore_salvato,numero_ottimo

    def attore_con_peso_maggiore(self):
        attore_salvato = None
        somma_salvata = 0

        for attore in list(self._grafo.nodes()):
            somma_peso = self._grafo.degree(attore, weight="peso")
            if somma_peso > somma_salvata:
                somma_salvata = somma_peso
                attore_salvato = attore
        return attore_salvato, somma_salvata

    def cinque_archi_peso_maggiore(self):

        lista = list(self._grafo.edges(data=True))

        lista_ordinata = sorted(lista, key=lambda x: (-x[2]["peso"], x[0].name, x[1].name))
        return lista_ordinata[:5]


    def attore_giovane(self):
        lista_attori = list(self._grafo.nodes)
        lista_ammissibili = []
        if len(lista_attori) > 0:
            for attore in lista_attori:
                if attore.date_of_birth is not None:
                    lista_ammissibili.append(attore)

        if len(lista_ammissibili) > 0 :
            attore_salvato = lista_ammissibili[0]
            print(attore_salvato)
            for attore in lista_ammissibili\
                    :
                if attore.date_of_birth > attore_salvato.date_of_birth :
                    attore_salvato = attore
            return attore_salvato
        return None

    def attore_anziano(self):
        lista_attori = list(self._grafo.nodes())
        lista_ammissibili = []

        for attore in lista_attori:
            if attore.date_of_birth is not None:
                lista_ammissibili.append(attore)

        if len(lista_ammissibili) > 0 :
            attore_salvato = lista_ammissibili[0]
            for attore in lista_ammissibili:
                if attore.date_of_birth < attore_salvato.date_of_birth:
                    attore_salvato = attore
            return attore_salvato
        else:
            return None

    def crea_albero(self, source, numero_attori):
        self.soluzione = []
        self.numero_totale_film = 0

        self.ricorsione([source], numero_attori)
        return self.soluzione

    def ricorsione(self, parziale, numero_attori):

        if len(parziale) == numero_attori and self.calcola_numero_film_lista(parziale) > self.numero_totale_film :
            self.numero_totale_film = self.calcola_numero_film_lista(parziale)
            self.soluzione = copy.deepcopy(parziale)
            return


        for candidato in self._grafo.nodes():
            if self.ammissibile(candidato, parziale):
                parziale.append(candidato)
                self.ricorsione(parziale, numero_attori)
                parziale.pop()

    def ammissibile(self, possibile, lista_parziale):
        count = 0
        for parziale in lista_parziale:
            if self._grafo.has_edge(possibile, parziale):
                count +=1


        if count == 1 and possibile not in lista_parziale:
            return True
        else:
            return False

    def calcola_numero_film_lista(self, lista_attori):
        if len(lista_attori) > 0:
            contatore = 0
            for attore in lista_attori:
                contatore += attore.count_film()
            return contatore
        return 0


















    def num_nodi(self):
        return len(self._grafo.nodes)
    def num_archi(self):
        return len(self._grafo.edges)