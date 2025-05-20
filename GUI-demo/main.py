import sys

import erlang
import Engset
import charts

import matplotlib.pyplot as plt
from PyQt5.QtGui import QTransform
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QFont, QColor, QFontDatabase, QPixmap, QRegularExpressionValidator
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGraphicsDropShadowEffect, QPushButton, QLineEdit, \
    QRadioButton, QButtonGroup, QVBoxLayout, QTextEdit


def create_shadow():
    """ Tworzy efekt cienia """
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(0)
    shadow.setXOffset(3)
    shadow.setYOffset(3)
    shadow.setColor(QColor("#ff8fab"))
    return shadow

def draw_chart(X, y, keyX, keyY, X_2, Y_2):
    '''Generuje wykres
    :param X: argumenty
    :param Y: wartości
    :param keyX: nazwa osi X
    :param keyY: nazwa osi Y
    :param X_2: wspł. X punktu
    :param Y_2: wspł. Y punktu'''

    plt.figure(figsize=(8, 5))
    plt.plot(X, y, color="#ff8fab", markersize=50)
    plt.plot(X_2, Y_2,'o',color='#ff8fab',label=f'Punkt{X_2, Y_2}')
    plt.legend()
    plt.autoscale()
    plt.xlabel(keyX)
    plt.ylabel(keyY)
    plt.grid(True)
    plt.show()

class ResultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historia wyników")
        self.setGeometry(1480, 190, 400, 700)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("background-color: #fefefe; font-size: 14px;")
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

    def add_entry(self, description, value):
        if isinstance(value, float):
            value = round(value, 4)
        self.text_edit.append(f"<b>{description}:</b> {value}")



class MainWindow(QWidget):



    def __init__(self):
        super().__init__()
        self.text_input = None
        self.buttonStyle = None
        self.initUI()

    def initUI(self):
        self.windowHeight = 700
        self.windowWidth = 1000



        self.setFixedSize(self.windowWidth, self.windowHeight)
        self.setWindowTitle("Erlang Calculator")
        self.setStyleSheet("background: #ffe5ec;")

        # Styl przycisków
        self.buttonStyle = """
                         QPushButton {
                             background-color: #ffb3c6;
                             color: black;
                             border: none;
                             border-radius: 10px;
                             padding: 15px 32px;
                             font-size: 24px;
                         }
                         QPushButton:hover {
                             background-color: #ff8fab;
                         }
                         QPushButton:pressed {
                             background-color: #fb6f92;
                         }
                     """

        self.text_input = """
                   QLineEdit {
                       border: 2px solid #fb6f92;
                       border-radius: 10px;
                       padding: 8px;
                       background-color: #ffe5ec;
                       selection-background-color: #f4acb7;
                       font-size: 14px;
                   }
                   QLineEdit:focus {
                       border: 2px solid #fb6f92;
                       background-color: #f4acb7;
                   }
                   QLineEdit:disabled {
                        border: 2px solid #ffe5ec;
                        color: #ffe5ec; /* Kolor tekstu dla zablokowanego pola */
                   }
               """
        # Styl dla napisów
        self.labelTextStyle = """
                          QLabel {
                              color: black;
                              font-size: 24px;
                              background: transparent;
                          }
                      """
        # Ładowanie czcionki
        font_id = QFontDatabase.addApplicationFont("BebasNeue-Regular.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font = QFont(font_family, 36)
        self.fontSmall = QFont(font_family, 45)



        # Główne layouty (widoki)
        self.main_view = QWidget(self)
        self.info_view = QWidget(self)
        self.calculator_view = QWidget(self)
        self.info_erlang_view = QWidget(self)
        self.info_enset_view = QWidget(self)
        self.cal_erlang_view = QWidget(self)
        self.cal_enset_view = QWidget(self)


        # Ustawienia stylu i rozmiaru dla widoków
        for view in [self.main_view, self.info_view, self.calculator_view, self.info_erlang_view,
                     self.info_enset_view, self.cal_erlang_view, self.cal_enset_view]:
            view.setFixedSize(self.windowWidth, self.windowHeight)
            view.setStyleSheet("background: #ffe5ec;")

            # Inicjalizacja widoków
        self.setup_main_view()
        self.setup_info_view()
        self.setup_calculator_view()
        self.setup_info_erlang_view()
        self.setup_info_enset_view()
        self.setup_cal_erlang_view()
        self.setup_cal_enset_view()

        # Pokaż widok główny
        self.show_main_view()
        self.info_view.hide()
        self.calculator_view.hide()
        self.info_erlang_view.hide()
        self.info_enset_view.hide()
        self.cal_erlang_view.hide()
        self.cal_enset_view.hide()

    def setup_main_view(self):
        """ Tworzy główny widok z przyciskami """
        self.main_view.setStyleSheet("background: #ffe5ec;")
        label = QLabel("Witaj w kalkulatorze Erlanga i Engseta", self.main_view)
        label.setFont(self.font)
        label.setStyleSheet("color: black; background: transparent;")
        label.setGraphicsEffect(create_shadow())

        font = label.font()
        font.setBold(True)
        font.setWeight(QFont.ExtraLight)
        label.setFont(QFont("Trebuchet MS", 25))


        # Napis na środku
        label.setGeometry(0, 50, self.windowWidth, 100)
        label.setAlignment(Qt.AlignCenter)




        # Przycisk „Informacje”
        buttonInfo = QPushButton("Informacje", self.main_view)
        buttonInfo.setFont(self.fontSmall)
        buttonInfo.setStyleSheet(self.buttonStyle)
        buttonInfo.resize(300, 200)
        buttonInfo.move(80, 220)
        buttonInfo.setGraphicsEffect(create_shadow())
        buttonInfo.clicked.connect(self.show_info_view)

        # Przycisk „Kalkulator”
        buttonCal = QPushButton("Kalkulator", self.main_view)
        buttonCal.setFont(self.fontSmall)
        buttonCal.setStyleSheet(self.buttonStyle)
        buttonCal.resize(300, 200)
        buttonCal.move(600, 450)
        buttonCal.setGraphicsEffect(create_shadow())
        buttonCal.clicked.connect(self.show_calculator_view)

        # Strzałka w lewo
        '''arrowLeft = QLabel(self.main_view)
        arrow_pixmap = QPixmap("icons8-arrow-64.png")  # Załaduj obrazek strzałki
        arrowLeft.setPixmap(arrow_pixmap)
        arrowLeft.move(450, 270)  # Pozycja strzałki

        # Strzałka w prawo
        arrowRight = QLabel(self.main_view)
        arrow_pixmap = QPixmap("icons8-arrow-right.png")  # Załaduj obrazek strzałki
        arrowRight.setPixmap(arrow_pixmap)
        arrowRight.move(450, 500) '''
        arrowPixmap = QPixmap("icons8-arrow-64.png")
        arrowLeft = QLabel(self.main_view)
        arrowRight = QLabel(self.main_view)

        # przypisz pixmapę do obu widgetów
        arrowLeft .setPixmap(arrowPixmap)
        arrowRight.setPixmap(arrowPixmap)

        # wyliczasz pozycje…
        x  = (self.windowWidth - arrowPixmap.width()) // 2
        y1 = 265
        spacing = 170
        y2 = y1 + arrowPixmap.height() + spacing

        # i przesuwasz
        arrowLeft .move(x, y1)
        arrowRight.move(x, y2)

        t = QTransform().scale(-1, 1)   # skala -1 w poziomie, 1 w pionie
        flipped2 = arrowPixmap.transformed(t)
        arrowRight.setPixmap(flipped2)




        # Tekst obok strzałki lewej
        labelLeft = QLabel("Kliknij mnie by dowiedzieć się więcej na temat", self.main_view)
        labelLeft.setFont(self.fontSmall)
        labelLeft.setStyleSheet(self.labelTextStyle)
        labelLeft.move(550, 285)

        # Tekst obok strzałki prawej
        labelRight = QLabel("Kliknij mnie by przejść do kalkulatora", self.main_view)
        labelRight.setFont(self.fontSmall)
        labelRight.setStyleSheet(self.labelTextStyle)
        labelRight.move(140, 520)

    def setup_calculator_view(self):
        """ Tworzy widok kalkulatora """


        label = QLabel("Chcę użyć kalkulatora...", self.calculator_view)
        label.setFont(self.font)
        label.move(50, 100)
        label.setStyleSheet("color: black; background: transparent;")
        label.setGraphicsEffect(create_shadow())

        # Przycisk powrót
        buttonBack = QPushButton("↩ Powrót", self.calculator_view)
        buttonBack.setFont(self.fontSmall)
        buttonBack.setStyleSheet(self.buttonStyle)
        buttonBack.move(680, 500)
        buttonBack.setGraphicsEffect(create_shadow())
        buttonBack.clicked.connect(self.show_main_view)

        # Przycisk Erlang
        buttonErlang = QPushButton("Erlanga", self.calculator_view)
        buttonErlang.setFont(self.fontSmall)
        buttonErlang.setStyleSheet(self.buttonStyle)
        buttonErlang.move(600, 200)
        buttonErlang.resize(300, 100)
        buttonErlang.setGraphicsEffect(create_shadow())
        buttonErlang.clicked.connect(self.show_cal_erlang_view)

        # Przycisk Engset
        buttonEngset = QPushButton("Engseta", self.calculator_view)
        buttonEngset.setFont(self.fontSmall)
        buttonEngset.setStyleSheet(self.buttonStyle)
        buttonEngset.move(600, 350)
        buttonEngset.resize(300, 100)
        buttonEngset.setGraphicsEffect(create_shadow())
        buttonEngset.clicked.connect(self.show_cal_enset_view)

        # Obrazek
        broCantMath = QLabel(self.calculator_view)
        broCantMathPixmap = QPixmap("Calculator-amico.png").scaled(400, 400)  # Załaduj obrazek
        broCantMath.setPixmap(broCantMathPixmap)
        broCantMath.move(50, 200)  # Pozycja

    def setup_info_view(self):
        """ Tworzy widok informacji """


        label = QLabel("Chce się dowiedziec więcej na temat...", self.info_view)
        label.setFont(self.font)
        label.move(50, 100)
        label.setStyleSheet("color: black; background: transparent;")
        label.setGraphicsEffect(create_shadow())

        #Przycisk Erlang
        buttonErlang = QPushButton("Erlanga", self.info_view)
        buttonErlang.setFont(self.fontSmall)
        buttonErlang.setStyleSheet(self.buttonStyle)
        buttonErlang.move(600, 200)
        buttonErlang.resize(300, 100)
        buttonErlang.setGraphicsEffect(create_shadow())
        buttonErlang.clicked.connect(self.show_info_erlang_view)

        #Przycisk Engset
        buttonEngset = QPushButton("Engseta", self.info_view)
        buttonEngset.setFont(self.fontSmall)
        buttonEngset.setStyleSheet(self.buttonStyle)
        buttonEngset.move(600, 350)
        buttonEngset.resize(300, 100)
        buttonEngset.setGraphicsEffect(create_shadow())
        buttonEngset.clicked.connect(self.show_info_enset_view)

        #Przycisk powrót
        buttonBack = QPushButton("↩ Powrót", self.info_view)
        buttonBack.setFont(self.fontSmall)
        buttonBack.setStyleSheet(self.buttonStyle)
        buttonBack.move(680, 500)
        buttonBack.setGraphicsEffect(create_shadow())
        buttonBack.clicked.connect(self.show_main_view)

        # Obrazek
        broCantThink = QLabel(self.info_view)
        broCantThinkPixmap = QPixmap("Questions-bro.png").scaled(400, 400)  # Załaduj obrazek
        broCantThink.setPixmap(broCantThinkPixmap)
        broCantThink.move(50, 200)  # Pozycja

    def setup_info_erlang_view(self):

        # Tekst teoretyczny
        theory_text = (
        "<div style='text-align: justify;'>"
        "<b>Do czego służy Teoria Erlanga?</b><br>"
        "Teoria Erlanga jest stosowana głównie w analizie systemów kolejkowych i telekomunikacji do oceny, jak skutecznie można obsługiwać wiele żądań (np. połączeń telefonicznych, klientów, pakietów danych) przy ograniczonych zasobach (kanałach, serwerach, liniach). Pozwala obliczyć prawdopodobieństwo blokady połączenia lub czas oczekiwania w kolejce.<br><br>"
        "</div>"
        "<b>Wzór Erlanga (B):</b><br>"
        "Wzór Erlanga (B) oblicza prawdopodobieństwo blokady prób połączeń w systemie z N kanałami i natężeniem ruchu A.<br><br>"
        "<b>Wzór Erlanga (A):</b><br>"
        "Wzór Erlanga A służy do obliczania prawdopodobieństwa oczekiwania w systemach kolejkowych z możliwością rezygnacji przez klientów (model z porzucaniem).<br><br>"
        "<b>Wzór Erlanga (N):</b><br>"
        "Wzór Erlanga N służy do wyznaczenia minimalnej liczby zasobów (np. kanałów, agentów), aby spełnić zadane warunki jakości obsługi przy danym natężeniu ruchu.<br><br>"
        "<b>Parametry:</b><br>"
        "A - natężenie ruchu w Erlangach (suma czasów trwania połączeń w jednostce czasu)<br>"
        "N - liczba dostępnych kanałów obsługi<br>"
        "B - docelowe prawdopodobieństwo blokady (wynik wzoru)<br><br>"
        "<b>Przykłady zastosowania:</b><br>" \
        " -> Określenie liczby kanałów w centrali telefonicznej, aby spełnić określone SLA (np. 99% połączeń bez blokady).<br>"
        " -> Wyznaczanie liczby konsultantów potrzebnych w danej godzinie szczytu.<br>"
        " -> Modelowanie obciążenia serwerów i zapotrzebowania na wątki/instancje aplikacji.<br>"
        " -> Zarządzanie przepustowością w systemach transportowych, np. liczba bramek na autostradach.<br>"
        )

        text_widget = QTextEdit(self.info_erlang_view)
        text_widget.setReadOnly(True)
        text_widget.setHtml(theory_text)
        text_widget.setStyleSheet("background: #FFFFFF; font-size: 16px;")
        text_widget.setGeometry(50, 210, 800, 300)
        font1 = QFont("Segoe UI", 11)
        text_widget.setFont(font1)
        shadow = create_shadow()
        text_widget.setGraphicsEffect(shadow)
        text_widget.setStyleSheet("""
        QTextEdit {
            background-color: #f9f9f9;
            color: #333333;
            font-size: 16px;
            padding: 15px;
            border: 1px solid #cccccc;
            border-radius: 10px;
        }
            """)


        label = QLabel("Teoria Erlanga", self.info_erlang_view)
        label.setFont(self.font)
        label.move(50, 80)
        label.setStyleSheet("color: black; background: transparent;")
        label.setGraphicsEffect(create_shadow())

        # Przycisk powrotu do ekranu Informacje
        buttonBack = QPushButton("↩ Powrót", self.info_erlang_view)
        buttonBack.setFont(self.fontSmall)
        buttonBack.setStyleSheet(self.buttonStyle)
        buttonBack.move(680, 550)
        buttonBack.setGraphicsEffect(create_shadow())
        buttonBack.clicked.connect(self.show_info_view) 



    def setup_info_enset_view(self):

        """Tworzy widok Engseta - teoria"""
        self.info_enset_view.setStyleSheet("background: #ffe5ec;")
        # Tytuł
        title = QLabel("Teoria Engseta", self.info_enset_view)
        title.setFont(self.font)
        title.move(50, 80)
        title.setStyleSheet("color: black; background: transparent;")
        title.setGraphicsEffect(create_shadow())

        # Tekst teoretyczny
        theory_text = (
            "<div style='text-align: justify;'>"
            "<b>Do czego służy Teoria Engseta?</b><br>"
            "Teoria Engseta jest stosowana w analizie systemów kolejkowych z ograniczoną liczbą użytkowników i zasobów, gdzie każdy użytkownik może generować żądania tylko wtedy, gdy nie jest już obsługiwany. Jest przydatna szczególnie tam, gdzie liczba źródeł żądań jest niewielka i skończona (np. w sieciach lokalnych lub systemach wojskowych).<br><br>"
            "</div>"
            "<b>Wzór Engseta:</b><br>"
            "Wzór Engseta oblicza prawdopodobieństwo blokady żądania w systemie z ograniczoną liczbą użytkowników oraz ograniczoną liczbą kanałów obsługi, przy założeniu, że nieobsłużone żądania nie trafiają do kolejki, ale są odrzucane.<br><br>"
            "<b>Założenia modelu Engseta:</b><br>"
            " - Liczba źródeł żądań (np. użytkowników) jest skończona.<br>"
            " - Nieobsłużone żądania są odrzucane (brak kolejki).<br>"
            " - Każde źródło może wygenerować nowe żądanie tylko wtedy, gdy nie jest już zajęte.<br><br>"
            "<b>Parametry:</b><br>"
            "N - liczba źródeł żądań (np. użytkowników)<br>"
            "m - liczba dostępnych kanałów obsługi<br>"
            "A - efektywne natężenie ruchu (zależne od liczby dostępnych użytkowników)<br>"
            "B - prawdopodobieństwo blokady (wynik wzoru)<br><br>"
            "<b>Przykłady zastosowania:</b><br>"
            " -> Analiza systemów łączności wojskowej z ograniczoną liczbą terminali.<br>"
            " -> Planowanie sieci lokalnych (LAN) z małą liczbą stacji roboczych.<br>"
            " -> Symulacje w systemach sterowania przemysłowego z ograniczoną liczbą punktów żądań.<br>"
            " -> Modelowanie małych systemów komunikacyjnych, np. wewnętrznych sieci radiowych."
        )

        text_widget = QTextEdit(self.info_enset_view)
        text_widget.setReadOnly(True)
        text_widget.setHtml(theory_text)
        text_widget.setStyleSheet("background: transparent; font-size: 16px;")
        text_widget.setGeometry(50, 210, 800, 300)
        font2 = QFont("Segoe UI", 11)
        text_widget.setFont(font2)
        shadow = create_shadow()
        text_widget.setGraphicsEffect(shadow)
        text_widget.setStyleSheet("""
        QTextEdit {
            background-color: #f9f9f9;
            color: #333333;
            font-size: 16px;
            padding: 15px;
            border: 1px solid #cccccc;
            border-radius: 10px;
        }
            """)

        # Przycisk powrotu do ekranu Informacje
        buttonBack = QPushButton("↩ Powrót", self.info_enset_view)
        buttonBack.setFont(self.fontSmall)
        buttonBack.setStyleSheet(self.buttonStyle)
        buttonBack.move(680, 550)
        buttonBack.setGraphicsEffect(create_shadow())
        buttonBack.clicked.connect(self.show_info_view) 
        



    def setup_cal_erlang_view(self):
        """ Tworzy widok Erlanga """
        label = QLabel("Kalkulator Erlanga", self.cal_erlang_view)
        label.setFont(self.font)
        label.move(50, 60)
        label.setStyleSheet("color: black; background: transparent;")
        label.setGraphicsEffect(create_shadow())

        # Ustawienie walidatora (tylko cyfry i -)
        regex = QRegularExpression(r"^\d+[-]?\d*$")
        validator = QRegularExpressionValidator(regex)

        # Ustawienie walidatora (tylko cyfry i -)
        regex2 = QRegularExpression(r"^(0(\.\d+)?|1(\.0*)?)$")
        validatorDot = QRegularExpressionValidator(regex2)

        labelA = QLabel("A - natężenie ruchu w erlangach", self.cal_erlang_view)
        labelA.setFont(self.fontSmall)
        labelA.setStyleSheet(self.labelTextStyle)
        labelA.move(50, 180)

        # Pole tekstowe A
        self.AInputEL = QLineEdit(self.cal_erlang_view)
        self.AInputEL.setStyleSheet(self.text_input)
        self.AInputEL.setPlaceholderText("np. 420 lub 21-37 (Liczby muszą byc pomiedzy 0.1 a 180)")
        self.AInputEL.move(50, 210)
        self.AInputEL.resize(400, 50)
        self.AInputEL.setValidator(validator)

        labelB = QLabel("B - maksymalne dopuszczalne prawdopodobieństwo blokady", self.cal_erlang_view)
        labelB.setFont(self.fontSmall)
        labelB.setStyleSheet(self.labelTextStyle)
        labelB.move(50, 320)

        # Pole tekstowe
        self.BInputEL = QLineEdit(self.cal_erlang_view)
        self.BInputEL.setStyleSheet(self.text_input)
        self.BInputEL.setPlaceholderText("np. 0.03 (Liczba musi byc pomiedzy 0.001 a 0.999)")
        self.BInputEL.move(50, 350)
        self.BInputEL.resize(400, 50)
        self.BInputEL.setValidator(validatorDot)

        labelN = QLabel("N - liczba dostępnych kanałów obsługi", self.cal_erlang_view)
        labelN.setFont(self.fontSmall)
        labelN.setStyleSheet(self.labelTextStyle)
        labelN.move(50, 450)

        # Pole tekstowe
        self.NInputEL = QLineEdit(self.cal_erlang_view)
        self.NInputEL.setStyleSheet(self.text_input)
        self.NInputEL.setPlaceholderText("np. 420 lub 21-37 (Liczby muszą byc pomiedzy 1 a 180)")
        self.NInputEL.move(50, 480)
        self.NInputEL.resize(400, 50)
        self.NInputEL.setValidator(validator)

        labelChoice = QLabel("Chce obliczyć: (wybierz opcje)", self.cal_erlang_view)
        labelChoice.setFont(self.fontSmall)
        labelChoice.setStyleSheet(self.labelTextStyle)
        labelChoice.move(600, 100)

        # Stylizacja przycisków
        buttonStyle = """
                   QRadioButton::indicator {
                       width: 20px;
                       height: 20px;
                   }
                   QRadioButton::indicator::unchecked {
                       image: url(heart_empty.png); 
                   }
                   QRadioButton::indicator::checked {
                       image: url(heart_filled.png); 
                   }
                    QRadioButton {
                        color: black; 
                    }
                    QRadioButton:checked {
                        color: #ff8fab;
                    }
        """

        button_group = QButtonGroup(self.cal_erlang_view)

        self.option1_AEL = QRadioButton("A - natężenie ruchu w erlangach", self.cal_erlang_view)
        self.option2_BEL = QRadioButton("B - maksymalne dopuszczalne prawdopodobieństwo blokady", self.cal_erlang_view)
        self.option3_NEL = QRadioButton("N - liczba dostępnych kanałów obsługi", self.cal_erlang_view)

        self.option3_NEL.setStyleSheet(buttonStyle)
        self.option1_AEL.setStyleSheet(buttonStyle)
        self.option2_BEL.setStyleSheet(buttonStyle)

        button_group.addButton(self.option1_AEL)
        button_group.addButton(self.option2_BEL)
        button_group.addButton(self.option3_NEL)

        self.option1_AEL.move(600, 150)
        self.option2_BEL.move(600, 200)
        self.option3_NEL.move(600, 250)

        self.option1_AEL.toggled.connect(self.handle_radio_button_change1)
        self.option2_BEL.toggled.connect(self.handle_radio_button_change1)
        self.option3_NEL.toggled.connect(self.handle_radio_button_change1)

        labelChoicePlots = QLabel(
            "Czy ma zostać utworzony wykres? Jeśli tak, określ jeden z parametrów jako zakres wartości",
            self.cal_erlang_view)
        labelChoicePlots.setFont(self.fontSmall)
        labelChoicePlots.setStyleSheet(self.labelTextStyle)
        labelChoicePlots.setWordWrap(True)
        labelChoicePlots.move(600, 300)

        self.plotParamB = QPushButton("B", self.cal_erlang_view)
        self.plotParamB.setFont(self.fontSmall)
        self.plotParamB.setStyleSheet(self.buttonStyle)
        self.plotParamB.move(650, 390)
        self.plotParamB.setFixedSize(80, 50)
        self.plotParamB.hide()  # domyślnie niewidoczny
        
        self.plotParamN = QPushButton("N", self.cal_erlang_view)
        self.plotParamN.setFont(self.fontSmall)
        self.plotParamN.setStyleSheet(self.buttonStyle)
        self.plotParamN.move(780, 390)
        self.plotParamN.setFixedSize(80, 50)
        self.plotParamN.hide()  # domyślnie niewidoczny

        # nowy przycisk „A” dla opcji 2
        self.plotParamA = QPushButton("A", self.cal_erlang_view)
        self.plotParamA.setFont(self.fontSmall)
        self.plotParamA.setStyleSheet(self.buttonStyle)
        self.plotParamA.setFixedSize(80, 50)
        self.plotParamA.move(650, 390)  # na tej samej pozycji co B
        self.plotParamA.hide()

        # 1) Ustawiamy je jako checkable
        for btn in (self.plotParamA, self.plotParamB, self.plotParamN):
            btn.setCheckable(True)

        # 2) Tworzymy grupę, żeby tylko jeden mógł być wciśnięty (opcjonalnie)
        self.plotParamGroup = QButtonGroup(self.cal_erlang_view)
        self.plotParamGroup.setExclusive(True)
        self.plotParamGroup.addButton(self.plotParamA)
        self.plotParamGroup.addButton(self.plotParamB)
        self.plotParamGroup.addButton(self.plotParamN)

        # 3) Nowy style-sheet dla tej trójki przycisków:
        toggle_style = """
        QPushButton {
            background-color: #ffb3c6;
            color: black;
            border: 2px solid #fb6f92;
            border-radius: 5px;
            padding: 4px 8px;
            font-size: 18px;
        }
        QPushButton:hover {
            background-color: #ff8fab;
        }
        QPushButton:checked {
            background-color: #fb6f92;   /* to będzie „podświetlenie” */
        }
        """
        for btn in (self.plotParamA, self.plotParamB, self.plotParamN):
            btn.setStyleSheet(toggle_style)


        # Przycisk Erlanga
        buttonEngset = QPushButton("Teoria Erlanga", self.cal_erlang_view)
        buttonEngset.setFont(self.fontSmall)
        buttonEngset.setStyleSheet(self.buttonStyle)
        buttonEngset.move(600, 450)
        buttonEngset.resize(300, 100)
        buttonEngset.setGraphicsEffect(create_shadow())
        buttonEngset.clicked.connect(self.show_info_erlang_view)

        # Przycisk powrót
        buttonBack = QPushButton("↩ Powrót", self.cal_erlang_view)
        buttonBack.setFont(self.fontSmall)
        buttonBack.setStyleSheet(self.buttonStyle)
        buttonBack.move(680, 600)
        buttonBack.setGraphicsEffect(create_shadow())
        buttonBack.clicked.connect(self.show_calculator_view)

        buttonCal = QPushButton("Oblicz", self.cal_erlang_view)
        buttonCal.setFont(self.fontSmall)
        buttonCal.setStyleSheet(self.buttonStyle)
        buttonCal.move(50, 570)
        buttonCal.resize(500, 100)
        buttonCal.setGraphicsEffect(create_shadow())
        buttonCal.clicked.connect(self.erlang_chooser)

        self.result_window = ResultWindow()
        self.result_window.show()

    def handle_radio_button_change1(self):

        self.plotParamA.hide()
        self.plotParamB.hide()
        self.plotParamN.hide()

        # Resetuj wszystkie pola
        self.AInputEL.setEnabled(True)
        self.AInputEL.setPlaceholderText("np. 420 lub 21-37 (Liczby muszą byc pomiedzy 0.1 a 180)")
        self.BInputEL.setEnabled(True)
        self.BInputEL.setPlaceholderText("np. 0.03 (Liczba musi byc pomiedzy 0.001 a 0.999)")
        self.NInputEL.setEnabled(True)
        self.NInputEL.setPlaceholderText("np. 420 lub 21-37 (Liczby całkowite muszą byc pomiedzy 1 a 180)")

        # Wyłącz odpowiednie pole na podstawie wyboru
        if self.option1_AEL.isChecked():
            self.AInputEL.setEnabled(False)
            self.AInputEL.setPlaceholderText("")
        elif self.option2_BEL.isChecked():
            self.BInputEL.setEnabled(False)
            self.BInputEL.setPlaceholderText("")
        elif self.option3_NEL.isChecked():
            self.NInputEL.setEnabled(False)
            self.NInputEL.setPlaceholderText("")

        # Resetuj pola (jak masz już)
        self.AInputEL.setEnabled(True)
        self.BInputEL.setEnabled(True)
        self.NInputEL.setEnabled(True)

        # Załóżmy, że ukrywasz/wyłączasz odpowiednie inputy
        if self.option1_AEL.isChecked():
            # obliczamy A → mamy B i N, więc pokazujemy guziki „B” i „N”
            self.AInputEL.setEnabled(False)
            self.plotParamB.show()
            self.plotParamB.move(650, 390)
            self.plotParamN.show()

        elif self.option2_BEL.isChecked():
            # obliczamy B → mamy A i N, więc pokazujemy guziki „A” i „N”
            self.BInputEL.setEnabled(False)
            self.plotParamA.show()
            self.plotParamN.show()

        elif self.option3_NEL.isChecked():
            # obliczamy N → mamy A i B, więc pokazujemy guziki „A” i „B”
            self.NInputEL.setEnabled(False)
            self.plotParamA.show()
            self.plotParamB.move(780, 390)
            self.plotParamB.show()

            if self.option2_BEL.isChecked():
                self.BInputEL.setEnabled(False)
            if self.option3_NEL.isChecked():
                self.NInputEL.setEnabled(False)

    def setup_cal_enset_view(self):
        """ Tworzy widok Engseta """
        label = QLabel("Kalkulator Engseta", self.cal_enset_view)
        label.setFont(self.font)
        label.move(50, 60)
        label.setStyleSheet("color: black; background: transparent;")
        label.setGraphicsEffect(create_shadow())

        self.plotParamB_E = QPushButton("B", self.cal_erlang_view)
        self.plotParamB_E.setFont(self.fontSmall)
        self.plotParamB_E.setStyleSheet(self.buttonStyle)
        self.plotParamB_E.move(650, 390)
        self.plotParamB_E.setFixedSize(80, 50)
        self.plotParamB_E.hide()  # domyślnie niewidoczny
        
        self.plotParamN_E = QPushButton("N", self.cal_erlang_view)
        self.plotParamN_E.setFont(self.fontSmall)
        self.plotParamN_E.setStyleSheet(self.buttonStyle)
        self.plotParamN_E.move(780, 390)
        self.plotParamN_E.setFixedSize(80, 50)
        self.plotParamN_E.hide()  # domyślnie niewidoczny

        # nowy przycisk „A” dla opcji 2
        self.plotParamA_E = QPushButton("A", self.cal_erlang_view)
        self.plotParamA_E.setFont(self.fontSmall)
        self.plotParamA_E.setStyleSheet(self.buttonStyle)
        self.plotParamA_E.setFixedSize(80, 50)
        self.plotParamA_E.move(650, 390)  # na tej samej pozycji co B
        self.plotParamA_E.hide()

        # 1) Ustawiamy je jako checkable
        for btn in (self.plotParamA_E, self.plotParamB_E, self.plotParamN_E):
            btn.setCheckable(True)

        # 2) Tworzymy grupę, żeby tylko jeden mógł być wciśnięty (opcjonalnie)
        self.plotParamGroup = QButtonGroup(self.cal_erlang_view)
        self.plotParamGroup.setExclusive(True)
        self.plotParamGroup.addButton(self.plotParamA_E)
        self.plotParamGroup.addButton(self.plotParamB_E)
        self.plotParamGroup.addButton(self.plotParamN_E)

        # 3) Nowy style-sheet dla tej trójki przycisków:
        toggle_style = """
        QPushButton {
            background-color: #ffb3c6;
            color: black;
            border: 2px solid #fb6f92;
            border-radius: 5px;
            padding: 4px 8px;
            font-size: 18px;
        }
        QPushButton:hover {
            background-color: #ff8fab;
        }
        QPushButton:checked {
            background-color: #fb6f92;   /* to będzie „podświetlenie” */
        }
        """
        for btn in (self.plotParamA_E, self.plotParamB_E, self.plotParamN_E):
            btn.setStyleSheet(toggle_style)

        # Ustawienie walidatora (tylko cyfry i _)
        regex = QRegularExpression(r"^\d+[-]?\d*$")
        validator = QRegularExpressionValidator(regex)

        # Ustawienie walidatora (tylko cyfry i _)
        regex2 = QRegularExpression(r"^(0(\.\d+)?|1(\.0*)?)$")
        validatorDot = QRegularExpressionValidator(regex2)

        labelA = QLabel("A - natężenie ruchu w erlangach", self.cal_enset_view)
        labelA.setFont(self.fontSmall)
        labelA.setStyleSheet(self.labelTextStyle)
        labelA.move(50, 180)

        # Pole tekstowe A
        self.AInput = QLineEdit(self.cal_enset_view)
        self.AInput.setStyleSheet(self.text_input)
        self.AInput.setPlaceholderText("np. 420 lub 21-37 (Liczby muszą byc pomiedzy 0.1 a 100)")
        self.AInput.move(50, 210)
        self.AInput.resize(400, 50)
        self.AInput.setValidator(validator)

        labelB = QLabel("B - maksymalne dopuszczalne prawdopodobieństwo blokady", self.cal_enset_view)
        labelB.setFont(self.fontSmall)
        labelB.setStyleSheet(self.labelTextStyle)
        labelB.move(50, 270)

        # Pole tekstowe
        self.BInput = QLineEdit(self.cal_enset_view)
        self.BInput.setStyleSheet(self.text_input)
        self.BInput.setPlaceholderText("np. 0.03 (Liczba musi byc pomiedzy 0.001 a 0.499)")
        self.BInput.move(50, 300)
        self.BInput.resize(400, 50)
        self.BInput.setValidator(validatorDot)



        labelN = QLabel("N - liczba dostępnych kanałów obsługi", self.cal_enset_view)
        labelN.move(50, 360)
        labelN.setFont(self.fontSmall)
        labelN.setStyleSheet(self.labelTextStyle)
        

        # Pole tekstowe
        self.NInput = QLineEdit(self.cal_enset_view)
        self.NInput.move(50, 387)
        self.NInput.setStyleSheet(self.text_input)
        self.NInput.setPlaceholderText("np. 420 lub 21-37 (Liczby muszą byc pomiedzy 1 a 100)")
        
        self.NInput.resize(400, 50)
        self.NInput.setValidator(validator)

        labelN = QLabel("a -  liczba użytkowników", self.cal_enset_view)
        labelN.setFont(self.fontSmall)
        labelN.setStyleSheet(self.labelTextStyle)
        labelN.move(50, 450)

        # Pole tekstowe - Number of traffic sources
        self.numInput = QLineEdit(self.cal_enset_view)
        self.numInput.setStyleSheet(self.text_input)
        self.numInput.setPlaceholderText("np. 420 lub 21-37 (Liczby muszą byc pomiedzy 10 a 2000)")
        self.numInput.move(50, 480)
        self.numInput.resize(400, 50)
        self.numInput.setValidator(validator)

        labelChoice = QLabel("Chce obliczyć: (wybierz opcje)", self.cal_enset_view)
        labelChoice.setFont(self.fontSmall)
        labelChoice.setStyleSheet(self.labelTextStyle)
        labelChoice.move(600, 100)

        # Stylizacja przycisków
        buttonStyle = """
                          QRadioButton::indicator {
                              width: 20px;
                              height: 20px;
                          }
                          QRadioButton::indicator::unchecked {
                              image: url(heart_empty.png); 
                          }
                          QRadioButton::indicator::checked {
                              image: url(heart_filled.png); 
                          }
                           QRadioButton {
                               color: black; 
                           }
                           QRadioButton:checked {
                               color: #ff8fab;
                           }
               """

        button_group = QButtonGroup(self.cal_enset_view)

        self.option1_A = QRadioButton("A - natężenie ruchu w erlangach", self.cal_enset_view)
        self.option2_B = QRadioButton("B - maksymalne dopuszczalne prawdopodobieństwo blokady", self.cal_enset_view)
        self.option3_N = QRadioButton("N - liczba dostępnych kanałów obsługi", self.cal_enset_view)

        self.option3_N.setStyleSheet(buttonStyle)
        self.option1_A.setStyleSheet(buttonStyle)
        self.option2_B.setStyleSheet(buttonStyle)

        button_group.addButton(self.option1_A)
        button_group.addButton(self.option2_B)
        button_group.addButton(self.option3_N)

        self.option1_A.move(600, 150)
        self.option2_B.move(600, 200)
        self.option3_N.move(600, 250)

        self.option1_A.toggled.connect(self.handle_radio_button_change)
        self.option2_B.toggled.connect(self.handle_radio_button_change)
        self.option3_N.toggled.connect(self.handle_radio_button_change)

        labelChoicePlots = QLabel(
            "Czy ma zostać utworzony wykres? Jeśli tak, określ jeden z parametrów jako zakres wartości",
            self.cal_enset_view)
        labelChoicePlots.setFont(self.fontSmall)
        labelChoicePlots.setStyleSheet(self.labelTextStyle)
        labelChoicePlots.setWordWrap(True)
        labelChoicePlots.move(600, 300)

        # stałe parametry
        x0, y0, dx = 600, 360, 100  

        # tworzymy przyciski zakresu
        self.plotParamA_E = QPushButton("A", self.cal_enset_view)
        self.plotParamB_E = QPushButton("B", self.cal_enset_view)
        self.plotParamN_E = QPushButton("N", self.cal_enset_view)

        toggle_style = """
        QPushButton {
            background-color: #ffb3c6;
            border: 2px solid #fb6f92;
            border-radius: 5px;
            padding: 4px 8px;
            font-size: 14px;
        }
        QPushButton:checked {
            background-color: #fb6f92;
        }
        """

        for i, btn in enumerate((self.plotParamA_E, self.plotParamB_E, self.plotParamN_E)):
            btn.setFixedSize(60, 30)
            btn.move(x0 + i*dx, y0)     # ten sam y0, równy odstęp dx
            btn.setCheckable(True)
            btn.setStyleSheet(toggle_style)
            btn.hide()                  # pokaż/chowaj tylko w handlerze

        self.plotParamGroupE = QButtonGroup(self.cal_enset_view)
        self.plotParamGroupE.setExclusive(True)
        for btn in (self.plotParamA_E, self.plotParamB_E, self.plotParamN_E):
            self.plotParamGroupE.addButton(btn)


        # Przycisk Erlanga
        buttonEngset = QPushButton("Teoria Erlanga", self.cal_enset_view)
        buttonEngset.setFont(self.fontSmall)
        buttonEngset.setStyleSheet(self.buttonStyle)
        buttonEngset.move(600, 450)
        buttonEngset.resize(300, 100)
        buttonEngset.setGraphicsEffect(create_shadow())
        buttonEngset.clicked.connect(self.show_info_enset_view)

        # Przycisk powrót
        buttonBack = QPushButton("↩ Powrót", self.cal_enset_view)
        buttonBack.setFont(self.fontSmall)
        buttonBack.setStyleSheet(self.buttonStyle)
        buttonBack.move(680, 600)
        buttonBack.setGraphicsEffect(create_shadow())
        buttonBack.clicked.connect(self.show_calculator_view)

        buttonCal = QPushButton("Oblicz", self.cal_enset_view)
        buttonCal.setFont(self.fontSmall)
        buttonCal.setStyleSheet(self.buttonStyle)
        buttonCal.move(50, 570)
        buttonCal.resize(500, 100)
        buttonCal.setGraphicsEffect(create_shadow())
        buttonCal.clicked.connect(self.enset_chooser)

        self.result_window = ResultWindow()
        self.result_window.show()

    def handle_radio_button_change(self):
        # Resetuj wszystkie pola
        self.AInput.setEnabled(True)
        self.AInput.setPlaceholderText("np. 420 lub 21-37 (Liczby muszą byc pomiedzy 0.1 a 100)")
        self.BInput.setEnabled(True)
        self.BInput.setPlaceholderText("np. 0.03 (Liczby muszą byc pomiedzy 0.001 a 0.499)")
        self.NInput.setEnabled(True)
        self.NInput.setPlaceholderText("np. 420 lub 21-37 (Liczby całkowite muszą byc pomiedzy 1 a 100)")
        self.numInput.setEnabled(True)
        self.numInput.setPlaceholderText("np. 420 lub 21-37 (Liczby całkowite muszą byc pomiedzy 10 a 2000)")

        # Wyłącz odpowiednie pole na podstawie wyboru
        if self.option1_A.isChecked():
            self.AInput.setEnabled(False)
            self.AInput.setPlaceholderText("")
        elif self.option2_B.isChecked():
            self.BInput.setEnabled(False)
            self.BInput.setPlaceholderText("")
        elif self.option3_N.isChecked():
            self.NInput.setEnabled(False)
            self.NInput.setPlaceholderText("")

        # 1) chowamy wszystkie pola wejściowe
        self.AInput.hide()
        self.BInput.hide()
        self.NInput.hide()
        self.numInput.hide()

        # 2) chowamy i odznaczamy przyciski zakresu Engseta
        for btn in (self.plotParamA_E, self.plotParamB_E, self.plotParamN_E):
            btn.hide()
            btn.setChecked(False)

        # 3) w zależności od wybranej opcji pokazujemy odpowiednie pola
        if self.option1_A.isChecked():
            # obliczamy A → potrzebujemy B, N, numInput
            self.BInput.show()
            self.NInput.show()
            self.numInput.show()
            # dodatkowo pokaż przyciski zakresu dla B i N
            self.plotParamB_E.show()
            self.plotParamB_E.move(650, 390)
            self.plotParamB_E.setFixedSize(80, 50)
            self.plotParamN_E.show()
            self.plotParamN_E.move(780, 390)
            self.plotParamN_E.setFixedSize(80, 50)

        elif self.option2_B.isChecked():
            # obliczamy B → potrzebujemy A, N, numInput
            self.AInput.show()
            self.NInput.show()
            self.numInput.show()
            self.plotParamA_E.show()
            self.plotParamA_E.setFixedSize(80, 50)
            self.plotParamA_E.move(650, 390)
            self.plotParamN_E.show()
            self.plotParamN_E.move(780, 390)
            self.plotParamN_E.setFixedSize(80, 50)

        elif self.option3_N.isChecked():
            # obliczamy N → potrzebujemy A, B, numInput
            self.AInput.show()
            self.BInput.show()
            self.numInput.show()
            self.plotParamA_E.show()
            self.plotParamA_E.move(780, 390)
            self.plotParamA_E.setFixedSize(80, 50)
            self.plotParamB_E.show()
            self.plotParamB_E.move(650, 390)
            self.plotParamB_E.setFixedSize(80, 50)



    """Funkcja, która pobiera dane z pola tekstowego i zwraca je w postaci listy"""

    def value_get(self, text):
        try:
            # Usuń zbędne spacje
            text = text.replace(" ", "")

            # Jeśli tekst zawiera znak "-", traktujemy to jako przedział
            if "-" in text:
                parts = list(map(float, text.split("-")))  # Podziel tekst po "-"
                if len(parts) == 2:
                    return parts  # Zwróć przedział jako listę
            elif not text:
                return 0
            else:
                # Jeśli nie zawiera "-", traktujemy to jako pojedynczą liczbę
                return float(text)  # Zwróć pojedynczą liczbę

        except ValueError:
            # Obsługuje przypadek, gdy nie uda się przekonwertować tekstu na liczbę
            print(f"Błąd: Nieprawidłowy format danych '{text}'")
            return None

    def enset_chooser(self):

        textNum = self.numInput.text().replace(" ", "")
        value_Num = int(self.value_get(textNum))

        textB = self.BInput.text().replace(" ", "")  # usuń spacje
        value_B = self.value_get(textB)

        textN = self.NInput.text().replace(" ", "")
        value_N = int(self.value_get(textN))

        textA = self.AInput.text().replace(" ", "")
        value_A = self.value_get(textA)


        if self.option1_A.isChecked():     # obliczamy A
            if not (0.001 <= value_B <= 0.499 and 1 <= value_N <= 100 and 10 <= value_Num <= 2000):
                self.result_window.add_entry("Błąd: B, N lub liczba użytkowników poza zakresem", 0)
            else:
                wynik = Engset.engset_A(value_Num, value_N, value_B)
                self.result_window.add_entry(f"[Engset] A (przy B={value_B}, N={value_N}), value_Num={value_Num}", wynik)
            
            if self.plotParamB_E.isChecked():
                Bs = [i/50 for i in range(1, 50)]  
                As = [Engset.engset_A(value_Num, value_N, b) for b in Bs]
                draw_chart(Bs, As, "Prawdopodobieństwo blokady B", "Natężenie ruchu A", value_B, wynik)

            elif self.plotParamN_E.isChecked():

                Ns = list(range(1, value_N + 1))
                As = [Engset.engset_A(value_Num, n, value_B) for n in Ns]
                draw_chart(Ns, As, "Liczba kanałów N", "Natężenie ruchu A", value_N, wynik)

        elif self.option2_B.isChecked(): 
            if not (0.1 <= value_A <= 100 and 1 <= value_N <= 100 and 10 <= value_Num <= 2000):
                self.result_window.add_entry("Błąd: A, N lub liczba użytkowników poza zakresem", 0)
            
            else:
                wynik = Engset.engset_b(value_A, value_Num, value_N)
                self.result_window.add_entry(f"[Engeset] B (przy A={value_A}, N={value_N}, value_Num={value_Num})", wynik)

            if self.plotParamN_E.isChecked():
                Ns = list(range(1, value_N + 1))
                As = [Engset.engset_b(value_A, value_Num, n) for n in Ns]
                draw_chart(Ns, As, "Liczba kanałów N", "Prawdopodobieństwo blokady B", value_N, wynik)

            elif self.plotParamA_E.isChecked():
                As1 = list(range(1, int(value_A) + 1))
                As = [Engset.engset_b(b, value_Num, value_N) for b in As1]
                draw_chart(As1, As, "Natężenie ruchu A", "Prawdopodobieństwo blokady B", value_A, wynik)

        elif self.option3_N.isChecked(): 
            if not (0.1 <= value_A <= 100 and 0.001 <= value_B <= 0.499 and 10 <= value_Num <= 2000):
                self.result_window.add_entry("Błąd: A, B lub liczba użytkowników poza zakresem", 0)

            else:
                wynik = Engset.engset_N(value_A, value_Num, value_B)
                self.result_window.add_entry(f"[Engset] N (przy A={value_A}, value_num={value_Num}, B={value_B})", wynik)

            if self.plotParamB_E.isChecked(): 
                Bs = [i / 100 for i in range(1, 100)]  # np. 0.01 - 0.99
                Ns = [Engset.engset_N(value_A, value_Num, b) for b in Bs]
                Bs_filtered, Ns_filtered = zip(*[(b, n) for b, n in zip(Bs, Ns) if n is not None])
                draw_chart(Bs_filtered, Ns_filtered, "Prawdopodobieństwo blokady B", "Liczba kanałów N", value_B, wynik)

            elif self.plotParamA_E.isChecked():
                As1 = [i / 2 for i in range(1, int(value_A * 2) + 1)]  # kroki co 0.5
                As_filtered = []
                Ns_filtered = []
                
                for a in As1:
                    n = Engset.engset_N(a, value_Num, value_B)
                    if n is None or n == value_Num: 
                        break
                    As_filtered.append(a)
                    Ns_filtered.append(n)

                draw_chart(As_filtered, Ns_filtered, "Natężenie ruchu A", "Liczba kanałów N", value_A, wynik)


        else:
            self.result_window.add_entry("Błąd: wybierz jedną opcję", 0)


    def erlang_chooser(self):

        textB = self.BInputEL.text().replace(" ", "")  # usuń spacje
        value_B = self.value_get(textB)

        textN = self.NInputEL.text().replace(" ", "")
        value_N = int(self.value_get(textN))

        textA = self.AInputEL.text().replace(" ", "")
        value_A = self.value_get(textA)

        # Liczenie wartości dla różnych inputów
        if self.option1_AEL.isChecked(): 
            if not (0.001 <= value_B <= 0.999 and 1 <= value_N <= 180):
                self.result_window.add_entry("Błąd: B lub N poza zakresem", 0)
            else:
                wynik = erlang.erlang_A(value_B, value_N)
                self.result_window.add_entry(f"[Erlang] A (przy B={value_B}, N={value_N})", wynik)

            if self.plotParamN.isChecked():
                Ns = list(range(1, value_N + 1))
                As = [erlang.erlang_A(value_B, n) for n in Ns]
                draw_chart(Ns, As, "Liczba kanałów N", "Natężenie ruchu A", value_N, wynik)

            elif self.plotParamB.isChecked():
                Bs = [i/50 for i in range(1, 50)]
                As = [erlang.erlang_A(b, value_N) for b in Bs]
                draw_chart(Bs, As, "Prawdopodobieństwo blokady B", "Natężenie ruchu A", value_B, wynik)


        elif self.option2_BEL.isChecked():  # liczymy B, mamy A i N
            if not (0.1 <= value_A <= 180 and 1 <= value_N <= 180):
                self.result_window.add_entry("Błąd: A lub N poza zakresem", 0)
            else:
                wynik = erlang.erlang_b(value_A, value_N)
                self.result_window.add_entry(f"[Erlang] B (przy A={value_A}, N={value_N})", wynik)


            if self.plotParamN.isChecked():
                Ns = list(range(1, value_N + 1))
                As = [erlang.erlang_b(value_A, n) for n in Ns]
                draw_chart(Ns, As, "Liczba kanałów N", "Prawdopodobieństwo blokady B", value_N, wynik)

            elif self.plotParamA.isChecked():
                As1 = list(range(1, int(value_A) + 1))
                As = [erlang.erlang_b(b, value_N) for b in As1]
                draw_chart(As1, As, "Natężenie ruchu A", "Prawdopodobieństwo blokady B", value_A, wynik)

        elif self.option3_NEL.isChecked():  # liczymy N, mamy A i B
            if not (0.1 <= value_A <= 180 and 0.001 <= value_B <= 0.999):
                self.result_window.add_entry("Błąd: A lub B poza zakresem", 0)
            else:
                wynik = erlang.erlang_N(value_A, value_B)
                self.result_window.add_entry(f"[Erlang] N (przy A={value_A}, B={value_B})", wynik)

            if self.plotParamB.isChecked():
                Bs = [i/50 for i in range(1, 50)]
                As = [erlang.erlang_N(value_A, b) for b in Bs]
                draw_chart(Bs, As, "Prawdopodobieństwo blokady B", "Liczba kanałów N", value_B, wynik)

            elif self.plotParamA.isChecked():
                As1 = list(range(1, int(value_A) + 1))
                As = [erlang.erlang_N(b, value_B) for b in As1]
                draw_chart(As1, As, "Natężenie ruchu A", "Liczba kanałów N", value_A, wynik)
        else:
            self.result_window.add_entry("Błąd: wybierz jedną opcję", 0)


    def show_main_view(self):
        """ Przełącza do głównego widoku """
        self.info_view.hide()
        self.calculator_view.hide()
        self.result_window.hide()
        self.main_view.show()

    def show_info_view(self):
        """ Przełącza do widoku informacji """
        self.main_view.hide()
        self.calculator_view.hide()
        self.info_erlang_view.hide()
        self.info_enset_view.hide()
        self.result_window.hide()
        self.info_view.show()

    def show_calculator_view(self):
        """ Przełącza do widoku kalkulatora """
        self.main_view.hide()
        self.info_view.hide()
        self.calculator_view.show()
        self.result_window.show()
        self.cal_enset_view.hide()
        self.cal_erlang_view.hide()

    def show_info_erlang_view(self):
        """ Przełącza do widoku Erlang """
        self.main_view.hide()
        self.info_view.hide()
        self.result_window.hide()
        self.calculator_view.hide()
        self.info_erlang_view.show()
        self.cal_erlang_view.hide()
        self.cal_enset_view.hide()

    def show_info_enset_view(self):
        """ Przełącza do widoku Erlang """
        self.main_view.hide()
        self.info_view.hide()
        self.result_window.hide()
        self.calculator_view.hide()
        self.info_enset_view.show()
        self.cal_erlang_view.hide()
        self.cal_enset_view.hide()

    def show_cal_erlang_view(self):
        self.main_view.hide()
        self.info_view.hide()
        self.calculator_view.hide()
        self.cal_erlang_view.show()
        self.result_window.show()
        self.info_erlang_view.hide()
        self.info_enset_view.hide()
        self.cal_enset_view.hide()

    def show_cal_enset_view(self):
        self.main_view.hide()
        self.info_view.hide()
        self.calculator_view.hide()
        self.info_enset_view.hide()
        self.cal_enset_view.show()
        self.result_window.show()
    


# Uruchomienie aplikacji
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
