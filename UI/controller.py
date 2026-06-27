import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def fillDDGenre(self):
        self._view._ddGenre.options = [
            ft.dropdown.Option(key=g.GenreId, text=g.Name)
            for g in self._model.getAllGenres()
        ]

    def abilitaBtnCreaGrafo(self, e):
        self._view._btnCreaGrafo.disabled = False
        self._view.update_page()

    def handleCreaGrafo(self, e):
        artists_by_genre = self._model.buildGraph(int(self._view._ddGenre.value))

        nn, ne = self._model.getGraphDetails()

        if not nn:
            self._view.create_alert("Grafo vuoto.")
            return

        self._view._ddArtist.options = [ft.dropdown.Option(key=a.ArtistId, text=a.Name) for a in artists_by_genre]

        self._view.txt_result.controls.clear()

        mia, mi = self._model.getMostInfluentialArtist()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato!"
                    f"\nNumero di nodi: {nn}"
                    f"\nNumero di archi: {ne}"
                    f"\nArtista più influente: {mia} ({mi})"))

        top5 = self._model.getTop5EdgesByWeight()
        self._view.txt_result.controls.append(ft.Text("\nTop 5 archi:"))
        for e in top5:
            self._view.txt_result.controls.append(ft.Text(f"{e[0]} -> {e[1]}: {e[2]['weight']}"))

        self._view.update_page()

    def abilitaBtnTrovaCammino(self, e):
        self._view._btnTrovaCammino.disabled = False
        self._view.update_page()

    def handleCammino(self, e):
        best_path, best_score = self._model.trovaCammino(int(self._view._ddArtist.value))

        self._view.txt_result.controls.clear()

        if not best_path:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino valido trovato a partire da questo artista."))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Cammino trovato! Lunghezza massima {best_score} archi:"))
            for nodo in best_path: self._view.txt_result.controls.append(ft.Text(f" - {nodo.Name}"))

        self._view.update_page()