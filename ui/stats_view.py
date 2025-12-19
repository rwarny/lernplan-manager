import tkinter as tk
from constants import COLORS, FONT_SIZES, KATEGORIEN

class StatsView:
    """ Statistik-Ansicht mit Übersicht über Aufgaben und Ziele (Tab 4). """
    def __init__(self, parent, week_manager):
        """
        Initialisiert die Statistik Ansicht.

        Args:
            parent: Das Übergeordnete Widget (Tab-Frame)
            week_manager: Der WeekManager mit den Daten
        """

        self.parent = parent
        self.week_manager = week_manager

        # Hauptframe erstellen
        self.haupt_frame = tk.Frame(parent, bg=COLORS['bg'])
        self.haupt_frame.pack(fill="both", expand=True, pady=5)

        # Aufrufe
        self.update_statistics()

    def update_statistics(self):
        """Aktualisiert die Statistik-Anzeige."""
        # Alte Widgets löschen
        for widget in self.haupt_frame.winfo_children():
            widget.destroy()

        # Statistiken vom WeekManager holen
        stats = self.week_manager.get_statistics()

        # Titel
        titel = tk.Label(
            self.haupt_frame,
            text="📊 Wochenstatistik",
            bg=COLORS['bg'],
            fg=COLORS['accent'],
            font=("Arial", FONT_SIZES['title'], "bold")
        )
        titel.pack(pady=20)
        
        # Aufgaben Statistiken
        tk.Label(
            self.haupt_frame,
            text="Aufgaben:",
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            font=("Arial", FONT_SIZES['normal'], 'bold')
        ).pack(pady=(10, 5))

        tk.Label(
            self.haupt_frame,
            text=f"Gesamt: {stats['tasks_gesamt']}",
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            font=("Arial", FONT_SIZES['normal'])
        ).pack()

        tk.Label(
            self.haupt_frame,
            text=f"Erledigt: {stats['tasks_erledigt']} ({stats['erledigungs_rate']}%)",
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            font=("Arial", FONT_SIZES['normal'])
        ).pack()

        tk.Label(
            self.haupt_frame,
            text=f"Offen: {stats['tasks_offen']}",
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            font=("Arial", FONT_SIZES['normal'])
        ).pack()

        # Ziele Statistiken
        tk.Label(
            self.haupt_frame,
            text="Ziele:",
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            font=("Arial", FONT_SIZES['normal'], 'bold')
        ).pack(pady=(20, 5))

        tk.Label(
            self.haupt_frame,
            text=f"Gesamt: {stats['goals_gesamt']}",
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            font=("Arial", FONT_SIZES['normal'])
        ).pack()

        tk.Label(
            self.haupt_frame,
            text=f"Erreicht: {stats['goals_erreicht']}",
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            font=("Arial", FONT_SIZES['normal'])
        ).pack()

        # Aufgaben pro Kategorie
        tk.Label(
            self.haupt_frame,
            text="Aufgaben pro Kategorie:",
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            font=("Arial", FONT_SIZES['normal'], 'bold')
        ).pack(pady=(20, 5))

        for kategorie, farbe in KATEGORIEN.items():
            anzahl = stats['tasks_pro_kategorie'].get(kategorie, 0)
            tk.Label(
                self.haupt_frame,
                text=f"{kategorie}: {anzahl}",
                bg=farbe,
                fg="white",
                font=("Arial", FONT_SIZES['normal']),
                padx=10
            ).pack(pady=2)