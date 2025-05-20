import math


import math

def engset_b(A, m, N):
    """
    Oblicza prawdopodobieństwo blokady w modelu Engseta.
    :param A: natężenie ruchu oferowanego przez jednego użytkownika (w erlangach)
    :param m: liczba użytkowników
    :param N: liczba kanałów
    :return: prawdopodobieństwo blokady
    """
    if N == 0 or m <= N:
        return 1.0  # system nie działa lub liczba użytkowników mniejsza niż liczba kanałów

    numerator = math.comb(m - 1, N) * A**N
    denominator = 0.0
    for k in range(0, N + 1):
        denominator += math.comb(m - 1, k) * A**k
    B = numerator / denominator
    return B


def engset_N(A, m, B_max):
    """
    Oblicza minimalną liczbę kanałów potrzebną do uzyskania poziomu blokady ≤ B_max.
    :param A: natężenie ruchu od jednego użytkownika
    :param m: liczba użytkowników
    :param B_max: maksymalne dopuszczalne prawdopodobieństwo blokady
    :return: minimalna liczba kanałów
    """
    N = 1
    while N < m and engset_b(A, m, N) > B_max:
        N += 1
    return N if N < m else None  # jeśli nie da się osiągnąć poziomu, zwraca None


def engset_A(m, N, B_max):
    """
    Oblicza maksymalne A (natężenie od jednego użytkownika), które zapewnia blokadę ≤ B_max.
    :param m: liczba użytkowników
    :param N: liczba kanałów
    :param B_max: maksymalne dopuszczalne prawdopodobieństwo blokady
    :return: natężenie A
    """
    A = 0.0
    while engset_b(A, m, N) <= B_max:
        A += 0.01
        if A > 100:  # zabezpieczenie przed nieskończoną pętlą
            return None
    return round(A - 0.01, 3)

