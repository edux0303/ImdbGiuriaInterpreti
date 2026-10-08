import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Giuria Interpreti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None
        self._title = None
        self._ddGenere = None
        self._ddAnno = None
        self._btnCreaGrafo = None
        self._btnAnalizza = None
        self._txtK = None
        self._btnGiuria = None
        self.txt_result = None

    def load_interface(self):
        self._title = ft.Text("Giuria Interpreti", color="blue", size=24)
        self._page.controls.append(self._title)

        # PUNTO 1
        self._ddGenere = ft.Dropdown(label="Genere", width=250)
        self._ddAnno = ft.Dropdown(label="Anno", width=150)
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                               on_click=self._controller.handleCreaGrafo)
        self._btnAnalizza = ft.ElevatedButton(text="Analizza",
                                              on_click=self._controller.handleAnalizza)
        row1 = ft.Row([self._ddGenere, self._ddAnno, self._btnCreaGrafo, self._btnAnalizza],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # PUNTO 2
        self._txtK = ft.TextField(label="K", width=150, value="3")
        self._btnGiuria = ft.ElevatedButton(text="Cerca Giuria",
                                            on_click=self._controller.handleGiuria)
        row2 = ft.Row([self._txtK, self._btnGiuria],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

        self._controller.fillDD()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
