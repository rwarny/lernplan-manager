from datetime import datetime 
from models.goal import Goal
from models.task import Task

class WeekManager:
    """ Verwaltet alle Tasks und Goals einer Woche """
    def __init__(self):
        """ Initialisiert einen neuen WeekManager für die aktuelle Woche. """
        self.tasks = []
        self.goals = []
        self.next_task_id = 1
        self.next_goal_id = 1
        self.wochennummer = datetime.now().isocalendar()[1]
        self.jahr = datetime.now().year
        self.auto_save_callback = None

    def add_task(self, task):
        """
        Fügt eine neue Aufgabe hinzu.

        Args:
            task: Das Task-Objekt, das hinzugefügt werden soll
        """
        task.id = self.next_task_id
        self.next_task_id += 1
        self.tasks.append(task)
        if self.auto_save_callback:
            self.auto_save_callback()

    def remove_task(self, task_id):
        """
        Entfernt eine Aufgabe anhand ihrer ID

        Args:
            task_id: Die ID der zu entfernenden Aufgabe
        """
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                break

        if self.auto_save_callback:
            self.auto_save_callback()

    def get_tasks_by_day(self, wochentag):
        """
        Gibt alle Aufgaben für einen bestimmten Wochentag zurück.

        Args:
            wochentag: Der Wochentag (z.B. "Montag")

        Returns:
            list: Liste aller Tasks an diesem Tag
        """
        ergebnisse = []
        for task in self.tasks:
            if task.wochentag == wochentag:
                ergebnisse.append(task)

        return ergebnisse
    
    def get_tasks_by_timeslot(self, wochentag, zeitslot):
        """
        Gibt alle Aufgaben für einen bestimmten Wochentag und Zeitslot zurück
        
        Args:
            wochentag: Der Wochentag (z.B. "Montag")
            zeitslot: Die Uhrzeit (z.B. "10:00")

        Returns:
            list: Liste aller Tasks an diesem Tag und Zeitslot
        """
        ergebnisse = []
        for task in self.tasks:
            if task.wochentag == wochentag and task.zeitslot == zeitslot:
                ergebnisse.append(task)

        return ergebnisse
    
    def add_goal(self, goal):
        """ 
        Fügt ein neues Ziel hinzu.
        
        Args:
            goal: Das Goal Objekt- das hinzugefügt werden soll.
        """
        goal.id = self.next_goal_id
        self.next_goal_id += 1
        self.goals.append(goal)
        if self.auto_save_callback:
            self.auto_save_callback()
    
    def remove_goal(self, goal_id):
        """
        Entfernt ein Ziel anhand seiner ID.

        Args:
            goal_id: Die ID des zu entfernenden Ziels
        """
        for goal in self.goals:
            if goal.id == goal_id:
                self.goals.remove(goal)
                break
        if self.auto_save_callback:
            self.auto_save_callback()

    def get_goals_by_kategorie(self, kategorie):
        """
        Gibt alle Ziele für eine bestimmte Kategorie zurück.

        Args:
            kategorie: Die Kategorie. (z.B. "Anw.P")

        Returns:
            list: Liste aller Ziele in dieser Kategorie
        """
        ergebnisse = []
        for goal in self.goals:
            if goal.kategorie == kategorie:
                ergebnisse.append(goal)

        return ergebnisse
    
    def get_statistics(self):
        """
        Berechnet Statistiken für die aktuelle Woche.

        Returns:
            dict: Dictionary mit verschiedenen Statistiken
        """
        # Einfache Zählungen
        tasks_gesamt = len(self.tasks)
        goals_gesamt = len(self.goals)

        # Erledigte Tasks zählen
        tasks_erledigt = 0
        for task in self.tasks:
            if task.erledigt:
                tasks_erledigt += 1

        # offenen Tasks berechnen
        tasks_offen = tasks_gesamt - tasks_erledigt

        # Erledigungs-Rate berechnen
        if tasks_gesamt > 0:
            erledigungs_rate = round((tasks_erledigt / tasks_gesamt) * 100, 1)
        else:
            erledigungs_rate = 0.0

        # Erreichte Goals zählen
        goals_erreicht = 0
        for goal in self.goals:
            if goal.is_completed():
                goals_erreicht += 1

        # Tasks pro Kategorie zählen
        tasks_pro_kategorie = {}
        for task in self.tasks:
            kategorie = task.kategorie
            if kategorie in tasks_pro_kategorie:
                tasks_pro_kategorie[kategorie] += 1
            else:
                tasks_pro_kategorie[kategorie] = 1

        return {
            "tasks_gesamt": tasks_gesamt,
            "tasks_erledigt": tasks_erledigt,
            "tasks_offen": tasks_offen,
            "erledigungs_rate": erledigungs_rate,
            "goals_gesamt": goals_gesamt,
            "goals_erreicht": goals_erreicht,
            "tasks_pro_kategorie": tasks_pro_kategorie
        }