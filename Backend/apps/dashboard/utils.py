import csv
import json

def get_device_datapoints_from_csv(csv_file):
    try:
        with open(csv_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            label_column = None
            for column in reader.fieldnames:
                if column.strip().lower() == 'label':
                    label_column = column
                    break
            if label_column is None:
                print("Label column not found.")
                return

            label_counts = {}
            total_labels = 0
            for row in reader:
                label = row[label_column].strip()
                if label:
                    total_labels += 1
                    if label in label_counts:
                        label_counts[label] += 1
                    else:
                        label_counts[label] = 1

            label_percentages = {label: round((count / total_labels) * 100, 1) for label, count in label_counts.items()}

            # Remove the "label" key from the dictionary
            if 'label' in label_percentages:
                del label_percentages['Label']

            # Convert the dictionary to the required format
            output = []
            for label, percentage in label_percentages.items():
                if label == 'Label':
                    continue
                output.append({'y': percentage, 'name': label})

            return(output)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

