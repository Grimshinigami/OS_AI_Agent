import uiautomation as automation
import time

# Define a recursive function to find an element by its name or control type and click it
def see_through_elements(control, target_name=None, target_control_type=None):
    # if target_name and control.Name == target_name:
    if target_name and target_name in control.Name:
        print(f"Found: {control.Name}, Control Type: {control.ControlTypeName} -> Clicking it.")
        control.Click()
        return True
    if target_control_type and control.ControlTypeName == target_control_type:
        print(f"Found: {control.Name}, Control Type: {control.ControlTypeName} -> Clicking it.")
        control.Click()
        return True

    # Recursively search for the element
    for child in control.GetChildren():
        if see_through_elements(child, target_name, target_control_type):
            return True
    return False

def find_and_click_element(target_name):

    # Get the current active window
    active_window = automation.GetForegroundControl()

    # Print the active window's details
    print(f"Active Window: {active_window.Name}, Control Type: {active_window.ControlTypeName}")

    # Example: Try to find and click a button by its name or control type
    result = see_through_elements(active_window, target_name)  # Find by name
    # OR
    # find_and_click_element(active_window, target_control_type="Button")  # Find by control type

    if result:
        print("Element Found and Clicked Successfully")
    else:
        print("Couldn't Find Element")

time.sleep(5)
# find_and_click_element("Address and search bar")
find_and_click_element("The Hindu Protesting doctors visit Mamata Banerjee, but impasse over streaming continues 5 hours ago")