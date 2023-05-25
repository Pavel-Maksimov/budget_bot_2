BACK_BUTTON = "⇦"


def create_keyboard(columns, buttons):
    """
    Create a custom keybord with specified buttons.
    Return it as list of list of strings.
    """
    keyboard = []
    keyboard.append([BACK_BUTTON])
    keyboard[0].extend([buttons[i] for i in range(min(columns - 1, len(buttons)))])
    idx = columns - 1
    while idx < len(buttons):
        left = idx
        idx += columns
        row = [buttons[i] for i in range(left, min(idx, len(buttons)))]
        keyboard.append(row)
    return keyboard
