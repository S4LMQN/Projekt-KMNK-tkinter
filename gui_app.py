import tkinter
import from_csv
import os
from tkinter import messagebox
from LeastSquares import Regression


class LinearRegressionApp():

    # W konstruktorze klasy LinearRegressionApp tworzymy główne okno aplikacji
    # oraz wywołujemy metody do budowania interfejsu użytkownika.
    def __init__(self):
        # Tworzenie głównego okna aplikacji
        self.window = tkinter.Tk()
        self.window.title("Regresja liniowa")
        self.window.geometry("600x700")

        # W procesie wybierania zmiennch powstają pola klasy, które przechowują wybrane przez użytkownika zmienne
        # Ułatwi to późniejsze przekazywanie ich do funkcji regresji liniowej.
        # Każda zmienna jest nazwą klucza ze słownika pobranego z pliku CSV
        self.ZmiennaZaleznaDoRegresji = None
        self.ZmienneNiezalezneDoRegresji = []

        # Lista przechowująca wszystkie zmienne z pliku CSV
        self.wszystkieZmienneLista = None

        # Słownik przechowujący wszystkie zmienne wraz z obserwacjami z pliku CSV
        self.SlownikZeWszystkimiZmiennymi = {}

        # Budowanie wszystkich obiektów interfejsu użytkownika
        self.buildCsvFrame() # Ramka do wczytywania pliku CSV
        self.buildVariableFrame() # Ramka do wyboru zmiennych
        self.buildRegressionButton() # Przycisk do uruchomienia regresji liniowej po kliknięciu następuje użycie funkcji buildRegressionWindow()

        # Uruchomienie głównej pętli aplikacji
        self.window.mainloop()

    def buildCsvFrame(self):
        # Ramka główna dla pliku CSV
        csvFrame = tkinter.Frame(
            self.window,
            bg="lightgrey",
            width=370,
            height=100,
        )
        csvFrame.pack(
            anchor='n',
            padx=25,
            pady=15
        )
        # Zapobiega zmianie rozmiaru okna na podstawie jego zawartości
        csvFrame.pack_propagate(False)

        # Label, tekst: Podaj nazwę pliku CSV
        csvLabel = tkinter.Label(
            csvFrame,
            text="Podaj nazwę pliku CSV (wraz z rozszerzeniem):",
            bg="lightgrey",
            font=("Arial", 10)
        )
        csvLabel.pack(
            side="top",
            pady=5
        )

        # Pole tekstowe do wprowadzenia nazwy pliku CSV
        self.csvEntry = tkinter.Entry(
            csvFrame,
            width=30,
            bg="white",
            font=("Arial", 10)
        )
        self.csvEntry.pack(
            side="top",
            padx=5,
            pady=5)

        # Przycisk do wczytania pliku CSV
        loadCsvButton = tkinter.Button(
            csvFrame,
            text="Wczytaj plik CSV",
            command=self.loadCsvFile,
            bg="white",
        )
        loadCsvButton.pack(
            side="top",
            padx=10,
            pady=3
        )

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
            side="top",
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
        self.wszystkieZmienneLista = tkinter.Listbox(
            wszystkieZmienneListaFrame,
            height=400,
            bg="white",
            font=("Arial", 10),
            selectmode='single'
        )
        self.wszystkieZmienneLista.pack(
            anchor='nw',
        )
        # Ramka wybranej zmiennej zależnej i niezaleznej wraz z etykietą do niej
        wybranaZmiennaZaleznaFrame = tkinter.Frame(
            variableFrame,
            bg="lightgrey",
            width=125,
            height=400
        )
        wybranaZmiennaZaleznaFrame.pack(
            side="right",
            padx=12,
            pady=10
        )
        wybranaZmiennaZaleznaFrame.pack_propagate(False)

        # Pole tekstowe wybranej zmiennej zależnej
        self.zmiennaZaleznaEntry = tkinter.Label(
            wybranaZmiennaZaleznaFrame,
            width=30,
            bg="white",
            font=("Arial", 13)
        )
        self.zmiennaZaleznaEntry.pack(
            side='top',
            padx=0,
            pady=0
        )
        # Listbox wybranych zmiennych niezależnych
        self.zmienneNiezalezneEntry = tkinter.Listbox(
            wybranaZmiennaZaleznaFrame,
            height=12,
            bg="white",
            font=("Arial", 13),
            selectmode='single'
        )
        self.zmienneNiezalezneEntry.pack(
            side='bottom',
            padx=0,
            pady=3
        )

        # Label, tekst: Zmienne zależne (X)
        wybranaZmiennaZaleznaLabel = tkinter.Label(
            wybranaZmiennaZaleznaFrame,
            text="Zmienne zależne (X)",
            bg="lightgrey",
            font=("Arial", 10)
        )
        wybranaZmiennaZaleznaLabel.pack(
            side='bottom',
            padx=0,
            pady=0
        )

        # Ramka przycisków do dodawania zmiennych
        buttonsFrame = tkinter.Frame(
            variableFrame,
            bg="lightgrey",
            width=60,
            height=500
        )
        buttonsFrame.pack(
            anchor='nw',
            padx=10,
            pady=10,
        )
        buttonsFrame.pack_propagate(False)

        # Przycisk do dodania zmiennej zależnej
        dodajZmiennaZaleznaButton = tkinter.Button(
            buttonsFrame,
            command=self.WypiszWybranaZmiennaZalezna,
            height=3,
            width=10,
            bg="lightblue",
            text="\u2794",
            font=("Arial", 13)
        )
        dodajZmiennaZaleznaButton.pack(
            side="top",
            pady=10
        )

        # Przycisk do usunięcia zmiennej niezależnej
        usunZmiennaNiezaleznaButton = tkinter.Button(
            buttonsFrame,
            command=self.UsunZmiennaNiezalezna,
            height=3,
            width=10,
            bg="lightblue",
            text="\u2190",
            font=("Arial", 13, "bold")
        )
        usunZmiennaNiezaleznaButton.pack(
            side="bottom",
            pady=30
        )

        # Przycisk do dodania zmiennej niezależnej
        dodajZmiennaNiezaleznaButton = tkinter.Button(
            buttonsFrame,
            command=self.DodajDoWybranychZmiennaNiezalezna,
            height=3,
            width=10,
            bg="lightblue",
            text="\u2794",
            font=("Arial", 13)
        )
        dodajZmiennaNiezaleznaButton.pack(
            side="bottom",
            pady=30
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
            bg="lightgrey",
            font=("Arial", 12)
        )
        startRegressionButton.pack(
            side="bottom",
            pady=30
        )

    # Funkcja budująca okno z wynikami regresji liniowej
    def buildRegressionWindow(self):

        # Przypisanie wybranych zmiennych do pól klasy
        self.ZmiennaZaleznaDoRegresji = self.zmiennaZaleznaEntry.cget('text')
        self.ZmienneNiezalezneDoRegresji = list(self.zmienneNiezalezneEntry.get(0, tkinter.END))

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


    def WypiszWybranaZmiennaZalezna(self):
        if len(self.wszystkieZmienneLista.curselection()) > 0:
            # Pobranie wybranej zmiennej z label
            wybranaZmienna = self.wszystkieZmienneLista.get(tkinter.ACTIVE)
            # Wyświetlenie zmiennej w polu tekstowym
            self.zmiennaZaleznaEntry.config(text=wybranaZmienna)

        else:
            messagebox.showerror("Błąd", "Nie wybrano żadnej zmiennej.")

    def DodajDoWybranychZmiennaNiezalezna(self):
        if len(self.wszystkieZmienneLista.curselection()) > 0:
            # Pobranie wybranej zmiennej z listy
            wybranaNiezalezna = self.wszystkieZmienneLista.get(tkinter.ACTIVE)

            # Sprawdzenie, czy zmienna już istnieje w liście zmiennych niezależnych
            if wybranaNiezalezna not in self.zmienneNiezalezneEntry.get(tkinter.END):
                # Dodanie zmiennej do listbox zmiennych niezależnych
                self.zmienneNiezalezneEntry.insert(tkinter.END, wybranaNiezalezna)
            else:
                messagebox.showwarning(
                    "Ostrzeżenie", "Ta zmienna jest już dodana.")

        else:
            messagebox.showerror("Błąd", "Nie wybrano żadnej zmiennej.")
        self.ZmienneNiezalezneDoRegresji.append(wybranaNiezalezna)

    def UsunZmiennaNiezalezna(self):
        if len(self.zmienneNiezalezneEntry.curselection()) > 0:
            # Usunięcie zmiennej z listboxa zmiennych niezależnych
            self.zmienneNiezalezneEntry.delete(tkinter.ACTIVE)
        else:
            messagebox.showerror("Błąd", "Nie wybrano żadnej zmiennej do usunięcia.")

    def loadCsvFile(self):
        # Obsługa błędów przy wczytywaniu pliku CSV:
        # 1. ValueError(Warość jest pusta) jest wywoływany w tej funkcji.
        # 2. FileNotFoundError(Plik nie istnieje) oraz FileExistsError(plik nie kończy sie na .csv) są wywoływane w module from_csv.py.

        try:
            if self.csvEntry.get() == "":
                raise ValueError("Nazwa pliku CSV nie może być pusta.")

            # Przetworzenie ścieżki
            basic_path = os.path.dirname(__file__)
            full_path = os.path.join(basic_path, self.csvEntry.get())

        except ValueError as e:
            messagebox.showerror("Błąd", str(e))
        except FileNotFoundError as e:
            messagebox.showerror("Błąd", str(e))
        except FileExistsError as e:
            messagebox.showerror("Błąd", str(e))

        else:
            try:
                dataDict = from_csv.read_csv(full_path)
                self.SlownikZeWszystkimiZmiennymi = {key: from_csv.clean(value) for key, value in dataDict.items()}
                for key in dataDict.keys():
                    self.wszystkieZmienneLista.insert(tkinter.END, key)

                messagebox.showinfo("Sukces", "Plik CSV został wczytany pomyślnie." +
                                "\n" + "Teraz już możesz wybrać zmienne.")
                self.csvEntry.delete(0, tkinter.END)
            except ValueError:
                messagebox.showerror("Błąd", "Dane muszą być liczbami.")

    def buildRegressionWindow(self):
    # Przypisanie wybranych zmiennych do pól klasy
        self.ZmiennaZaleznaDoRegresji = self.zmiennaZaleznaEntry.cget('text')
        self.ZmienneNiezalezneDoRegresji = list(self.zmienneNiezalezneEntry.get(0, tkinter.END))

    # Sprawdzenie czy wybrano zmienne
        if not self.ZmiennaZaleznaDoRegresji or not self.ZmienneNiezalezneDoRegresji:
            messagebox.showerror("Błąd", "Musisz wybrać zmienną zależną i przynajmniej jedną niezależną.")
            return

    # Tworzenie nowego okna
        regressionWindow = tkinter.Toplevel(self.window)
        regressionWindow.title("Regresja liniowa")
        regressionWindow.geometry("800x500")

    # Konfiguracja okna
        regressionWindow.transient(self.window)
        regressionWindow.grab_set()
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

    # Tworzenie obiektu Regression i wyświetlenie wyników
        try:
        # Utworzenie obiektu regresji
            regresja = Regression(samples=self.SlownikZeWszystkimiZmiennymi, y_label=self.ZmiennaZaleznaDoRegresji, x_labels=self.ZmienneNiezalezneDoRegresji)
        
        # Tworzenie pola tekstowego z wynikami
            results_text = tkinter.Text(
                regressionWindow,
                wrap=tkinter.WORD,
                font=("Courier New", 13)  # Używamy czcionki o stałej szerokości dla lepszego formatowania
            )
            results_text.pack(
                expand=True,
                fill=tkinter.BOTH,
                padx=10,
                pady=10
            )
        
        # Wstawienie wyników do pola tekstowego
            results_text.insert(tkinter.END, str(regresja))
            results_text.config(state=tkinter.DISABLED)  # Blokowanie edycji
        
        # Dodanie paska przewijania
            scrollbar = tkinter.Scrollbar(results_text)
            scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            results_text.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=results_text.yview)
        
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas obliczeń: {str(e)}")

object1 = LinearRegressionApp()
