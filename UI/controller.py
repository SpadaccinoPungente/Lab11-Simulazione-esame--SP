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

    def handleCreaGrafo(self, e):

        if not self._view._ddGenre.value:
            self._view.create_alert("Seleziona un genere!")
            return

        self._model.buildGraph(self._view._ddGenre.value)

        nn, ne = self._model.getGraphDetails()

        if not nn:
            self._view.create_alert("Grafo vuoto.")
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato!\nNumero di nodi: {nn}\nNumero di archi: {ne}"))
        self._view.update_page()

    def handleCammino(self, e):
        pass