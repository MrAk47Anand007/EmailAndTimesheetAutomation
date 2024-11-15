import json
from typing import Dict, Any


def load_json(file_path: str) -> Dict[str, Any]:
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def filter_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Filter and clean the email data."""
    filtered_data = {"value": []}

    for email in data.get("value", []):
        filtered_email = {
            "subject": email.get("subject", ""),
            "body": email.get("body", ""),
            "bodyPreview": email.get("bodyPreview", "")
        }

        # Only include emails with non-empty required fields
        if filtered_email["subject"] and (filtered_email["body"] or filtered_email["bodyPreview"]):
            filtered_data["value"].append(filtered_email)

    return filtered_data


def export_json(data: Dict[str, Any], output_file_path: str) -> None:
    """Export filtered JSON data to a file."""
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    input_file = 'input.json'
    output_file = 'output.json'

    try:
        # Load and process data
        data = load_json(input_file)
        filtered_data = filter_data(data)
        export_json(filtered_data, output_file)
        print(f"Successfully filtered data and saved to {output_file}")

    except Exception as e:
        print(f"Error processing data: {str(e)}")


if __name__ == "__main__":
    main()
