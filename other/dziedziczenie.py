# MicroPython 1.24.1 ESP32-S3 Octal SPIRAM

class Zwierze():
    def __init__(self, imie, wiek):
        print(f"Zwierze.__init__({self}, {imie}, {wiek})")
        self.imie = imie
        self.wiek = wiek
        
    def przedstaw_sie(self):
        print(f"Zwierze.przedstaw_sie({self})")
        print(f"- Nazywam sie {self.imie}")
        
    def ile_masz_lat(self):
        print(f"Zwierze.ile_masz_lat({self})")
        print(f"- Mam {self.wiek} lat")
        
    def metoda_polimorficzna(self):
        print(f"Zwierze.metoda_polimorficzna()")
 
class Pies(Zwierze):
    def __init__(self, rasa, kolor):
        print(f"Pies.__init__({self}, {rasa}, {kolor})")
        self.rasa  = rasa
        self.kolor = kolor
        super().__init__("Reksio", 100)
        
    def szczekaj(self):
        print(f"Pies.szczekaj({self})")
        print(f"- Hau hau")
        
    def opisz_sie(self):
        print(f"Pies.opisz_sie({self})")
        print(f"- imie: {self.imie}")
        print(f"- kolor: {self.kolor}")
        print(f"- rasa: {self.rasa}")
        print(f"- wiek: {self.wiek}")
    
    def metoda_polimorficzna(self):
        print(f"Pies.metoda_polimorficzna()")

if __name__ == "__main__":
    print("=== 1 ===")
    zwierzak = Zwierze("Test", 10)
    zwierzak.przedstaw_sie()
    zwierzak.ile_masz_lat()
    zwierzak.metoda_polimorficzna()
    
    print("=== 2 ===")
    reksio = Pies("jamnik", "brazowy")
    reksio.ile_masz_lat()
    reksio.opisz_sie()
    reksio.metoda_polimorficzna()
    
    