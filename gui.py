import tkinter as tk
from logic import submit_vote, show_warning, clear_vote, show_results
from typing import Dict, Set

class VoteApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Voting App")
        self.geometry("400x350")
        self.resizable(False, False)

        self.candidates: Dict[str, int] = {"Bianca": 0, "Edward": 0, "Felicia": 0}
        self.voted_ids: Set[str] = set()

        self.create_widgets()

    def create_widgets(self) -> None:
        self.label_vote_menu = tk.Label(self, text="VOTE MENU", font=("Helvetica", 16, "bold"))
        self.label_vote_menu.pack(pady=10)

        self.vote_var = tk.StringVar()
        for candidate in self.candidates.keys():
            rb = tk.Radiobutton(self, text=candidate, variable=self.vote_var, value=candidate)
            rb.pack()

        self.label_voter_id = tk.Label(self, text="Enter Voter ID:")
        self.label_voter_id.pack()

        self.voter_id_entry = tk.Entry(self)
        self.voter_id_entry.pack()

        self.warning_label = tk.Label(self, text="", fg="red")
        self.warning_label.pack()

        self.clear_button = tk.Button(self, text="Clear", command=self.clear_vote)
        self.clear_button.pack()

        self.submit_button = tk.Button(self, text="Submit Vote", command=self.submit_vote)
        self.submit_button.pack(pady=10)

        self.results_button = tk.Button(self, text="Show Results", command=self.show_results)
        self.results_button.pack(pady=10)

    def submit_vote(self) -> None:
        selected_candidate: str = self.vote_var.get()
        voter_id: str = self.voter_id_entry.get()

        self.warning_label.config(text="")

        result_message: str = submit_vote(selected_candidate, voter_id, self.candidates, self.voted_ids)
        show_warning(result_message, self.warning_label)

        self.vote_var.set("")
        self.voter_id_entry.delete(0, tk.END)

    def clear_vote(self) -> None:
        clear_vote(self.vote_var, self.voter_id_entry, self.warning_label)

    def show_results(self):
        result_message = show_results('voting_results.csv')  # Pass the filename here
        results_window = tk.Toplevel(self)
        results_window.title("Voting Results")
        results_label = tk.Label(results_window, text=result_message)
        results_label.pack(padx=20, pady=20)
