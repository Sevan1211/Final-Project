import csv
from typing import Dict, Set, Tuple
import tkinter as tk

def submit_vote(selected_candidate: str, voter_id: str, candidates: Dict[str, int], voted_ids: Set[str]) -> str:
    if not selected_candidate:
        return "Please select a candidate."

    if not voter_id:
        return "Please enter a voter ID."

    if voter_id in voted_ids:
        return "You have already voted."

    try:
        with open('voting_results.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0] == voter_id:
                    return "You have already voted."
    except FileNotFoundError:
        pass

    with open('voting_results.csv', 'a', newline='') as csvfile:
        fieldnames = ['VoterID', 'Candidate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow({'VoterID': voter_id, 'Candidate': selected_candidate})

    voted_ids.add(voter_id)

    candidates[selected_candidate] += 1


def show_warning(message: str, warning_label: tk.Label) -> None:
    warning_label.config(text=message)

def clear_vote(vote_var: tk.StringVar, voter_id_entry: tk.Entry, warning_label: tk.Label) -> None:
    vote_var.set("")
    voter_id_entry.delete(0, 'end')
    warning_label.config(text="")


def get_all_votes(filename: str) -> Tuple[Dict[str, int], int]:
    candidates_votes = {}
    total_votes = 0

    try:
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                if row:
                    candidate = row[1]  # Candidate's name is in the second column
                    candidates_votes[candidate] = candidates_votes.get(candidate, 0) + 1
                    total_votes += 1
    except FileNotFoundError:
        pass

    return candidates_votes, total_votes

def show_results(filename: str) -> str:
    candidates_votes, total_votes = get_all_votes(filename)

    result_message = "Voting Results:\n"
    for candidate, votes in candidates_votes.items():
        percentage = (votes / total_votes) * 100 if total_votes > 0 else 0
        result_message += f"{candidate}: {votes} votes ({percentage:.2f}%)\n"
    result_message += f"Total Votes: {total_votes}"

    return result_message
