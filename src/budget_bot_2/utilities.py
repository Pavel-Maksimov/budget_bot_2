def create_keyboard(columns: int, buttons: list[str]) -> list[list[str]]:
    """
    Create a custom keybord with specified buttons.
    Return it as list of list of strings.
    """
    keyboard = []
    idx = 0
    while idx < len(buttons):
        left = idx
        idx += columns
        row = [buttons[i] for i in range(left, min(idx, len(buttons)))]
        keyboard.append(row)
    return keyboard
