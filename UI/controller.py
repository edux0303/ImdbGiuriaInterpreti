import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def fillDD(self):
        for g in self._model.getGenres():
            self._view._ddGenere.options.append(ft.dropdown.Option(g))
        for a in self._model.getAnni():
            self._view._ddAnno.options.append(ft.dropdown.Option(str(a)))
        self._view.update_page()

    # -------------------- PUNTO 1 --------------------

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        genere = self._view._ddGenere.value
        anno = self._view._ddAnno.value
        if genere is None or anno is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona genere e anno!"))
            self._view.update_page()
            return

        self._model.buildGraph(genere, int(anno))
        self._view.txt_result.controls.append(ft.Text("Grafo creato!"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))
        self._view.update_page()

    def handleAnalizza(self, e):
        self._view.txt_result.controls.clear()
        if self._model.getNumNodi() == 0:
            self._view.txt_result.controls.append(ft.Text("Crea prima il grafo!"))
            self._view.update_page()
            return

        interpreti, grado = self._model.getGradoMassimo()
        self._view.txt_result.controls.append(ft.Text(f"Grado massimo: {grado}"))
        for i in interpreti:
            self._view.txt_result.controls.append(ft.Text(f"{i}"))

        self._view.txt_result.controls.append(
            ft.Text(f"Numero componenti connesse: {self._model.getNumConnesse()}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Dimensione componente più grande: {self._model.getMaxComponente()}"))

        giovane, anziano = self._model.getGiovaneAnziano()
        if giovane is None:
            self._view.txt_result.controls.append(
                ft.Text("Nessun interprete con data di nascita valida"))
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Più giovane: {giovane} ({giovane.date_of_birth})"))
            self._view.txt_result.controls.append(
                ft.Text(f"Più anziano: {anziano} ({anziano.date_of_birth})"))
        self._view.update_page()

    # -------------------- PUNTO 2 --------------------

    def handleGiuria(self, e):
        self._view.txt_result.controls.clear()
        if self._model.getNumNodi() == 0:
            self._view.txt_result.controls.append(ft.Text("Crea prima il grafo!"))
            self._view.update_page()
            return

        try:
            k = int(self._view._txtK.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("K deve essere un intero!"))
            self._view.update_page()
            return
        if k < 2:
            self._view.txt_result.controls.append(ft.Text("K deve essere almeno 2!"))
            self._view.update_page()
            return

        giuria, giorni = self._model.getGiuria(k)
        if len(giuria) == 0:
            self._view.txt_result.controls.append(
                ft.Text(f"Impossibile trovare {k} interpreti in componenti diverse"))
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Differenza minima: {giorni} giorni"))
            for i in giuria:
                self._view.txt_result.controls.append(
                    ft.Text(f"{i} ({i.date_of_birth})"))
        self._view.update_page()