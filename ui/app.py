import tkinter as tk
from constants import WINDOW_TITLE, WINDOW_HEIGHT, WINDOW_WIDTH, COLORS, JSON_FILENAME, ARCHIVE_FOLDER
from managers.storage import load_week, save_week, archive_week, export_to_txt
from tkinter import ttk, messagebox, filedialog
from ui.week_view import WeekView
from ui.task_view import TaskView
from ui.goal_view import GoalView
from ui.stats_view import StatsView
from ui.dialogs import TaskDialog, GoalDialog
import os


class LernplanUI:
    """ Hauptfenster der Lernplan-Manager Anwendung """
    def __init__(self):
        """ Initialisiert das Hauptfenster und lädt die Daten """
        # Fenster erstellen
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=COLORS["bg"])

        # Daten Laden
        self.week_manager = load_week(JSON_FILENAME)
        self.week_manager.auto_save_callback = self.auto_save

        # Tabs erstellen
        self.create_tabs()

        # Header Frame erstellen
        self.header_frame = tk.Frame(self.root, bg=COLORS['bg'])
        self.header_frame.pack(fill="x", padx=10, pady=(10, 0))

        # Wochennummer anzeigen
        self.week_label = tk.Label(
            self.header_frame,
            text=f"KW {self.week_manager.wochennummer} - {self.week_manager.jahr}",
            bg=COLORS['bg'],
            fg=COLORS['accent'],
            font=("Arial", 16, "bold")
        )
        self.week_label.pack(side="left")

        # Button zum archivieren erstellen
        self.new_week_button = tk.Button(
            self.header_frame,
            text="Neue Woche starten",
            bg=COLORS['button1'],
            fg=COLORS['fg'],
            command=self._start_new_week
        )
        self.new_week_button.pack(side="right")

        # Button zum durchsuchen des archives

        self.archive_button = tk.Button(
            self.header_frame,
            text="Archiv ansehen",
            bg=COLORS['button1'],
            fg=COLORS['fg'],
            command=self._show_archive
        )
        self.archive_button.pack(side="right", padx=(0,10))

        # Button um zur aktuellen Woche zurückzukehren
        self.back_button = tk.Button(
            self.header_frame,
            text="Aktuelle Woche",
            bg=COLORS['button2'],
            fg=COLORS['fg'],
            command=self._back_to_current_week
        )
        

        self.export_txt_button = tk.Button(
            self.header_frame,
            text="Als TXT exportieren",
            bg=COLORS['button1'],
            fg=COLORS['fg'],
            command=self._export_txt
        )
        self.export_txt_button.pack(side="right", padx=(0, 10))

        # notebook packen
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Statusleiste erstellen
        self.status_frame = tk.Frame(self.root, bg=COLORS['bg_light'])
        self.status_frame.pack(fill="x", side="bottom", padx=10, pady=5)

        self.status_label = tk.Label(
            self.status_frame,
            text="",
            bg=COLORS['bg_light'],
            fg=COLORS['fg'],
            font=("Arial", 10)
        )
        self.status_label.pack(side="left", pady=10)

        # Views erstellen
        self.week_view = WeekView(self.tab_wochenplan, self.week_manager)
        self.task_view = TaskView(self.tab_aufgaben, self.week_manager)
        self.goal_view = GoalView(self.tab_ziele, self.week_manager)
        self.stats_view = StatsView(self.tab_statistik, self.week_manager)

        # Tasten und Funtkionen binden
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        self.root.bind("<Control-n>", lambda e: self._neue_aufgabe())
        self.root.bind("<Control-g>", lambda e:self._neues_ziel())
        self.root.bind("<Control-e>", lambda e:self._export_txt())
        self.root.bind("<Control-s>", lambda e:self._manuell_speichern())

        self._create_tooltip(self.new_week_button, "Aktuelle Woche archivieren")
        self._create_tooltip(self.export_txt_button, "CTRL+E")

        self._create_hover_effect(self.new_week_button, COLORS['button1'], COLORS['accent2'])
        self._create_hover_effect(self.archive_button, COLORS['button1'], COLORS['accent2'])
        self._create_hover_effect(self.back_button, COLORS['button2'], COLORS['accent'])
        self._create_hover_effect(self.export_txt_button, COLORS['button1'], COLORS['accent2'])

        self._update_status()

    def run(self):
        """ Startet die Anwendung """
        self.root.mainloop()

    def create_tabs(self):
        """ Erstellt das Tab-System mit allen Tabs """
        # Notebook erstellen 
        self.notebook = ttk.Notebook(self.root)

        # Tab Frames erstellen
        self.tab_wochenplan = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.tab_aufgaben = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.tab_ziele = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.tab_statistik = tk.Frame(self.notebook, bg=COLORS['bg'])

        # Tabs zum Notebook hinzufügen
        self.notebook.add(self.tab_wochenplan, text="Wochenplan")
        self.notebook.add(self.tab_aufgaben, text="Aufgaben")
        self.notebook.add(self.tab_ziele, text="Ziele")
        self.notebook.add(self.tab_statistik, text="Statistik")

    def auto_save(self):
        """ Speichert die aktuelle Woche automatisch """
        save_week(self.week_manager, JSON_FILENAME)
        self._update_status()

    def _on_tab_changed(self, event):
        """ Aktualisiert die View beim Tab-Wechsel. """
        self.task_view.update_task_list()
        self.goal_view.update_goal_list()
        self.stats_view.update_statistics()

    def _start_new_week(self):
        """ Archiviert die aktuelle Woche und startet eine Neue. """
        # Bestätigung abfragen
        antwort = messagebox.askyesno(
            "Neue Woche",
            "Möchtest du die aktuelle Woche archivieren und eine neue starten?\n\n"
            "Alle Aufgaben und ziele werden gespeichert."
        )

        if antwort:
            # Woche archivieren und neuen Manager bekommen
            self.week_manager = archive_week(self.week_manager)
            self.week_manager.auto_save_callback = self.auto_save

            # Neue leere Woche starten
            self.auto_save()


            # Label aktualisieren
            self.week_label.config(
                text=f"KW {self.week_manager.wochennummer} - {self.week_manager.jahr}"
            )

            # Alle Views aktualisieren
            self._refresh_all_views()

    def _refresh_all_views(self):
        """ Aktualisiert alle Views mit dem neuen WeekManager"""
        self.week_view.week_manager = self.week_manager
        self.task_view.week_manager = self.week_manager
        self.goal_view.week_manager = self.week_manager
        self.stats_view.week_manager = self.week_manager

        self.week_view.update_week_view()
        self.task_view.update_task_list()
        self.goal_view.update_goal_list()
        self.stats_view.update_statistics()
        self._update_status()

    def _show_archive(self):
        """ Öffnet einen Dialog zum Ansehen archivierter Wochen. """
        # Prüfen ob Archiv-Ordner existiert
        if not os.path.exists(ARCHIVE_FOLDER):
            messagebox.showinfo("Archiv", "Noch keine archivierten Wochen vorhanden.")
            return
        
        # Archiv-Dateien auflisten
        dateien = [f for f in os.listdir(ARCHIVE_FOLDER) if f.endswith('.json')]

        if not dateien:
            messagebox.showinfo("Archiv", "Noch keine archivierten Wochen vorhanden")
            return
        
        # Dialog erstellen
        dialog = tk.Toplevel(self.root)
        dialog.title("Archiv")
        dialog.geometry("300x400")
        dialog.configure(bg=COLORS['bg'])
        dialog.grab_set()

        # Titel
        tk.Label(
            dialog,
            text="Archivierte Wochen:",
            bg=COLORS['bg'],
            fg=COLORS['accent'],
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Liste der Dateien
        listbox  = tk.Listbox(dialog, width=35, height=15)
        listbox.pack(pady=10, padx=10)

        for datei in sorted(dateien, reverse=True):
            listbox.insert(tk.END, datei.replace('.json', ''))

        # Buttons Frame
        button_frame = tk.Frame(dialog, bg=COLORS['bg'])
        button_frame.pack(pady=10)

        # Ansehen Button
        tk.Button(
            button_frame,
            text="Ansehen",
            bg=COLORS['button2'],
            fg=COLORS['fg'],
            command=lambda: self._load_archive(listbox, dialog)
        ).pack(side="left", padx=5)

        # Schließen Button
        tk.Button(
            button_frame,
            text="Schließen",
            bg=COLORS['button3'],
            fg=COLORS['fg'],
            command=dialog.destroy
        ).pack(side="left", padx=5)

    def _load_archive(self, listbox, dialog):
        """Lädt eine archivierte Woche zur Ansicht (read-only)."""
        
        # Prüfen ob etwas ausgewählt ist
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Archiv", "Bitte eine Woche auswählen!")
            return
        
        # Dateiname holen
        dateiname = listbox.get(selection[0]) + ".json"
        dateipfad = os.path.join(ARCHIVE_FOLDER, dateiname)
        
        # Archiv laden
        self.week_manager = load_week(dateipfad)
        self.week_manager.auto_save_callback = None  # Read-only: kein Auto-Save!
        
        # Label aktualisieren (mit Hinweis)
        self.week_label.config(
            text=f"KW {self.week_manager.wochennummer} - {self.week_manager.jahr} (Archiv - nur Ansicht)"
        )

        # Button für Rückkehr zur aktuellen Woche packen
        self.back_button.pack(side="right", padx=(0, 10))

        # Views aktualisieren
        self._refresh_all_views()
        
        # Dialog schließen
        dialog.destroy()
        
        messagebox.showinfo("Archiv", "Archivierte Woche geladen.\n\nÄnderungen werden NICHT gespeichert!")

    def _back_to_current_week(self):
        """Lädt die aktuelle Woche wieder."""
        # Aktuelle Woche laden
        self.week_manager = load_week(JSON_FILENAME)
        self.week_manager.auto_save_callback = self.auto_save
        
        # Label aktualisieren (ohne Archiv-Hinweis)
        self.week_label.config(
            text=f"KW {self.week_manager.wochennummer} - {self.week_manager.jahr}"
        )

        # Button für aktuelle Woche wieder verstecken
        self.back_button.pack_forget()
        
        # Views aktualisieren
        self._refresh_all_views()
    
    def _export_txt(self):
        """ Öffnet einen Speichern-Dialog und exportiert den Wochenplan als TXT-Datei. """
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Textdatei", "*.txt")],
            initialfile=f"wochenplan_kw{self.week_manager.wochennummer}.txt"
        )
        if filename:
            export_to_txt(self.week_manager, filename)
            messagebox.showinfo("Export", "Wochenplan erfolgreich exportiert")

    def _neue_aufgabe(self):
        """
        Öffnet den Dialog zum Erstellen einer neuen Aufgabe.
        Wir durch Tastenkürzel Ctrl+N aufgerufen
        """
        TaskDialog(
            self.root,
            self.week_manager,
            on_save=self._refresh_all_views
        )
    
    def _neues_ziel(self):
        """
        Öffnet den Dialog zum Erstellen eines neuen Ziels.
        Wird durch Tastenkürzel Ctrl+G aufgerufen.
        """
        GoalDialog(
            self.root,
            self.week_manager,
            on_save=self._refresh_all_views
        )

    def _manuell_speichern(self):
        """
        Speichert die aktuelle Woche manuell.
        Wird durch Tastenkürzel Ctrl+S aufgerufen
        """
        self.auto_save()
        messagebox.showinfo("Manuell Speichern", "Das aktuelle Programm wurde Erfolgreich manuell gespeichert.")

    def _create_tooltip(self, widget, text):
        """
        Erstellt einen Tooltip für ein Widget.

        Args:
            widget: das Widget, das den Tooltip bekommen soll.
            text: Der anzuzeigende Tooltip-Text
        """
        tooltip = None

        def show_tooltip(event):
            nonlocal tooltip
            # Position berechnen (unterhalb des Widgets)
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + widget.winfo_height() + 5

            # Tooltip-Fenster erstellen
            tooltip = tk.Toplevel(self.root)
            tooltip.wm_overrideredirect(True) # Keine Fensterrahmen
            tooltip.wm_geometry(f"+{x}+{y}")

            label = tk.Label(
                tooltip,
                text=text,
                bg="#ffffe0",
                fg="black",
                relief="solid",
                borderwidth=1,
                font=("Arial", 9)
            )
            label.pack()
        
        def hide_tooltip(event):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def _update_status(self):
        """ Aktualisiert die Statusleiste mit aktuellen Statistiken """
        stats = self.week_manager.get_statistics()
        self.status_label.config(text=f"{stats['tasks_gesamt']} Aufgaben | {stats['tasks_erledigt']} erledigt | {stats['goals_erreicht']} Ziele erreicht")

    def _create_hover_effect(self, button, normal_color, hover_color):
        """
        Fügt einem Button einen Hover-Effekt hinzu.
        
        Args:
            button: Der Button, der den Effekt bekommen soll
            normal_color: Die normale Hintergrundfarbe
            hover_color: Die Farbe beim Hovern
        """
        button.bind("<Enter>", lambda e: button.config(bg=hover_color), add=True)
        button.bind("<Leave>", lambda e: button.config(bg=normal_color), add=True)

