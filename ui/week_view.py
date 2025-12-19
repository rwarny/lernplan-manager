import tkinter as tk
from constants import WOCHENTAGE, ZEITSLOTS, COLORS, FONT_SIZES, KATEGORIEN
from ui.dialogs import TaskDialog
from datetime import datetime, timedelta

class WeekView:
    """Kalender-Ansicht des Wochenplans (Tab 1). """
    def __init__(self, parent, week_manager):
        """ 
        Initialisiert die Wochenplan Ansicht.
        
        Args:
            parent: Das übergeordnete Widget (Tab-Frame)
            week_manager: Der WeekManager mit den Daten
        """
        self.parent = parent
        self.week_manager = week_manager

        # Haupt-Frame erstellen
        self.frame = tk.Frame(parent, bg=COLORS['bg'])
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Dictionary für die Slot-Frames
        self.slot_frames = {}

        # Grid erstellen
        self.create_grid()
        # Ansicht aktualisieren
        self.update_week_view()

    def create_grid(self):
        """ Erstellt das kalender-Grid mit Zeiten und Wochentagen """
        # Grid-Spalten konfigurieren (gleichmäßig verteilen)
        for i in range(8): # Spalte 0 = Zeit, Spalten 1-7 = Tage
            self.frame.grid_columnconfigure(i, weight=1)

        # Grid-Zeilen konfigurieren
        for i in range(len(ZEITSLOTS) + 1): # Zeile 0 = Header, Rest = Zeitslots
            self.frame.grid_rowconfigure(i, weight=1)

        # Wochentage-Labels erstellen (Zeile 0, Spalten 1-7)
        for col, tag in enumerate(WOCHENTAGE):
            label = tk.Label(
                self.frame,
                text=self._get_wochentag_mit_datum(col),
                bg=COLORS['bg'],
                fg=COLORS['accent'],
                font=("Arial", FONT_SIZES['normal'], 'bold')
            )
            label.grid(row=0, column=col + 1, sticky="nsew", padx=2, pady=2)

        # Zeit-Label erstellen (Spalte 0, Zeilen 1-7)
        for row, zeit in enumerate(ZEITSLOTS):
            label = tk.Label(
                self.frame,
                text=zeit,
                bg=COLORS['bg'],
                fg=COLORS['fg'],
                font=("Arial", FONT_SIZES['small'])
            )
            label.grid(row=row + 1, column=0, sticky="nsew", padx=2, pady=2)

        # Slot-Frames erstellen (für jeden Tag/Zeit)
        for row, zeit in enumerate(ZEITSLOTS):
            for col, tag in enumerate(WOCHENTAGE):
                slot_frame = tk.Frame(
                    self.frame,
                    bg=COLORS['bg_light'],
                    relief="ridge",
                    bd=1
                )
                slot_frame.grid(row=row + 1, column=col + 1, sticky="nsew", padx=2, pady=2)

                # Im Dictionary speichern für späteren Zugriff
                self.slot_frames[(tag, zeit)] = slot_frame

                # Hover-Effekt für den Slot
                slot_frame.bind("<Enter>", lambda e, sf=slot_frame: sf.config(bg=COLORS['accent2']))
                slot_frame.bind("<Leave>", lambda e, sf=slot_frame: sf.config(bg=COLORS['bg_light']))
        
                # Klick-Event binden
                slot_frame.bind("<Button-1>", lambda e, t=tag, z=zeit: self._on_slot_click(t, z))

    def _on_slot_click(self, wochentag, zeitslot):
        """ 
        Wird aufgerufen, wenn ein zeitslot angeklickt wird.
        
        Args:
            wochentag: Der angeklickte Wochentag
            zeitslot: Der angeklickte Zeitslot
        """
        if self.week_manager.auto_save_callback is None:
            from tkinter import messagebox
            messagebox.showinfo("Archiv", "Dies ist eine archivierte Woche.\n\nÄnderungen sind nicht möglich.")
            return
    
        TaskDialog(
            self.parent,
            self.week_manager,
            wochentag=wochentag,
            zeitslot=zeitslot,
            on_save=self.update_week_view
        )

    def update_week_view(self):
        """ Aktualisiert die Anzeige aller Zeitslots mit den aktuellen Tasks """
        # Alle Slots durchlaufen
        for (tag, zeit), slot_frame in self.slot_frames.items():
            # Alte Widgets in Slot löschen
            for widget in slot_frame.winfo_children():
                widget.destroy()

            # Tasks für diesen Slot holen
            tasks = self.week_manager.get_tasks_by_timeslot(tag, zeit)

            if tasks:
                # Tasks anzeigen
                for task in tasks:
                    farbe = KATEGORIEN.get(task.kategorie, "#95a5a6")

                    # Text anpassen: ✓ für erledigte Tasks
                    text = f"✓ {task.titel}" if task.erledigt else task.titel

                    label = tk.Label(
                        slot_frame,
                        text=text,
                        bg=farbe,
                        fg="white",
                        font=("Arial", FONT_SIZES['small']),
                        padx=5,
                        pady=5
                    )
                    label.pack(fill="x", padx=2, pady=2)
                    # Klock auf Task: Als erledigt markieren
                    label.bind("<Button-1>", lambda e, t=task: self._toggle_task(t))
                    label.bind("<Button-3>", lambda e, t=task: self._show_task_menu(e, t))
            else:
                # Leerer Slot - "+" anzeigen
                label = tk.Label(
                    slot_frame,
                    text="+",
                    bg=COLORS['bg_light'],
                    fg=COLORS['fg'],
                    font=("Arial", FONT_SIZES['large'])
                )
                label.pack(expand=True)
                # Klick auf "+" soll auch funktionieren
                label.bind("<Button-1>", lambda e, t=tag, z=zeit: self._on_slot_click(t, z))

    def _toggle_task(self, task):
        """ 
        Schaltet den erledigt Status eines Tasks um 
        
        Args:
            task: Der Task, dessen Status geändert werden soll
        """
        # Prüfen ob Schreibrechte vorhanden (nicht im Archiv-Modus)
        if self.week_manager.auto_save_callback is None:
            from tkinter import messagebox
            messagebox.showinfo("Archiv", "Dies ist eine archivierte Woche.\n\nÄnderungen sind nicht möglich.")
            return
        
        task.toggle_erledigt()
        self.week_manager.auto_save_callback()
        self.update_week_view()

    def _show_task_menu(self, event, task):
        """
        Zeigt ein Kontextmenüü für einen Task an.

        Args:
            event: das Maus-event
            task: Der Task, für den das Man angezeigt wird.
        """
        # Prüfen ob Schreibrechte vorhanden sind
        if self.week_manager.auto_save_callback is None:
            from tkinter import messagebox
            messagebox.showinfo(" Archiv", "Dies ist eine Archivierte Woche.\n\nVeränderungen sind nicht möglich.")
            return
        
        # Kontextmenü erstellen
        menu = tk.Menu(self.parent, tearoff=0)
        menu.add_command(label="Bearbeiten", command=lambda: self._edit_task(task))
        menu.add_command(label="Löschen", command=lambda: self._delete_task(task))

        # Menü anzeigen
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
            on_save=self.update_week_view
        )

    def _delete_task(self, task):
        """
        Löscht einen Task nach Bestätigung.
        
        Args:
            task: Der zu löschende Task
        """
        from tkinter import messagebox
        antwort = messagebox.askyesno("Löschen", f"Möchtest du '{task.titel}' wirklich löschen?")
        if antwort:
            self.week_manager.remove_task(task.id)
            self.update_week_view()

    def _get_wochentag_mit_datum(self, wochentag_index):
        """
        Gibt den Wochentag mit Datum zurück.
        
        Args:
            wochentag_index: Index des Wochentags (0=Montag, 6=Sonntag)
        
        Returns:
            str: z.B. "Montag 16.12."
        """
        # Aktuelles Jahr und Kalenderwoche vom WeekManager
        jahr = self.week_manager.jahr
        kw = self.week_manager.wochennummer
        
        # ISO-Kalenderwoche: Der 4. Januar ist immer in KW 1
        jan4 = datetime(jahr, 1, 4)
        # Montag der KW 1 finden
        montag_kw1 = jan4 - timedelta(days=jan4.weekday())
        # Montag der gewünschten KW
        erster_tag = montag_kw1 + timedelta(weeks=kw - 1)
        
        # Gewünschten Tag berechnen
        tag_datum = erster_tag + timedelta(days=wochentag_index)
        
        return f"{WOCHENTAGE[wochentag_index]} {tag_datum.strftime('%d.%m.')}"