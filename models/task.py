from datetime import datetime

class Task:
    """ Repräsentiert eine einzelne Aufgabe im Lernplan. """
    def __init__(self, titel, kategorie, wochentag, zeitslot, beschreibung="", erledigt=False, id=None):
        """
        Erstellt eine neue Aufgabe.
        
        Args:
            titel: Name der Aufgabe
            kategorie: Kategorie (z.B. "Python", "ITT")
            wochentag: Wochentag der Aufgabe (z.B. "Montag")
            zeitslot: Uhrzeit (z.B. "10:00")
            beschreibung: Optionale Details zur Aufgabe
            erledigt: Status der Aufgabe
            id: Eindeutige ID (wird vom WeekManager gesetzt)
        """
        self.titel = titel
        self.beschreibung = beschreibung 
        self.kategorie = kategorie 
        self.wochentag = wochentag 
        self.zeitslot = zeitslot 
        self.erledigt = erledigt 
        self.erstellt_am = datetime.now()
        self.id = id 

    def toggle_erledigt(self):
        """ Schaltet den Erledigt-Status der Aufgabe um """
        self.erledigt = not self.erledigt

    def to_dict(self):
        """
        Wandelt die Aufgabe in ein Dictionary um.

        Returns: 
        dict: Alle Attribute als Dictionary (für JSON-Speicherung)
        """
        return {
            "id": self.id,
            "titel": self.titel,
            "beschreibung": self.beschreibung,
            "kategorie": self.kategorie,
            "wochentag": self.wochentag,
            "zeitslot": self.zeitslot,
            "erledigt": self.erledigt,
            "erstellt_am": self.erstellt_am.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Erstellt eine Task aus einem Dictionary.

        Args:
            data: Dictionary mit Task-Daten (aus JSON)

        Returns:
            Task: Neues Task-Objekt
        """
        task = cls(
            titel=data["titel"],
            beschreibung=data["beschreibung"],
            kategorie=data["kategorie"],
            wochentag=data["wochentag"],
            zeitslot=data["zeitslot"],
            erledigt=data["erledigt"],
            id=data["id"]
        )
        task.erstellt_am=datetime.fromisoformat(data["erstellt_am"])
        return task
