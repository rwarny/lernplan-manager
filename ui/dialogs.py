import tkinter as tk
from tkinter import ttk, messagebox
from constants import KATEGORIEN, WOCHENTAGE, ZEITSLOTS, COLORS, FONT_SIZES
from models.task import Task
from models.goal import Goal

class TaskDialog:
    """ Dialog zum Erstellen oder Bearbeiten einer Aufgabe. """
    def __init__(self, parent, week_manager, wochentag="", zeitslot="", task=None, on_save=None):
        """ 
        Öffnet den Task-Dialog.
        
        Args:
            parent: Das übergeordnete Fenster
            week_manager: Der WeekManager
            wochentag: Vorausgewählter Wochentag
            zeitslot: Vorausgewählter Zeitslot
            task: Existierender Task zum Bearbeiten (None = neuer Task)
            on_save: Callback-Funktion nach dem Speichern"""
        
        self.week_manager = week_manager
        self.task = task
        self.on_save = on_save
        
        # Dialog-Fenster erstellen
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Neue Aufgabe" if task is None else "Aufgabe bearbeiten")
        self.dialog.geometry("400x400")
        self.dialog.configure(bg=COLORS['bg'])
        self.dialog.grab_set() # Modal machen

        # Formular erstellen
        self._create_form(wochentag, zeitslot)

    def _create_form(self, wochentag, zeitslot):
        """ Erstellt das Eingabeformular """
        # Titel
        tk.Label(self.dialog, text="Titel:", bg=COLORS['bg'], fg=COLORS['fg']).pack(pady=(10,0))
        self.titel_entry = tk.Entry(self.dialog, width=40)
        self.titel_entry.pack(pady=5)

        # Kategorie
        tk.Label(self.dialog, text="Kategorie:", bg=COLORS['bg'], fg=COLORS['fg']).pack(pady=(10,0))
        self.kategorie_combo = ttk.Combobox(self.dialog, values=list(KATEGORIEN.keys()), state="readonly")
        self.kategorie_combo.pack(pady=5)
        self.kategorie_combo.current(0)
        
        # Wochentag
        tk.Label(self.dialog, text="Wochentag:", bg=COLORS["bg"], fg=COLORS["fg"]).pack(pady=(10, 0))
        self.wochentag_combo = ttk.Combobox(self.dialog, values=WOCHENTAGE, state="readonly")
        self.wochentag_combo.pack(pady=5)
        if wochentag in WOCHENTAGE:
            self.wochentag_combo.set(wochentag)
        else:
            self.wochentag_combo.current(0)
        
        # Zeitslot
        tk.Label(self.dialog, text="Zeitslot:", bg=COLORS["bg"], fg=COLORS["fg"]).pack(pady=(10, 0))
        self.zeitslot_combo = ttk.Combobox(self.dialog, values=ZEITSLOTS, state="readonly")
        self.zeitslot_combo.pack(pady=5)
        if zeitslot in ZEITSLOTS:
            self.zeitslot_combo.set(zeitslot)
        else:
            self.zeitslot_combo.current(0)
        
        # Beschreibung
        tk.Label(self.dialog, text="Beschreibung:", bg=COLORS["bg"], fg=COLORS["fg"]).pack(pady=(10, 0))
        self.beschreibung_text = tk.Text(self.dialog, width=40, height=3)
        self.beschreibung_text.pack(pady=5)

        if self.task:
            self.titel_entry.insert(0, self.task.titel)
            self.kategorie_combo.set(self.task.kategorie)
            self.wochentag_combo.set(self.task.wochentag)
            self.zeitslot_combo.set(self.task.zeitslot)
            self.beschreibung_text.insert("1.0", self.task.beschreibung)
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg=COLORS["bg"])
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Speichern", bg=COLORS['button2'], fg=COLORS['fg'], command=self._save).pack(side="left", padx=10)
        tk.Button(button_frame, text="Abbrechen", bg=COLORS['button3'], fg=COLORS['fg'],command=self.dialog.destroy).pack(side="left", padx=10)

    def _save(self):
        """ Speichert den Task und schließt den Dialog """
        # Werte aus Formular holen
        titel = self.titel_entry.get()
        kategorie = self.kategorie_combo.get()
        wochentag = self.wochentag_combo.get()
        zeitslot = self.zeitslot_combo.get()
        beschreibung = self.beschreibung_text.get("1.0", "end-1c").strip()

        # Validierung: Titel darf nicht leer sein
        if not titel:
            messagebox.showwarning("FEHLER", "Bitte einen Titel eingeben!")
            return
        
        # Prüfen ob wir einen bestehenden Task bearbeiten oder einen neuen erstellen
        if self.task:
            # Bestehenden Task aktualisieren
            self.task.titel = titel
            self.task.kategorie = kategorie
            self.task.wochentag = wochentag
            self.task.zeitslot = zeitslot
            self.task.beschreibung = beschreibung

            # Auto-Save auslösen
            if self.week_manager.auto_save_callback:
                self.week_manager.auto_save_callback()
        
        else:
            # Neuen Task erstellen
            task = Task(
                titel=titel,
                kategorie=kategorie,
                wochentag=wochentag,
                zeitslot=zeitslot,
                beschreibung=beschreibung
            )

            # Task hinzufügen
            self.week_manager.add_task(task)

        # Callback aufrufen (z.B. View aktuelisieren)
        if self.on_save:
            self.on_save()

        # Dialog schließen
        self.dialog.destroy()

class GoalDialog:
    """ Dialog zum Erstellen oder Bearbeiten eines neuen Ziels. """
    def __init__(self, parent, week_manager, goal=None, on_save=None):
        """
        Öffnet den Goal-Dialog.

        Args:
            parent: Das übergeordnete Fenster.
            week_manager: Der WeekManager.
            goal: Existierendes Goal zum Bearbeiten (None = neues Goal)
            on_save: Callback-Funktion nach dem Speichern.
        """
        self.parent = parent
        self.week_manager = week_manager
        self.goal = goal
        self.on_save = on_save

        # Dialog-Fenster erstellen
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Neues Ziel")
        self.dialog.geometry("300x300")
        self.dialog.configure(bg=COLORS['bg'])
        self.dialog.grab_set() # Modal machen

        # Formular erstellen
        self._create_form()

    def _create_form(self):
        """Erstellt das Eingabeformular."""
        # Titel
        tk.Label(self.dialog, text="Titel:", bg=COLORS['bg'], fg=COLORS['fg']).pack(pady=(10, 0))
        self.titel_entry = tk.Entry(self.dialog, width=40)
        self.titel_entry.pack(pady=5)
        
        # Kategorie
        tk.Label(self.dialog, text="Kategorie:", bg=COLORS['bg'], fg=COLORS['fg']).pack(pady=(10, 0))
        self.kategorie_combo = ttk.Combobox(self.dialog, values=list(KATEGORIEN.keys()), state="readonly")
        self.kategorie_combo.pack(pady=5)
        self.kategorie_combo.current(0)
        
        # Ziel-Anzahl
        tk.Label(self.dialog, text="Ziel-Anzahl:", bg=COLORS['bg'], fg=COLORS['fg']).pack(pady=(10, 0))
        self.anzahl_spinbox = tk.Spinbox(self.dialog, from_=1, to=20, width=5)
        self.anzahl_spinbox.pack(pady=5)

        # Falls ein bestehendes Ziel bearbeitet wird, Felder vorausfüllen
        if self.goal:
            self.titel_entry.insert(0, self.goal.titel)
            self.kategorie_combo.set(self.goal.kategorie)
            self.anzahl_spinbox.delete(0, "end")
            self.anzahl_spinbox.insert(0, self.goal.ziel_anzahl)
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg=COLORS['bg'])
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Speichern",  bg=COLORS['button2'], fg=COLORS['fg'], command=self._save).pack(side="left", padx=10)
        tk.Button(button_frame, text="Abbrechen",  bg=COLORS['button3'], fg=COLORS['fg'], command=self.dialog.destroy).pack(side="left", padx=10)
    
    def _save(self):
        """Speichert das Ziel und schließt den Dialog."""
        # Werte holen
        titel = self.titel_entry.get()
        kategorie = self.kategorie_combo.get()
        ziel_anzahl = int(self.anzahl_spinbox.get())
        
        # Validierung
        if not titel:
            messagebox.showwarning("Fehler", "Bitte einen Titel eingeben!")
            return
        
        if self.goal:
            # Bestehendes Ziel aktualisieren
            self.goal.titel = titel
            self.goal.kategorie = kategorie
            self.goal.ziel_anzahl = ziel_anzahl

            # Auto-Save auslösen
            if self.week_manager.auto_save_callback:
                self.week_manager.auto_save_callback()

        else:
            # Goal erstellen
            goal = Goal(
                titel=titel,
                kategorie=kategorie,
                ziel_anzahl=ziel_anzahl
            )
            
            # Goal hinzufügen
            self.week_manager.add_goal(goal)
        
        # Callback aufrufen
        if self.on_save:
            self.on_save()
        
        # Dialog schließen
        self.dialog.destroy()

        