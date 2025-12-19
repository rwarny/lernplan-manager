from datetime import datetime
class Goal:
    """Repräsentiert ein Wochenziel im Lernplan"""
    def __init__(self, titel, kategorie, ziel_anzahl, aktuell=0, id=None):
        """
        Erstellt ein neues Wochenziel.

        Args:
            titel: Beschreibung des Ziels
            kategorie: Zugehörige Kategorie
            ziel_anzahl: Anzahl zu erreichender Einheiten
            aktuell: Aktueller Fortschritt
            id: Eindeutige ID (wird vom WeekManager gesetzt)
        """

        self.titel = titel
        self.kategorie = kategorie
        self.ziel_anzahl = ziel_anzahl
        self.aktuell = aktuell
        self.erstellt_am = datetime.now()
        self.id = id

    def increment(self):
        """ Erhöht den Fortschritt um 1, falls das Ziel noch nicht erreicht ist. """
        if self.aktuell < self.ziel_anzahl:
            self.aktuell += 1

    def get_progress(self):
        """
        Berechnet den Fortschritt in Prozent.

        Returns:
            Fortschritt in Prozent (0.0 - 100.0)
        """
        return round((self.aktuell / self.ziel_anzahl) * 100, 1)
    
    def is_completed(self):
        """
        Prüft, ob das Ziel erreicht wurde.
        
        Returns:
            bool: True wenn Ziel erreicht, sonst False
        """
        return self.aktuell >= self.ziel_anzahl
    
    def to_dict(self):
        """
        Wandelt das Ziel in ein Dictionary um.

        Returns: 
        dict: Alle Attribute als Dictionary (für JSON-Speicherung)
        """
        return {
            "id": self.id,
            "titel": self.titel,
            "ziel_anzahl": self.ziel_anzahl,
            "kategorie": self.kategorie,
            "aktuell": self.aktuell,
            "erstellt_am": self.erstellt_am.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Erstellt ein Goal aus einem Dictionary.

        Args:
            data: Dictionary mit Goal-Daten (aus JSON)

        Returns:
            Goal: Neues Goal-Objekt
        """
        goal = cls(
            titel=data["titel"],
            ziel_anzahl=data["ziel_anzahl"],
            kategorie=data["kategorie"],
            aktuell=data["aktuell"],
            id=data["id"]
        )
        goal.erstellt_am=datetime.fromisoformat(data["erstellt_am"])
        return goal
