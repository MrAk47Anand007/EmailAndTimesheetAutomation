import json
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Task:
    date: str
    task_name: str
    description: str
    time_spent: float


class EmailProcessor:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def parse_time(self, time_str: str) -> float:
        """Convert time string to hours."""
        try:
            return float(time_str)
        except ValueError:
            return 0.0

    def extract_table_data(self, html: str) -> List[Dict[str, str]]:
        """Extract data from HTML table, excluding the date column after the first row."""
        soup = BeautifulSoup(html, 'html.parser')
        tasks = []

        # Find the main task table
        table = soup.find('table', {'id': 'table_0'})
        if not table:
            return tasks

        # Get the date from the first cell in the first row (header row)
        rows = table.find_all('tr')
        first_row_cells = rows[1].find_all('td')
        date = first_row_cells[0].get_text(strip=True)

        # Process rows excluding the date column in subsequent rows
        for i, row in enumerate(rows[1:], start=1):
            # Skip header and date row

            cols = row.find_all(['td', 'th'])
            if len(cols) >= 3:  # Ensure we have enough columns
                task = {
                    'task_name': cols[1].get_text(strip=True) if i == 1 else cols[0].get_text(strip=True),
                    'description': cols[2].get_text(strip=True) if i == 1 else cols[1].get_text(strip=True),
                    'time_spent': self.parse_time(cols[3].get_text(strip=True)) if i == 1 else self.parse_time(
                        cols[2].get_text(strip=True))
                }
                tasks.append(task)

        return [{'date': date, 'tasks': tasks}]

    def process_emails(self) -> None:
        """Process emails and generate structured output."""
        try:
            # Load input data
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            structured_data = []

            for email in data.get('value', []):
                email_data = {
                    'subject': email.get('subject', ''),
                    'tasks': []
                }

                # Extract tasks from email body
                if email.get('body'):
                    tasks = self.extract_table_data(email['body'])
                    email_data['tasks'] = tasks
                    structured_data.append(email_data)

            # Save structured data
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, indent=4, ensure_ascii=False)

            print(f"Successfully processed emails and saved to {self.output_file}")

        except Exception as e:
            print(f"Error processing emails: {str(e)}")


def main():
    processor = EmailProcessor('output.json', 'structured_emails.json')
    processor.process_emails()


if __name__ == "__main__":
    main()
