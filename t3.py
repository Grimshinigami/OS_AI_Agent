import uiautomation as automation
import time

# while True:
#     # Get the currently focused window
#     focused_element = automation.GetFocusedControl()

#     # Print the name and control type of the focused element
#     print(f"Name: {focused_element.Name}")
#     print(f"Control Type: {focused_element.ControlTypeName}")
#     time.sleep(1)

def list_ui_elements(control, depth=0, filter_type=["Button"]):
    # if control.ControlTypeName in filter_type:
    #     print(f"{' ' * depth}Name: {control.Name}, Control Type: {control.ControlTypeName}")
    print(f"{' ' * depth}Name: {control.Name}, Control Type: {control.ControlTypeName}")
    
    for child in control.GetChildren():
        list_ui_elements(child, depth + 4, filter_type)

# active_window = automation.GetForegroundControl()

# Only list buttons in the active window
# list_ui_elements(active_window, filter_type=["Button"])


while True:
    active_window = automation.GetForegroundControl()
    list_ui_elements(active_window, filter_type=["Button","ComboBoxControl"])
    print("\n\n\n\n")
    time.sleep(5)