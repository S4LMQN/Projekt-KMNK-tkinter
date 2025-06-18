import tkinter
# import from_csv


class LinearRegressionApp():

    # W konstruktorze klasy LinearRegressionApp tworzymy główne okno aplikacji
    # oraz wywołujemy metody do budowania interfejsu użytkownika.
    def __init__(self):
        # Tworzenie głównego okna aplikacji
        self.window = tkinter.Tk()
        self.window.title("Regresja liniowa")
        self.window.geometry("800x800")



        # Budowanie wszystkich obiektów interfejsu użytkownika
        self.buildVariableFrame()
        self.buildRegressionButton()

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
        # Zapobiega zmianie rozmiaru okna na podstawie jego zawartości
        variableFrame.pack_propagate(False)

        # Ramka górna dla etykiet
        topLabelsFrame = tkinter.Frame(
            variableFrame,
            bg="lightgrey",
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

        # Ramka listy wszystkich zmiennych
        wszystkieZmienneListaFrame = tkinter.Frame(
            variableFrame,
            bg="blue",
            width=115,
            height=400
        )
        wszystkieZmienneListaFrame.pack(
            side="left",
            padx=10,
            pady=10,
        )
        wszystkieZmienneListaFrame.pack_propagate(False)
        
        # Lista wszystkich zmiennych
        wszystkiZmienneLista = tkinter.Listbox(
            wszystkieZmienneListaFrame,
            height=400,
            bg="white",
            font=("Arial", 10),
            selectmode='single'
        )
        wszystkiZmienneLista.pack(
            anchor='nw',
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

    # Funkcja budująca przycisk do uruchomienia regresji liniowej

    def buildRegressionButton(self):
        startRegressionButton = tkinter.Button(
            self.window,
            text="Uruchom regresję",
            command=self.buildRegressionWindow,
            bg="white",
            font=("Arial", 12)
        )
        startRegressionButton.pack(
            side="bottom",
            pady=20
        )

    # Funkcja budująca okno z wynikami regresji liniowej
    def buildRegressionWindow(self):
        # Tworzenie nowego okna
        regressionWindow = tkinter.Toplevel(self.window)
        regressionWindow.title("Regresja liniowa")
        regressionWindow.geometry("800x500")

        # Konfiguracja okna
        # Okno będzie zawsze na wierzchu okna głównego
        regressionWindow.transient(self.window)
        # Blokuje interakcję z głównym oknem, dopóki to nie zostanie zamknięte
        regressionWindow.grab_set()
        # Zapobiega zmianie rozmiaru okna na podstawie jego zawartości
        regressionWindow.pack_propagate(False)

        # Label, Tekst: Regresja liniowa
        headerLabel = tkinter.Label(
            regressionWindow,
            text="Wyniki regresji",
            font=("Arial", 16, "bold"),
        )
        headerLabel.pack(
            side="top",
            pady=10
        )
    
    


object1 = LinearRegressionApp()
