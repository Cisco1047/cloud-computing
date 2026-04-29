import csv
import json
import math

# --- CONFIGURATION ---
CSV_FILE = 'quotes.csv'
TABLE_NAME = 'Fortunes'  # Replace with your EXACT DynamoDB table name
STARTING_ID = 7
MAX_ITEMS_PER_BATCH = 25 # DynamoDB hard limit

def generate_dynamodb_batches():
    try:
        # 1. Read the quotes from the CSV
        with open(CSV_FILE, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Grabs the first column, ignores empty lines
            quotes = [row[0].strip() for row in reader if row and row[0].strip()]

    except FileNotFoundError:
        print(f"Error: Could not find {CSV_FILE}. Make sure it is in the same folder.")
        return

    print(f"Found {len(quotes)} quotes. Generating JSON files...")

    # 2. Loop through the quotes in chunks of 25
    for i in range(0, len(quotes), MAX_ITEMS_PER_BATCH):
        chunk = quotes[i : i + MAX_ITEMS_PER_BATCH]
        batch_items = []

        # 3. Format each quote into DynamoDB JSON
        for index, quote in enumerate(chunk):
            current_id = STARTING_ID + i + index

            item = {
                "PutRequest": {
                    "Item": {
                        "id": { "S": str(current_id) },
                        "fortune": { "S": quote }
                    }
                }
            }
            batch_items.append(item)

        # 4. Wrap in the Table Name requirement
        dynamodb_json = {
            TABLE_NAME: batch_items
        }

        # 5. Save the file (e.g., batch_1.json, batch_2.json)
        file_number = math.ceil(i / MAX_ITEMS_PER_BATCH) + 1
        output_filename = f'batch_{file_number}.json'

        with open(output_filename, 'w', encoding='utf-8') as outfile:
            json.dump(dynamodb_json, outfile, indent=2, ensure_ascii=True)

        print(f"✔️ Created {output_filename} (Contains {len(chunk)} items. IDs: {STARTING_ID + i} to {STARTING_ID + i + len(chunk) - 1})")

    print("\nDone! You can now run the AWS CLI commands on these files.")

# Run the function
if __name__ == "__main__":
    generate_dynamodb_batches()