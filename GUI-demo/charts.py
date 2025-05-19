import matplotlib.pyplot as plt

class Charts:
    def __init__(self, X, y):
        self.X = X
        self.y = y
    
    def draw_chart(X, y):
        plt.figure(figsize=(8, 5))
        plt.plot(X, y, color="green", markersize=50)
        plt.xlabel("Liczba kanałów obsługi ")
        plt.ylabel("Współczynnik blokady B(N)")
        plt.grid(True)
        plt.show()