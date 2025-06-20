# Least squares regression GUI app
### 17.06.2025
*co zostało zrobione?*
- Ramka główna do wybierania zmiennych a w niej zwykłe etykiety tekstowe opisujące przyszłe pola wybranych zmiennych.
- Przycisk do uruchomienia regresji (brak zabezpieczeń itd.)
- Nowe pojawiające się okno regresji z etykietą
- Funkcja do czytania pliku .csv zwracająca `dict` o postaci `{'column_name': [values]}`

### 18.06.2025
- Backend: Dodano calculate_covariance_matrix, t_student_critical_values.
- Backend: W klasie Regression zaktualizowano działanie r_sq(), dodano metody sst(), ssr(), sse(), calculate_squared_residual_error(), beta_error(i), calculate_confidence_interval(i), t_test(i), f_test(i). Nadpisano metodę \__str__().
- Frontend: Widok i funkcjonalność wczytywania danych z pliku CSV (`buildCsvFrame`)zostało zrobione w całości i jest gotowe.
- Frontend: Widok i funkcjonalność wybierania zmiennych zależnych i niezależnych (`buildVariableFrame`) zostało zrobione w całości i jest gotowe.
- (SUGESTIA): Klasa tworząca całą aplikację (`LinearRegressionApp`), ma atrybuty (`ZmiennaZaleznaDoRegresji`, `ZmienneNiezalezneDoRegresji`) to właśnie one są wynikiem działania finalnego wyboru zmiennych. Przypisanie poprawnych wartości następuje po kliknięciu przycisku '`Uruchom regresję`', w metodzie `buildRegressionWindow` Przechowują nazwy kluczy ze słownika (`SlownikZeWszystkimiZmiennymi`), dzięki temu przekazanie wybranych zmiennych do metod wykonywania regresji będzie prostsze.

### 19.05.2025
- Backend: Zmodyfikowano wyświetlanie obiektu klasy Regression

### 20.05.2025
- Backend: Zmodyfikowano konstruktor klasy Regression. Przyjmuje słownik nazwa_próby-próba, listę nazw zmiennych objaśniających x, str nazwy zmiennej objaśnianej y.
- Backend: Dodano funkcję clean(raw_list) w pliku read_csv.py.
