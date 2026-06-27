import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Lab11-Simulazione esame"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None

    def load_interface(self):
        self._title = ft.Text("TdP-Simulazione esame Chinook", color="blue", size=24)
        self._page.controls.append(self._title)

        self._ddGenre = ft.Dropdown(label="Genere", on_change=self._controller.abilitaBtnCreaGrafo)
        self._controller.fillDDGenre()
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo, disabled=True)

        self._page.controls.append(
            ft.Row([self._ddGenre, self._btnCreaGrafo], alignment=ft.MainAxisAlignment.CENTER)
        )

        self._ddArtist = ft.Dropdown(label="Artist", on_change=self._controller.abilitaBtnTrovaCammino)
        self._btnTrovaCammino = ft.ElevatedButton(text="Trova Cammino", on_click=self._controller.handleCammino, disabled=True)

        self._page.controls.append(
            ft.Row([self._ddArtist, self._btnTrovaCammino], alignment=ft.MainAxisAlignment.CENTER)
        )

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self.update_page()

    @property
    def controller(self):
        return self._controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()