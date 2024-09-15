import uiautomation as automation
import json
import time

# Function to recursively list UI elements and store them in a list
def list_ui_elements_to_dict(control, depth=0):
    element_dict = {
        "name": control.Name,
        "control_type": control.ControlTypeName,
        "children": []
    }
    
    # Recursively process children
    for child in control.GetChildren():
        element_dict["children"].append(list_ui_elements_to_dict(child, depth + 4))
    
    return element_dict

# Get the active window
# active_window = automation.GetRootControl()

# while True:
time.sleep(5)

# while True:

active_window = automation.GetForegroundControl()

# Create a dictionary for the active window
ui_elements_dict = {
    "name": active_window.Name,
    "control_type": active_window.ControlTypeName,
    "children": []
}

# Populate the dictionary with UI elements

ui_elements_dict["children"] = [list_ui_elements_to_dict(child) for child in active_window.GetChildren()]

# Save the dictionary as a JSON file
# with open("ui_elements.json", "w") as json_file:
    # json.dump(ui_elements_dict, json_file, indent=4)
json_object = json.dumps(ui_elements_dict, indent=2)

# print("UI elements saved to ui_elements.json")

print("JSON Object is: \n",json_object)

# print(len(json_object))