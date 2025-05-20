


def erlang_b(A, N):
    """
    metoda do obliczania wsp. blokady w systemach ze stratami zgłoszeń opisanych modelem Erlanga
    :param A = λ * h  to natężenie ruchu w erlangach (produkt średniego strumienia zgłoszeń λ
    i średniego czasu obsługi h),
    :param N:  liczba dostępnych kanałów obsługi,
    :return: prawdopodobieństwo blokady
    """
    if N == 0:
        return 1
    else:
        # Iteracyjne obliczanie Erlang-B
        # Początkowa wartość B = 1, ponieważ dla N=1 mamy
        # jedną linię, która może być zablokowana
        B = 1.0
        for i in range(1, N + 1):
            # B(i) = (B(i-1) * A) / (B(i-1) * A + i)
            B = (B * A) / (B * A + i)
        return round(B, 3)





def erlang_N(A, B_max):
    """metoda do obliczania minimalnej liczby kanałów przy której
    zostanie zapewniona określony poziom prawdopodobieństwa blokady B(N)
    Początkowa liczba kanłów jest obliczana  w oparciu o przybliżenie natężenia ruchu A
    oraz maksymalnego prawdopodobieństwa blokady B_max.  N = ⌈A/(1-B_max)⌉
    :param A: natężenie ruchu w erlangach
    :param B_max: maksymalne dopuszczone prawdopodobieństwo blokady B(N)
    :return: minimalna liczba knałów N spełnijąca warunek"""

   # N = math.ceil(A/(1-B_max))
    N=1
    while erlang_b(A, N) > B_max:
        N += 1
    return N


def erlang_A(B_max, N):
    """Oblicza minimalne natężenie ruchu A, które odpowiada określonemu poziomowi blokady B_max
        :param B_max: maksymalne dopuszczalne prawdopodobieństwo blokady B(N)
        :param N: liczba kanałów
        :return: natężenie ruchu A, które zapewnia blokadę ≤ B_max
        """
    A=0.0
    while erlang_b(A, N) <= B_max:
        A += 0.1

    return round(A, 3)

