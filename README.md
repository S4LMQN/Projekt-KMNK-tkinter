# Least squares regression GUI app
### 17.06.2025
*co zostało zrobione?*
- Ramka główna do wybierania zmiennych a w niej zwykłe etykiety tekstowe opisujące przyszłe pola wybranych zmiennych.
- Przycisk do uruchomienia regresji (brak zabezpieczeń itd.)
- Nowe pojawiające się okno regresji z etykietą
- Funkcja do czytania pliku .csv zwracająca `dict` o postaci `{'column_name': [values]}`

### Dalej - Backend
- Dodanie atrybutów w klasie `Regression`: $R^2$, ...
- Dodanie funkcji: `test_t_parameter`, `test_f`, `calculate_confidence_interval`
