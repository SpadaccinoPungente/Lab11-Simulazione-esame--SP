import copy
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.id_map_genres = {g.GenreId: g for g in DAO.getAllGenres()}
        self.id_map_artists = {a.ArtistId: a for a in DAO.getAllArtistsWPopularity()}

        self.best_path = None
        self.best_score = None

    def getAllGenres(self):
        return self.id_map_genres.values()

    def buildGraph(self, selected_genre_id):
        self.graph.clear()

        nodes_by_id = DAO.getArtistsIdByGenre(selected_genre_id)
        nodes = [self.id_map_artists[artist_id] for artist_id in nodes_by_id]
        self.graph.add_nodes_from(nodes)

        all_edges = DAO.getEdgesByGenre(selected_genre_id)

        for e in all_edges:
            a = self.id_map_artists[e[0]]
            b = self.id_map_artists[e[1]]
            w = a.Popularity + b.Popularity

            if a.Popularity > b.Popularity:
                self.graph.add_edge(a, b, weight=w)
            elif b.Popularity > a.Popularity:
                self.graph.add_edge(b, a, weight=w)
            else:
                self.graph.add_edge(a, b, weight=w)
                self.graph.add_edge(b, a, weight=w)

        return nodes

    def getGraphDetails(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()

    def getMostInfluentialArtist(self):
        most_influential_artist = None
        max_influence = -1
        for node in self.graph.nodes():
            weight_in = sum([e[2]['weight'] for e in self.graph.in_edges(node, data=True)])
            weight_out = sum([e[2]['weight'] for e in self.graph.out_edges(node, data=True)])
            influence = weight_out - weight_in

            if influence > max_influence:
                most_influential_artist = node
                max_influence = influence

        return most_influential_artist, max_influence

    def getTop5EdgesByWeight(self):
        return sorted(self.graph.edges(data=True), key=lambda e: e[2]['weight'], reverse=True)[:5]

    """
    PUNTO	2	
    a. Selezionare dal corrispondente menu a tendina un artista. Popolare il menu a tendina con artisti del genere 
    selezionato dal menu a tendina del genere del punto 1. 
    b. Facendo click sul pulsante “Cerca percorso”, individuare il percorso più lungo.  
    c. Trovare un cammino semplice di lunghezza massima tale che ogni arco successivo abbia peso strettamente 
    crescente. 
    """

    def trovaCammino(self, id_nodo_partenza):
        self.best_path = []
        self.best_score = 0

        parziale = [self.id_map_artists[id_nodo_partenza]]
        self._ricorsione(parziale)

        return self.best_path, self.best_score

    def _ricorsione(self, parziale):
        # 1. PRUNING (Uscita anticipata)
        # In questo caso specifico non abbiamo condizioni che ci fanno scartare
        # a priori un percorso in corso, perché la validità è gestita dal metodo is_valid.

        # 2. CASO TERMINALE / OBIETTIVO
        # Poiché cerchiamo il percorso più lungo in assoluto, ogni nodo aggiunto
        # genera un percorso potenzialmente da record.
        # Valutiamo se la lunghezza del cammino attuale supera il record precedente.
        if len(parziale) > self.best_score:
            self.best_path = copy.deepcopy(parziale)
            self.best_score = len(parziale)

        # 3. GENERAZIONE OPZIONI
        ultimo_nodo = parziale[-1]
        vicini = self.graph.successors(ultimo_nodo)

        # 4. CICLO E BACKTRACKING
        for vicino in vicini:
            # Separiamo la logica di controllo nel metodo helper
            if self.is_valid(vicino, parziale):
                parziale.append(vicino)  # 1. DO (Scelta)
                self._ricorsione(parziale)  # 2. RECURSE (Esplorazione)
                parziale.pop()  # 3. UNDO (Backtracking)

    def is_valid(self, vicino, parziale):
        # Regola 1: Cammino semplice (nessun nodo ripetuto)
        if vicino in parziale: return False

        # Regola 2: Gli archi successivi devono avere peso strettamente crescente
        # Possiamo fare questo controllo solo se ci sono almeno 2 nodi in 'parziale'
        # (cioè se stiamo per aggiungere almeno il secondo arco)
        if len(parziale) >= 2:
            peso_arco_precedente = self.graph[parziale[-2]][parziale[-1]]['weight']
            peso_arco_nuovo = self.graph[parziale[-1]][vicino]['weight']

            # Se il nuovo peso non è STRETTAMENTE maggiore del precedente, la mossa non è valida
            if peso_arco_nuovo <= peso_arco_precedente: return False

        return True