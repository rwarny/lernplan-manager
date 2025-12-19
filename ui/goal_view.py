import tkinter as tk
from constants import COLORS, FONT_SIZES, KATEGORIEN
from ui.dialogs import GoalDialog

def aufhellen(hex_farbe, faktor=0.3):
    """
    Macht eine Hex-Farbe Heller

    Args:
        hex_farbe: Farbe im Format "#RRGGBB"
        faktor: Wie viel heller (0.0 - 1.0)
    
    Returns:
        str: Die aufgehellte farbe
    """
    hex_farbe = hex_farbe.lstrip('#')
    r = int(hex_farbe[0:2], 16)
    g = int(hex_farbe[2:4], 16)
    b = int(hex_farbe[4:6], 16)
    
    r = int(r + (255 - r) * faktor)
    g = int(g + (255 - g) * faktor)
    b = int(b + (255 - b) * faktor)
    
    return f'#{r:02x}{g:02x}{b:02x}'


class GoalView:
    """ Ansicht für Wochenziele mt Fortschritt-Tracking (Tab 3) """
    def __init__(self, parent, week_manager):
        """
        Initialisiert die Ziele-Ansicht.
          
        Args:
            parent: Das übergeordneteWidget (Tab-Frame)
            week_manager: Der WeekManager mit allen Daten
        """
        self.parent = parent
        self.week_manager = week_manager

        # Button Frame oben
        self.button_frame = tk.Frame(parent, bg=COLORS['bg'])
        self.button_frame.pack(fill="x", pady=5)

        # Button für neues Ziel
        self.new_goal_button = tk.Button(
            self.button_frame,
            text="+ Neues Ziel",
            bg=COLORS['button1'],
            fg=COLORS['fg'],
            command=self._on_new_goal
        )
        self.new_goal_button.pack(side="left", padx=10)

        # Canvas erstellen
        self.canvas = tk.Canvas(parent, bg=COLORS['bg'], highlightthickness=0)
        # Scrollbar erstellen
        self.scrollbar = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)

        # Canvas mit Scrollbar verbinden
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # einen inneren Frame im Canvas erstellen
        self.inner_frame = tk.Frame(self.canvas, bg=COLORS['bg'])
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.update_goal_list())

        # Aufrufe
        self.update_goal_list()

    def _on_new_goal(self):
        """ Öffnet den Dialog zum Erstellen eines neuen Ziels. """
        # Prüfen ob Schreibrechte vorhanden (nicht im Archiv-Modus)
        if self.week_manager.auto_save_callback is None:
            from tkinter import messagebox
            messagebox.showinfo("Archiv", "Dies ist eine archivierte Woche.\n\nÄnderungen sind nicht möglich.")
            return
        
        GoalDialog(
            self.parent,
            self.week_manager,
            on_save=self.update_goal_list
        )

    def update_goal_list(self):
        """ Aktualisiert die Anzeige der Ziele-Liste. """
        # Alte Widgets löschen
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Spaltenanzahl berechnen
        spalten = self._get_column_count()

        # Alle Goals holen und anzeigen
        for index, goal in enumerate(self.week_manager.goals):
            row = index // spalten
            col = index % spalten
            self._create_goal_item(goal, row, col)

    def _create_goal_item(self, goal, row=0, col=0):
        """
        Erstellt ein Widget für eine einzelne Aufgabe.

        Args:
            goal: Das Goal-Objekt, das angezeigt werden soll

        Returns:
            tk.Frame: Der erstellte Task-Frame
        """
        # Farbe der Kategorie holen
        farbe = KATEGORIEN.get(goal.kategorie, "#95a5a6")
        
        # Haupt-Frame
        goal_frame = tk.Frame(
            self.inner_frame,
            bg=farbe,
            relief="ridge",
            bd=2
        )
        goal_frame.grid(row=row, column=col, padx=5, pady=3, sticky="nsew")
        
        # Titel
        titel_label = tk.Label(
            goal_frame,
            text=goal.titel,
            bg=farbe,
            fg="white",
            font=("Arial", FONT_SIZES['normal'], "bold")
        )
        titel_label.pack(side="left", padx=5)

        # Fortschritt
        fortschritt_label = tk.Label(
            goal_frame,
            text=f"{goal.aktuell}/{goal.ziel_anzahl} ({goal.get_progress()}%)",
            bg=COLORS['bg_light'],
            fg=COLORS['fg'],
            font=("Arial", FONT_SIZES['normal'])
        )
        fortschritt_label.pack(side="right", padx=5)

        # Kleiner Canvas für den Balken
        bar_canvas = tk.Canvas(goal_frame, width=200, height=20, bg=COLORS['bg'], highlightthickness=0)
        bar_canvas.pack(side="left", padx=10)

        # Fortschritt berechnen (0.0 bis 1.0)
        progress = goal.aktuell / goal.ziel_anzahl

        # Gefüllten Teil zeichnen
        helle_farbe = aufhellen(farbe, 0.4)
        bar_canvas.create_rectangle(0, 0, 200 * progress, 20, fill=helle_farbe, outline="")

        plus_button = tk.Button(
            goal_frame,
            text="+1",
            command=lambda g=goal: self._increment_goal(g)
        )
        plus_button.pack(padx=5, pady=5)

        # Events binden
        goal_frame.bind("<Button-3>", lambda e, g=goal: self._show_goal_menu(e, g))
        titel_label.bind("<Button-3>", lambda e, g=goal: self._show_goal_menu(e, g))
        fortschritt_label.bind("<Button-3>", lambda e, g=goal: self._show_goal_menu(e, g))
        
        return goal_frame
    
    def _increment_goal(self, goal):
        """Erhöht den Fortschritt eines Ziels um 1."""
        # Prüfen ob Schreibrechte vorhanden (nicht im Archiv-Modus)
        if self.week_manager.auto_save_callback is None:
            from tkinter import messagebox
            messagebox.showinfo("Archiv", "Dies ist eine archivierte Woche.\n\nÄnderungen sind nicht möglich.")
            return
        goal.increment()
        self.week_manager.auto_save_callback()
        self.update_goal_list()

    def _show_goal_menu(self, event, goal):
        """
        Zeigt ein Kontextmenü für ein Goal an.
        
        Args:
            event: Das Maus-Event
            goal: Das Goal, für das das Menü angezeigt wird
        """
        if self.week_manager.auto_save_callback is None:
            from tkinter import messagebox
            messagebox.showinfo("Archiv", "Dies ist eine archivierte Woche.\n\nÄnderungen sind nicht möglich.")
            return
        
        menu = tk.Menu(self.parent, tearoff=0)
        menu.add_command(label="Bearbeiten", command=lambda: self._edit_goal(goal))
        menu.add_command(label="Löschen", command=lambda: self._delete_goal(goal))
        menu.post(event.x_root, event.y_root)

    def _edit_goal(self, goal):
        """
        Öffnet den Dialog zum Bearbeiten eines Goals.
        
        Args:
            goal: Das zu bearbeitende Goal
        """
        GoalDialog(
            self.parent,
            self.week_manager,
            goal=goal,
            on_save=self.update_goal_list
        )

    def _delete_goal(self, goal):
        """
        Löscht ein Goal nach Bestätigung.
        
        Args:
            goal: Das zu löschende Goal
        """
        from tkinter import messagebox
        antwort = messagebox.askyesno("Löschen", f"Möchtest du '{goal.titel}' wirklich löschen?")
        if antwort:
            self.week_manager.remove_goal(goal.id)
            self.update_goal_list()

    def _get_column_count(self):
        """
        Berechnet die Anzahl der Spalten basierend auf Fensterbreite und längstem Titel.
        
        Returns:
            int: Anzahl der Spalten (mindestens 1, maximal 5)
        """
        breite = self.canvas.winfo_width()
        
        # Längsten Titel finden
        laengster_titel = 0
        for goal in self.week_manager.goals:
            if len(goal.titel) > laengster_titel:
                laengster_titel = len(goal.titel)
        
        # Geschätzte Breite: ca. 8 Pixel pro Zeichen + 350 für Balken, Button, Padding
        geschaetzte_breite = (laengster_titel * 8) + 350
        
        min_spaltenbreite = max(400, geschaetzte_breite)
        
        spalten = breite // min_spaltenbreite
        
        return max(1, min(spalten, 5))