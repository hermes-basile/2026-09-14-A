import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        txtInMin = self._view._txtRatingMin.value
        txtInMax = self._view._txtRatingMax.value

        if txtInMin is None or txtInMin.strip() == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Devi inserire qualche valore nel primo campo.", color="red"))
            self._view.update_page()
            return

        if txtInMax is None or txtInMax.strip() == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Devi inserire qualche valore nel secondo campo.", color="red"))
            self._view.update_page()
            return

        try:
            numeroMin = float(txtInMin)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("devi inserire un numero decimale", color= "red"))
            self._view._txtRatingMin.value = "8"
            self._view.update_page()
            return

        try:
            numeroMax = float(txtInMax)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("devi inserire un numero decimale", color= "red"))
            self._view._txtRatingMax.value = "10"
            self._view.update_page()
            return

        self._model.build_grafo(numeroMin, numeroMax)

        self._view._txt_result.controls.append(ft.Text("Grafo creato correttamente", color = "green"))

        self._view._txt_result.controls.append(ft.Text(f"il grafo ha {self._model.num_nodi()} nodi e {self._model.num_archi()} archi."))
        self._view._btnStampaInfo.disabled = False
        self._view.update_page()


    def handleStampaInfo(self, e):
        attore_grado_maggiore, grado_maggiore = self._model.attore_grado_maggiore()
        attore_pesi_massimo, peso_totale = self._model.attore_con_peso_maggiore()
        attore_giovane = self._model.attore_giovane()
        attore_anziano = self._model.attore_anziano()
        lista_5_archi = self._model.cinque_archi_peso_maggiore()

        if attore_grado_maggiore is not None:
            self._view._txt_result.controls.append(ft.Text(
                f"l'attore con il grado maggiore è: {attore_grado_maggiore.name}, con grado {grado_maggiore}"))
        else:
            self._view._txt_result.controls.append(ft.Text("Non c'è un attore che abbia questa caratteristica", color = "red"))

        if attore_pesi_massimo is not None:
            self._view._txt_result.controls.append(ft.Text(f"l'attore con somma pesi incidenti massima è: {attore_pesi_massimo.name} ({peso_totale})"))
        else:
            self._view._txt_result.controls.append(ft.Text("Non c'è alcun attore collegato ad un altro"))
        if attore_giovane is not None:
            self._view._txt_result.controls.append(ft.Text(
                f"l'attore più giovane è: {attore_giovane.name}, nato il {attore_giovane.date_of_birth}"))
        else:
            self._view._txt_result.controls.append(ft.Text("Non c'è alcun attore nel grafo creato che possa essere il più giovane"))

        if attore_anziano is not None:
            self._view._txt_result.controls.append(ft.Text(
                f"l'attore più anziano è: {attore_anziano.name}, nato il {attore_anziano.date_of_birth}"))
        else:
            self._view._txt_result.controls.append(ft.Text("Non c'è alcun attore nel grafo creato che possa essere il più anziano"))

        if len(lista_5_archi) > 0 :
            for tupla in lista_5_archi:
                self._view._txt_result.controls.append(ft.Text(f"{tupla[0]} --> {tupla[1]}, peso {tupla[2]["peso"]}"))
                self._view.update_page()
        else:
            self._view._txt_result.controls.append("non c'è alcun attore nella lista")

        self._view.update_page()








    def handleTrovaGruppo(self, e):
        pass
