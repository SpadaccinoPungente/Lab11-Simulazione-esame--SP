import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.id_map_genres = {g.GenreId: g for g in DAO.getAllGenres()}
        self.id_map_artists = {a.ArtistId: a for a in DAO.getAllArtistsWPopularity()}

    def getAllGenres(self):
        return self.id_map_genres.values()

    def buildGraph(self, selected_genre_id):

        self.graph.clear()

        nodes_by_id = DAO.getArtistsByGenre(selected_genre_id)
        nodes = [self.id_map_artists[id] for id in nodes_by_id]
        self.graph.add_nodes_from(nodes)

        all_edges = DAO.getAllEdges(selected_genre_id)

        for e in all_edges:
            a = self.id_map_artists[e[0]]
            b = self.id_map_artists[e[1]]
            w = a.Popularity + b.Popularity
            if a.Popularity > b.Popularity:
                self.graph.add_edge(a, b, weight=w)
            elif b.Popularity > a.Popularity:
                self.graph.add_edge(a, b, weight=w)
            else:
                self.graph.add_edge(a, b, weight=w)
                self.graph.add_edge(a, b, weight=w)

    def getGraphDetails(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()