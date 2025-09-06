#!/usr/bin/env python3
"""
Generator Wykresu Gęstości Liczb Pierwszych
Program tworzy wykres gęstości liczb pierwszych używając pliku cache.
"""

import argparse
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import sys
from typing import Set, List, Tuple

# Nazwa domyślnego pliku cache
PLIK_CACHE_PIERWSZYCH = "pierwsze_cache.pkl"


def wyswietl_postep(aktualny, calkowity, prefix="Postęp", dlugosc=50):
    """Wyświetla pasek postępu który pozostaje w miejscu."""
    procent = (aktualny / calkowity) * 100
    wypelniona_dlugosc = int(dlugosc * aktualny // calkowity)
    pasek = '█' * wypelniona_dlugosc + '-' * (dlugosc - wypelniona_dlugosc)
    sys.stdout.write(f'\r{prefix}: |{pasek}| {procent:.1f}% ({aktualny:,}/{calkowity:,})')
    sys.stdout.flush()
    if aktualny == calkowity:
        sys.stdout.write('\n')
        sys.stdout.flush()


def wczytaj_cache(nazwa_pliku: str = PLIK_CACHE_PIERWSZYCH) -> Tuple[Set[int], int]:
    """Wczytaj cache liczb pierwszych z pliku."""
    if not os.path.exists(nazwa_pliku):
        raise FileNotFoundError(f"Plik cache '{nazwa_pliku}' nie istnieje")

    try:
        with open(nazwa_pliku, 'rb') as f:
            dane = pickle.load(f)

        pierwsze = dane.get('pierwsze', set())
        max_sprawdzone = dane.get('max_sprawdzone', 0)

        if not isinstance(pierwsze, set):
            pierwsze = set(pierwsze) if pierwsze else set()

        return pierwsze, max_sprawdzone

    except Exception as e:
        raise Exception(f"Błąd podczas wczytywania cache: {e}")


def oblicz_gestosc_w_przedziałach(pierwsze: Set[int],
                                  max_zakres: int,
                                  rozmiar_przedzialu: int = 10000) -> Tuple[List[int],
                                                                            List[float],
                                                                            List[int]]:
    """
    Oblicz gęstość liczb pierwszych w przedziałach.

    Args:
        pierwsze: Zbiór liczb pierwszych
        max_zakres: Maksymalny zakres do analizy
        rozmiar_przedzialu: Rozmiar każdego przedziału

    Returns:
        Tuple: (środki_przedziałów, gęstości, liczby_pierwszych_w_przedziałach)
    """
    przedzialy = []
    gestosci = []
    liczby_w_przedziałach = []

    # Oblicz liczbę przedziałów dla paska postępu
    liczba_przedziałów = (max_zakres - 2) // rozmiar_przedzialu + \
        (1 if (max_zakres - 2) % rozmiar_przedzialu else 0)
    aktualny_przedział = 0

    for start in range(2, max_zakres, rozmiar_przedzialu):
        aktualny_przedział += 1
        koniec = min(start + rozmiar_przedzialu, max_zakres)
        srodek = (start + koniec) / 2

        # Wyświetl postęp
        if aktualny_przedział % max(1, liczba_przedziałów //
                                    20) == 0 or aktualny_przedział == liczba_przedziałów:
            wyswietl_postep(aktualny_przedział, liczba_przedziałów, "Analiza przedziałów")

        # Policz liczby pierwsze w przedziale
        pierwsze_w_przedziale = sum(1 for p in pierwsze if start <= p < koniec)

        # Oblicz gęstość jako procent
        gestosc = (pierwsze_w_przedziale / rozmiar_przedzialu) * 100

        przedzialy.append(srodek)
        gestosci.append(gestosc)
        liczby_w_przedziałach.append(pierwsze_w_przedziale)

    # Upewnij się, że pasek postępu jest zakończony
    if liczba_przedziałów > 0:
        wyswietl_postep(liczba_przedziałów, liczba_przedziałów, "Analiza przedziałów")

    return przedzialy, gestosci, liczby_w_przedziałach


def oblicz_gestosc_teoretyczna(x_values: List[float]) -> List[float]:
    """
    Oblicz teoretyczną gęstość liczb pierwszych według twierdzenia o liczbach pierwszych.
    Gęstość ≈ 1/ln(x)
    """
    return [1.0 / math.log(x) * 100 if x > 1 else 0 for x in x_values]


def utworz_wykres_gestosci(
    przedzialy: List[int],
    gestosci: List[float],
    gestosci_teoretyczne: List[float],
    liczby_w_przedziałach: List[int],
    rozmiar_przedzialu: int,
    nazwa_pliku: str = None
):
    """Utwórz wykres gęstości liczb pierwszych."""

    print("Przygotowywanie wykresu...")
    plt.style.use('default')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Wykres gęstości (górny)
    wyswietl_postep(1, 4, "Tworzenie wykresu")
    ax1.plot(przedzialy, gestosci, 'b-', linewidth=2, label='Rzeczywista gęstość')
    ax1.plot(przedzialy, gestosci_teoretyczne, 'r--', linewidth=2,
             alpha=0.7, label='Teoretyczna gęstość (1/ln(x))')

    ax1.set_xlabel('Liczba (środek przedziału)', fontsize=12)
    ax1.set_ylabel('Gęstość liczb pierwszych (%)', fontsize=12)
    ax1.set_title(
        f'Gęstość liczb pierwszych w przedziałach po {rozmiar_przedzialu:,}',
        fontsize=14,
        fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=11)

    # Formatowanie osi X
    wyswietl_postep(2, 4, "Tworzenie wykresu")
    ax1.ticklabel_format(style='plain', axis='x')
    ax1.xaxis.set_major_formatter(
        plt.FuncFormatter(
            lambda x,
            p: f'{int(x/1000)}k' if x >= 1000 else f'{int(x)}'))

    # Wykres liczby pierwszych w przedziałach (dolny)
    wyswietl_postep(3, 4, "Tworzenie wykresu")
    ax2.bar(przedzialy, liczby_w_przedziałach, width=rozmiar_przedzialu * 0.8,
            alpha=0.7, color='skyblue', edgecolor='navy', linewidth=0.5)

    ax2.set_xlabel('Liczba (środek przedziału)', fontsize=12)
    ax2.set_ylabel('Liczba pierwszych w przedziale', fontsize=12)
    ax2.set_title(f'Liczba pierwszych w każdym przedziale', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    # Formatowanie osi X
    ax2.ticklabel_format(style='plain', axis='x')
    ax2.xaxis.set_major_formatter(
        plt.FuncFormatter(
            lambda x,
            p: f'{int(x/1000)}k' if x >= 1000 else f'{int(x)}'))

    plt.tight_layout()

    wyswietl_postep(4, 4, "Tworzenie wykresu")

    if nazwa_pliku:
        print(f"Zapisywanie wykresu do pliku: {nazwa_pliku}")
        plt.savefig(nazwa_pliku, dpi=300, bbox_inches='tight')
        print(f"Wykres zapisano jako: {nazwa_pliku}")

    return fig


def wyswietl_statystyki_gestosci(
        przedzialy: List[int],
        gestosci: List[float],
        gestosci_teoretyczne: List[float],
        liczby_w_przedziałach: List[int],
        rozmiar_przedzialu: int,
        max_sprawdzone: int):
    """Wyświetl statystyki gęstości."""

    print(f"\n=== STATYSTYKI GĘSTOŚCI LICZB PIERWSZYCH ===")
    print(f"Analizowany zakres: 2 - {max_sprawdzone:,}")
    print(f"Rozmiar przedziału: {rozmiar_przedzialu:,}")
    print(f"Liczba przedziałów: {len(przedzialy):,}")

    if gestosci:
        print(f"\nGęstość rzeczywista:")
        print(f"  Maksymalna: {max(gestosci):.3f}%")
        print(f"  Minimalna: {min(gestosci):.3f}%")
        print(f"  Średnia: {np.mean(gestosci):.3f}%")

        print(f"\nGęstość teoretyczna (1/ln(x)):")
        print(f"  Na początku zakresu: {gestosci_teoretyczne[0]:.3f}%")
        print(f"  Na końcu zakresu: {gestosci_teoretyczne[-1]:.3f}%")

        # Największy przedział z liczbami pierwszymi
        max_idx = np.argmax(liczby_w_przedziałach)
        print(f"\nNajbogatszy przedział:")
        print(f"  Środek: {przedzialy[max_idx]:,}")
        print(f"  Liczba pierwszych: {liczby_w_przedziałach[max_idx]:,}")
        print(f"  Gęstość: {gestosci[max_idx]:.3f}%")


def main():
    """Główna funkcja programu."""
    parser = argparse.ArgumentParser(
        description="Generator wykresu gęstości liczb pierwszych",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  %(prog)s                           # Standardowy wykres
  %(prog)s --przedział 5000         # Przedziały po 5000
  %(prog)s --limit 1000000          # Analiza do 1 miliona
  %(prog)s --zapisz gestosc.png     # Zapisz wykres do pliku
  %(prog)s --pokaz                  # Pokaż wykres na ekranie
        """
    )

    parser.add_argument(
        '--plik-cache',
        default=PLIK_CACHE_PIERWSZYCH,
        help=f'Plik cache z liczbami pierwszymi (domyślnie: {PLIK_CACHE_PIERWSZYCH})')
    parser.add_argument('--przedział', type=int, default=10000,
                        help='Rozmiar przedziału do analizy gęstości (domyślnie: 10000)')
    parser.add_argument('--limit', type=int,
                        help='Maksymalny zakres analizy (domyślnie: cały cache)')
    parser.add_argument('--zapisz', type=str,
                        help='Nazwa pliku do zapisu wykresu (np. gestosc.png)')
    parser.add_argument('--pokaz', action='store_true',
                        help='Pokaż wykres na ekranie')
    parser.add_argument('--bez-statystyk', action='store_true',
                        help='Pomiń wyświetlanie statystyk')

    args = parser.parse_args()

    print("=== GENERATOR WYKRESU GĘSTOŚCI LICZB PIERWSZYCH ===")

    try:
        # Wczytaj cache
        print(f"Wczytywanie cache z pliku: {args.plik_cache}")
        pierwsze, max_sprawdzone = wczytaj_cache(args.plik_cache)

        if not pierwsze:
            print("❌ Cache jest pusty - brak danych do analizy")
            return

        # Ustal zakres analizy
        max_zakres = min(args.limit, max_sprawdzone) if args.limit else max_sprawdzone

        print(f"Liczba pierwszych w cache: {len(pierwsze):,}")
        print(f"Maksymalny zakres cache: {max_sprawdzone:,}")
        print(f"Zakres analizy: 2 - {max_zakres:,}")
        print(f"Rozmiar przedziału: {args.przedział:,}")

        # Sprawdź czy zakres jest sensowny
        if max_zakres < args.przedział * 2:
            print(
                f"⚠️  Ostrzeżenie: Zakres analizy ({max_zakres:,}) jest bardzo mały w porównaniu do rozmiaru przedziału ({args.przedział:,})")

        # Oblicz gęstość w przedziałach
        print(f"\nObliczanie gęstości w przedziałach...")
        przedziały, gestosci, liczby_w_przedziałach = oblicz_gestosc_w_przedziałach(
            pierwsze, max_zakres, args.przedział
        )

        if not przedziały:
            print("❌ Brak danych do utworzenia wykresu")
            return

        # Oblicz teoretyczną gęstość
        gestosci_teoretyczne = oblicz_gestosc_teoretyczna(przedziały)

        # Wyświetl statystyki
        if not args.bez_statystyk:
            wyswietl_statystyki_gestosci(przedziały, gestosci, gestosci_teoretyczne,
                                         liczby_w_przedziałach, args.przedział, max_sprawdzone)

        # Utwórz wykres
        print(f"\nTworzenie wykresu...")
        fig = utworz_wykres_gestosci(
            przedziały, gestosci, gestosci_teoretyczne, liczby_w_przedziałach,
            args.przedział, args.zapisz
        )

        # Pokaż wykres jeśli wymagane
        if args.pokaz:
            print("Wyświetlanie wykresu... (zamknij okno aby kontynuować)")
            plt.show()
        elif not args.zapisz:
            # Domyślnie zapisz jako PNG jeśli nie podano innej opcji
            domyślna_nazwa = f"gestosc_pierwszych_{args.przedział}.png"
            fig.savefig(domyślna_nazwa, dpi=300, bbox_inches='tight')
            print(f"Wykres zapisano jako: {domyślna_nazwa}")

        print(f"\n✅ Wykres gęstości utworzony pomyślnie!")

    except FileNotFoundError as e:
        print(f"❌ {e}")
        print(f"Upewnij się, że plik cache istnieje. Możesz go utworzyć używając generuj_cache_pierwszych.py")
    except Exception as e:
        print(f"❌ Wystąpił błąd: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperacja przerwana przez użytkownika.")
    except Exception as e:
        print(f"\nNieoczekiwany błąd: {e}")
