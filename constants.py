KATEGORIEN = {
    "Anw.P": "#3498db",
    "ITT": "#9b59b6",
    "BGP": "#39884A",
    "Unterricht": "#e74c3c",
    "Projekte": "#f39c12",
    "Sonstiges": "#95a5a6"
}

ZEITSLOTS = [
    "08:00-08:45",
    "08:45-09:30",
    "09:35-10:20",
    "10:20-11:05",
    "11:10-11:55",
    "11:55-12:40",
    "13:25-14:10",
    "14:15-15:00",
    "15:00-16:00"
]

WOCHENTAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

FESTE_ZEITEN = {
    "Pause 1": {"start": "09:30", "end": "09:35"},
    "Pause 2": {"start": "11:05", "end": "11:10"},
    "Mittagspause": {"start": "12:40", "end": "13:25"},
    "Pause 3": {"start": "14:10", "end": "14:15"},
}

# UI Konstanten
WINDOW_TITLE = "Lernplan-Manager"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

COLORS = {
    "bg": "#1a1a2e",
    "bg_light": "#16213e",
    "fg": "#e0e0e0",
    "accent": "#64ffda",
    "accent2": "#667eea",
    "button1":"#4E0561", # normale Button Farbe
    "button2": "#027528", # Speichern Button
    "button3": "#F50000" # scholießen/löschen Button
}

FONT_SIZES = {
    "small": 10,
    "normal": 12,
    "large": 16,
    "title": 20
}

# JSON - Dateinamen 
JSON_FILENAME = "current_week.json" 
ARCHIVE_FOLDER = "archive"