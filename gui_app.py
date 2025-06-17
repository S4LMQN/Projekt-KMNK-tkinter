import tkinter


class LinearRegressionApp():

    # W konstruktorze klasy LinearRegressionApp tworzymy główne okno aplikacji
    # oraz wywołujemy metody do budowania interfejsu użytkownika.
    def __init__(self):
        # Tworzenie głównego okna aplikacji
        self.window = tkinter.Tk()
        self.window.title("Regresja liniowa")
        self.window.geometry("1200x800")

        # Budowanie obiektów interfejsu użytkownika
        self.buildVariableFrame()

        # Uruchomienie głównej pętli aplikacji
        self.window.mainloop()


    # Funkcja tworząca ramkę do wyboru zmiennych
    def buildVariableFrame(self):

        # Ramka główna
        variableFrame = tkinter.Frame(
            self.window,
            bg="lightgrey",
            width=370,
            height=450
        )
        variableFrame.pack(
            side="left",
            padx=25
        )
        variableFrame.pack_propagate(False)

        # Ramka górna dla etykiet
        topLabelsFrame = tkinter.Frame(
            variableFrame,
            bg="blue",
            width=370,
            height=50
        )
        topLabelsFrame.pack(
            side="top",
            fill="x"
        )

        # Label, tekst: zmienne do wyboru
        wszystkieZmienneLabel = tkinter.Label(
            topLabelsFrame,
            text="Zmienne do wyboru",
            bg="lightgrey",
            font=("Arial", 10)
        )
        wszystkieZmienneLabel.pack(
            side="left",
            padx=10,
            pady=5
        )

        # Label, tekst: Zmienna zależna (Y)
        zmiennaZaleznaLabel = tkinter.Label(
            topLabelsFrame,
            text="Zmienna zależna (Y)",
            bg="lightgrey",
            font=("Arial", 10)
        )
        zmiennaZaleznaLabel.pack(
            side="right",
            padx=10,
            pady=5
        )

        # Label, tekst: Zmienne niezależne (X)
        zmiennaNiezaleznaLabel = tkinter.Label(
            variableFrame,
            text="Zmienne niezależne (X)",
            bg="lightgrey",
            font=("Arial", 10)
        )
        zmiennaNiezaleznaLabel.pack(
            anchor='ne',
            padx=5,
            pady=50
        )


object1 = LinearRegressionApp()
