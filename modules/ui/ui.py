import tkinter as tk
from modules.database.db_client import DbJobClient
from modules.models.job_models import EJobState, JobApplication
import webbrowser

def _open_link(link: str):
    webbrowser.open(link)  # Go to example.com

def _copy_to_clipboard(text: str, t: tk.Tk):
    t.clipboard_clear()
    t.clipboard_append(text)
    t.update()


class WindowObject:

    def mark_applied_job_as_ready(self):
        for job in self.database.get_all_jobs_by_state(EJobState.APPLIED):
            self.database.set_job_state(job.id, EJobState.READY)

    def __init__(self, database: DbJobClient) -> None:
        self.root = tk.Tk(baseName="nombre")
        self.root.geometry("600x400")
        self.offset = 0
        self.database = database

        self.mark_applied_job_as_ready()
        
        # Área de información
        self.job_frame = tk.Frame(self.root, bd=2, relief="solid")
        self.job_frame.pack(fill="x", padx=10, pady=10)

        self.job_display = tk.Label(self.job_frame, text="Nombre: Shyne")
        self.job_display.pack()

        self.id_label = tk.Label(self.job_frame, text="ID")
        self.id_label.pack()
        
        self.url_btn = tk.Button(self.job_frame, text="Job")
        self.url_btn.pack()

        self.hiring_message = tk.Button(self.job_frame, text="Hiring message")
        self.hiring_message.pack()

        self.cover_letter = tk.Button(self.job_frame, text="Cover Letter")
        self.cover_letter.pack()

        self.salary_range = {
            "min" : tk.Label(self.job_frame, text="Min"),
            "max" : tk.Label(self.job_frame, text="Max"),
        }

        self.salary_range["min"].pack()
        tk.Label(self.job_frame, text="-").pack()
        self.salary_range["max"].pack()
        self.salary_currency = tk.Label(self.job_frame, text="Currency")
        self.salary_currency.pack()


        self.score = tk.Label(self.job_frame, text="Score")
        self.score.pack()

        # Otra área
        self.app_frame = tk.Frame(self.root, bd=2, relief="solid")
        self.app_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.applied = tk.Button(self.app_frame, text="Applied")
        self.applied.pack()

        self.revisit = tk.Button(self.app_frame, text="Revisit")
        self.revisit.pack()

        tk.Button(self.app_frame, text="Siguiente", command=lambda: self._modify_offset(+1)).pack(pady=5)
        tk.Button(self.app_frame, text="Anterior",  command=lambda: self._modify_offset(-1)).pack(pady=5)

    def update(self):
        self.build(self.database.get_ready_job(self.offset))

    def _modify_offset(self, value: int | None):
        self.offset += value if value is not None else 0
        limit_offset = self.database.get_num_ready_jobs() - 1
        self.offset = 0 if self.offset < 0 else limit_offset if self.offset > limit_offset else self.offset
        self.update()

    def build(self, app: JobApplication):

        self.id_label.configure(text=app.id)

        self.url_btn.configure(command=lambda : _open_link(app.job.url))
        self.job_display.configure(text=f"{app.job.role} at {app.job.company}")

        self.hiring_message.configure(command=lambda: _copy_to_clipboard(str(app.hiring_manager), self.root))
        self.cover_letter.configure(command=lambda: _copy_to_clipboard(str(app.cover_letter), self.root))
        
        self.salary_range["min"].configure(text=str(app.salary.minimum) if app.salary is not None else "Unknown")
        self.salary_range["max"].configure(text=str(app.salary.maximum) if app.salary is not None else "Unknown")
        
        self.salary_currency.configure(text=str(app.salary.currency) if app.salary is not None else "Unknown")

        if app.score is not None:
            self.score.configure(text=f"{app.score:1}/100")
        else:
            self.score.configure(text=f"?/100")
        
        def _set_job_state(self, state: EJobState):
            self.database.set_job_state(app.id, state)
            self.update()

        self.applied.configure(command=lambda: _set_job_state(self, EJobState.APPLIED))
        self.revisit.configure(command=lambda: _set_job_state(self, EJobState.PARSED))

    def run(self):
        self.build(self.database.get_ready_job(self.offset))
        self.root.mainloop()

    