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
