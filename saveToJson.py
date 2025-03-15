import json
import os

def write_json(new_data):
    file_path = r".\DataBase\DataBase.json"
    
    # Create file with default structure if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump({"DataBase": []}, file)
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                file_data = json.load(file)
            except json.JSONDecodeError:
                file_data = {"DataBase": []}
    except Exception as e:
        print(f"Error reading file: {e}")
        file_data = {"DataBase": []}
    
    # Ensure notifications key exists
    if "DataBase" not in file_data:
        file_data["DataBase"] = []
    
    file_data["DataBase"].append(new_data)
    
    # Write updated data
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(file_data, file, indent=4)
        print("Data successfully saved")
    except Exception as e:
        print(f"Error writing file: {e}")