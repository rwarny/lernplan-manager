import tkinter as tk
from tkinter import ttk, messagebox
from constants import COLORS, KATEGORIEN, WOCHENTAGE, FONT_SIZES
from ui.dialogs import TaskDialog

class TaskView:
    """ Listen-Ansicht aller Aufgaben mit Filter-Funktion (Tab2) """
    def __init__(self, parent, week_manager):
        """ 
        Initialisiert die Aufgaben-Listen-Ansicht.

        Args:
            parent: Das übergeordnete Widget (Tab-Frame)
            week_manager: Der WeekManager mit den Daten
        """
        self.parent = parent
        self.week_manager = week_manager

        # Canvas erstellen
        self.canvas = tk.Canvas(parent, bg=COLORS['bg'], highlightthickness=0)
        # Scrollbar erstellen
        self.scrollbar = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)

        # Canvas mit Scrollbar verbinden
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # einen inneren Frame im Canvas erstellen
        self.inner_frame = tk.Frame(self.canvas, bg=COLORS['bg'])
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.update_task_list())

        # Aufrufe:
        self._create_filter_bar()
        self.update_task_list()

    def _create_filter_bar(self):
        """ Erstellt die Filter-Leiste mit Dropdown-Menüs. """
        # Frame erstellen
        self.filter_frame = tk.Frame(self.parent, bg=COLORS['bg'])
        self.filter_frame.pack(fill="x", pady=5)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Comboboxen erstellen
        # Kategorie - Filter
        self.kategorie_label = tk.Label(
            self.filter_frame,
            text="Kategorie:",
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            font=("Arial", FONT_SIZES['normal'])
        )
        self.filter_kategorie = ttk.Combobox(
            self.filter_frame, 
            values=["Alle"] + list(KATEGORIEN.keys()),
            state="readonly"
            )

        # Status - Filter
        self.status_label = tk.Label(
            self.filter_frame,
            text="Status:",
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            font=("Arial", FONT_SIZES['normal'])
        )
        self.filter_status = ttk.Combobox(
            self.filter_frame,
            values=["Alle", "Offen", "Erledigt"],
            state="readonly"
            )

        # Wochentag - Filter
        self.wochentag_label = tk.Label(
            self.filter_frame,
            text="Wochentag:",
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            font=("Arial", FONT_SIZES['normal'])
        )
        self.filter_wochentag = ttk.Combobox(
            self.filter_frame,
            values=["Alle"] + list(WOCHENTAGE),
            state="readonly")
        
        # Sortieren - Auswahl
        self.sortieren_label = tk.Label(
            self.filter_frame,
            text="Sortieren:",
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            font=("Arial", FONT_SIZES['normal'])
        )
        self.filter_sortieren = ttk.Combobox(
            self.filter_frame,
            values=["Nach Datum", "Nach Kategorie"],
            state="readonly"
        )

        # Alles packen
        self.filter_wochentag.pack(side="right")
        self.wochentag_label.pack(side="right")

        self.filter_status.pack(side="right")
        self.status_label.pack(side="right")

        self.filter_kategorie.pack(side="right")
        self.kategorie_label.pack(side="right")

        
        self.filter_sortieren.pack(side="right")
        self.sortieren_label.pack(side="right")
        self.filter_sortieren.current(0) # Standard: nach Datum

        # Standartwerte setzen
        self.filter_wochentag.current(0)
        self.filter_status.current(0)
        self.filter_kategorie.current(0)

        # Filter - Events binden
        self.filter_kategorie.bind("<<ComboboxSelected>>", lambda e: self.update_task_list())
        self.filter_status.bind("<<ComboboxSelected>>", lambda e: self.update_task_list())
        self.filter_wochentag.bind("<<ComboboxSelected>>", lambda e: self.update_task_list())
        self.filter_sortieren.bind("<<ComboboxSelected>>", lambda e: self.update_task_list())

        # button erstellen
        self.new_task_button = tk.Button(self.filter_frame,
                                   text="+ Neue Aufgabe",
                                   bg=COLORS['button1'],
                                   fg=COLORS['fg'],
                                   command=self._on_new_task
                                   )
        self.new_task_button.pack(side="left", padx=(0, 20))

    def _on_new_task(self):
        """ Öffnet den Dialog zum Erstellen einer neuen Aufgabe. """
        # Prüfen ob Schreibrechte vorhanden (nicht im Archiv-Modus)
        if self.week_manager.auto_save_callback is None:
            messagebox.showinfo("Archiv", "Dies ist eine archivierte Woche.\n\nÄnderungen sind nicht möglich.")
            return
        
        TaskDialog(
            self.parent,
            self.week_manager,
            on_save=self.update_task_list
        )

    def update_task_list(self):
        """ Aktualisiert die Anzeige der Aufgaben-Liste. """
        # Alle alten Widget löschen
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Alle Tasks holen
        tasks = self.week_manager.tasks

        # Filter Werte holen
        kategorie = self.filter_kategorie.get()
        status = self.filter_status.get()
        tag = self.filter_wochentag.get()

        # gefilterte Tasks sammeln
        gefilterte_tasks = []
        for task in tasks:
            # kategorie - Filter prüfen
            if kategorie != "Alle" and task.kategorie != kategorie:
                continue

            # Status - Filter prüfen
            if status == "Offen" and task.erledigt:
                continue
            if status == "Erledigt" and not task.erledigt:
                continue
            
            # Wochentag - Filter prüfen
            if tag != "Alle" and task.wochentag != tag:
                continue

            gefilterte_tasks.append(task)

        # Sortieren
        sortierung = self.filter_sortieren.get()
        if sortierung == "Nach Datum":
            gefilterte_tasks.sort(key=lambda t: (WOCHENTAGE.index(t.wochentag), t.zeitslot))
        elif sortierung == "Nach Kategorie":
            gefilterte_tasks.sort(key=lambda t: t.kategorie)
            
        # Spaltenanzahl berechnen
        spalten = self._get_column_count()

        # Tasks im Grid anzeigen
        for index, task in enumerate(gefilterte_tasks):
            row = index // spalten
            col = index % spalten
            self._create_task_item(task, row, col)

    def _create_task_item(self, task, row=0, col=0):
        """
        Erstellt ein Widget für eine einzelne Aufgabe.

        Args:
            task: Das Task-Objekt, das angezeigt werden soll

        Returns:
            tk.Frame: Der erstellte Task-Frame
        """
        # Farbe der Kategorie holen
        farbe = KATEGORIEN.get(task.kategorie, "#95a5a6")
        
        # Haupt-Frame für diesen Task
        task_frame = tk.Frame(
            self.inner_frame,
            bg=farbe,
            relief="ridge",
            bd=2
        )
        task_frame.grid(row=row, column=col, padx=5, pady=3, sticky="nsew")
        
        # Checkbox-Symbol
        if task.erledigt:
            checkbox_text = "✓"
        else:
            checkbox_text = "☐"
        
        checkbox_label = tk.Label(
            task_frame,
            text=checkbox_text,
            bg=farbe,
            fg="white",
            font=("Arial", FONT_SIZES['large'])
        )
        checkbox_label.pack(side="left", padx=5)

        # Titel
        titel_label = tk.Label(
            task_frame,
            text=task.titel,
            bg=farbe,
            fg="white",
            font=("Arial", FONT_SIZES['normal'], "bold")
        )
        titel_label.pack(side="left", padx=5)
        
        # Info rechts
        info_text = f"{task.wochentag}, {task.zeitslot}"
        info_label = tk.Label(
            task_frame,
            text=info_text,
            bg=farbe,
            fg="white",
            font=("Arial", FONT_SIZES['small'])
        )
        info_label.pack(side="right", padx=5)

        # Rechtsklick-Menü für den ganzen Frame
        task_frame.bind("<Button-3>", lambda e, t=task: self._show_task_menu(e, t))
        checkbox_label.bind("<Button-3>", lambda e, t=task: self._show_task_menu(e, t))
        titel_label.bind("<Button-3>", lambda e, t=task: self._show_task_menu(e, t))
        info_label.bind("<Button-3>", lambda e, t=task: self._show_task_menu(e, t))

        return task_frame
    
    def _show_task_menu(self, event, task):
        """
        Zeigt ein Kontextmenü für einen Task an.
        
        Args:
            event: Das Maus-Event
            task: Der Task, für den das Menü angezeigt wird
        """
        if self.week_manager.auto_save_callback is None:
            messagebox.showinfo("Archiv", "Dies ist eine archivierte Woche.\n\nÄnderungen sind nicht möglich.")
            return
        
        menu = tk.Menu(self.parent, tearoff=0)
        menu.add_command(label="Bearbeiten", command=lambda: self._edit_task(task))
        menu.add_command(label="Löschen", command=lambda: self._delete_task(task))
        menu.post(event.x_root, event.y_root)

    def _edit_task(self, task):
        """
        Öffnet den Dialog zum Bearbeiten eines Tasks.
        
        Args:
            task: Der zu bearbeitende Task
        """
        TaskDialog(
            self.parent,
            self.week_manager,
            task=task,
            on_save=self.update_task_list
        )

    def _delete_task(self, task):
        """
        Löscht einen Task nach Bestätigung.
        
        Args:
            task: Der zu löschende Task
        """
        antwort = messagebox.askyesno("Löschen", f"Möchtest du '{task.titel}' wirklich löschen?")
        if antwort:
            self.week_manager.remove_task(task.id)
            self.update_task_list()

    def _get_column_count(self):
        """
        Berechnet die Anzahl der Spalten basierend auf Fensterbreite und längstem Titel.
        
        Returns:
            int: Anzahl der Spalten (mindestens 1, maximal 5)
        """
        breite = self.canvas.winfo_width()
        
        # Längsten Titel finden
        laengster_titel = 0
        for task in self.week_manager.tasks:
            if len(task.titel) > laengster_titel:
                laengster_titel = len(task.titel)
        
        # Geschätzte Breite: ca. 8 Pixel pro Zeichen + 150 Pixel für Checkbox, Datum, Padding
        geschaetzte_breite = (laengster_titel * 8) + 150
        
        # Mindestens 250 Pixel pro Spalte
        min_spaltenbreite = max(250, geschaetzte_breite)
        
        spalten = breite // min_spaltenbreite
        
        # Mindestens 1, maximal 5 Spalten
        return max(1, min(spalten, 5))
    
