import json
import os
from models.task import Task
from models.goal import Goal
from managers.week_manager import WeekManager
from constants import ARCHIVE_FOLDER, WOCHENTAGE
from tkinter import messagebox

def save_week(week_manager, filename):
    """
    Speichert die aktuelle Woche als JSON-Datei.

    Args:
        week_manager: Der Weekmanager mit allen Daten
        filename: Name der Datei (z.B "current_week.json")
    """
    data = {
        "wochennummer": week_manager.wochennummer,
        "jahr": week_manager.jahr,
        "next_task_id": week_manager.next_task_id,
        "next_goal_id": week_manager.next_goal_id,
        "tasks": [task.to_dict() for task in week_manager.tasks],
        "goals": [goal.to_dict() for goal in week_manager.goals]
    }
    try: 
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except (IOError, OSError) as e:
        messagebox.showerror("Fehler", f"Die Datei '{filename}' konnte nicht gespeichert werden.\n\nBitte prüfe die Schreibrechte.")
        
def load_week(filename):
    """
    Lädt eine Woche aus einer JSON-Datei.

    Args:
        filename: Name der Datei
    
    Returns:
        WeekManager: Der geladene WeekManager, oder ein neuer falls Datei nicht existiert.
    """
    # Prüfen ob die Datei existiert
    if not os.path.exists(filename):
        return WeekManager()
    
    try:
        # Datei laden
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)


        # WeekManager erstellen und befüllen
        manager = WeekManager()
        manager.wochennummer = data["wochennummer"]
        manager.jahr = data["jahr"]
        manager.next_task_id = data["next_task_id"]
        manager.next_goal_id = data["next_goal_id"]

        # Tasks laden
        for task_data in data["tasks"]:
            task = Task.from_dict(task_data)
            manager.tasks.append(task)

        # Goals laden
        for goal_data in data["goals"]:
            goal = Goal.from_dict(goal_data)
            manager.goals.append(goal)

    except (json.JSONDecodeError, KeyError) as e:
        messagebox.showerror("Fehler", f"Die Datei '{filename}' konnte nicht geladen werden.\n\nEine neue Woche wird erstellt.")
        return WeekManager()

    return manager

def archive_week(week_manager):
    """
    Archiviert die aktuelle Woche und erstellt einen neuen WeekManager.
    
    Args:
        week_manager: Der aktuelle WeekManager
    
    Returns:
        WeekManager: Ein neuer, leerer WeekManager für nächste Woche.
    """
    # Archiv-Ordner erstellen
    os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

    filename = f"week_{week_manager.jahr}_W{week_manager.wochennummer:02d}.json"
    filepath = os.path.join(ARCHIVE_FOLDER, filename)

    # Speichern
    save_week(week_manager, filepath)

    # Neuen WeekManager zurückgeben
    return WeekManager()

def export_to_txt(week_manager, filename):
    """
    Exportiert die Woche als txt-Datei

    Args:
        week_manager: Der Weekmanager mit allen Daten
        filename: name der txt-Datei
    """
    trennlinie = 50 * "="

    text = f"{trennlinie}\n"
    text += f"WOCHENPLAN KW {week_manager.wochennummer} - {week_manager.jahr}\n"
    text += f"{trennlinie}\n\n"

    for tag in WOCHENTAGE:
        text += f"--- {tag} ---\n"
        tasks = week_manager.get_tasks_by_day(tag)
        if tasks:
            for task in tasks:
                status = "✓ Erledigt" if task.erledigt else "○ Offen"
                text += f"{task.zeitslot} | {task.titel} | {status}\n"
            text += "\n"
        else:
            text += "Keine Aufgaben\n\n"

    
    zielueberschrift = f"{trennlinie}\n"
    zielueberschrift += "ZIELE\n"
    zielueberschrift += f"{trennlinie}\n\n"

    
    text += zielueberschrift

    for goal in week_manager.goals:
        fertig = "✓" if goal.is_completed() else ""
        text += f"{goal.titel} ({goal.aktuell}/{goal.ziel_anzahl}) - {goal.get_progress()}% {fertig}\n"

    try:
        with open(filename, "w", encoding="utf-8") as datei:
            datei.write(text)

    except (IOError, OSError) as e:
        messagebox.showerror("FEHLER", f"Die datei '{filename}' konnte nicht exportiert werden.")
