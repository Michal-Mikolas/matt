# Matt

Matt is a Python library for UI automation and testing. It serves as a robust wrapper around `pyautogui`, providing enhanced functionality for image-based element lookup, region caching for performance optimization, OCR capabilities, and a simplified API for interacting with UI elements.

## Features

-   **Image-based UI Lookup:** Define UI elements using image files.
-   **Performance Optimization:** Caches the last known location of UI elements to speed up subsequent searches.
-   **Resilience:** specific methods to wait for elements to appear.
-   **OCR Support:** Built-in optical character recognition using `pytesseract`.
-   **Simplified API:** Easy-to-use methods for clicking, typing, and moving the mouse.

## Quickstart

### 1. Installation

Import Matt as a [git submodule](https://www.atlassian.com/git/tutorials/git-submodule):

```sh
git submodule add https://github.com/Michal-Mikolas/matt.git
```

### 2. Basic Usage

```python
from matt.matt import Matt

# Initialize Matt
matt = Matt(
    cache_file='cache/matt.json'
)

# Define UI elements (name -> image path)
matt.set_ui({
    'start_button': 'images/start.png',
    'settings_icon': ['images/settings.png', 'images/settings_hover.png'], # Can provide multiple images for one element
})

# Interact with the UI
matt.click('start_button')
matt.wait('settings_icon')
matt.click('settings_icon')
```

## API Reference & Examples

### `set_ui(ui)`

Sets the dictionary of UI elements.

```python
matt.set_ui({
    'submit_btn': 'assets/submit.png',
    'cancel_btn': 'assets/cancel.png'
})
```

### `wait(ui, timeout=None, step=0.1)`

Waits for a UI element to appear on the screen. Returns the center coordinates.

```python
# Wait for the submit button to appear
pos = matt.wait('submit_btn', timeout=10)
print(f"Button found at: {pos}")
```

### `which(*args, timeout=None, step=0.1)`

Waits for *any one* of the specified UI elements to appear. Useful for handling conditional popups or different states.

```python
# Wait for either 'login_success' or 'login_error'
element, pos = matt.which('login_success', 'login_error')

if element == 'login_success':
    print("Logged in successfully!")
else:
    print("Login failed.")
```

### `click(ui=None, x=0, y=0, timeout=None)`

Clicks on a UI element. If `ui` is None, clicks at the current mouse position.

```python
# Click the submit button
matt.click('submit_btn')

# Click at the current position
matt.click()

# Click 10 pixels to the right of the center of the element
matt.click('submit_btn', x=10)
```

### `double_click(ui=None, x=0, y=0, timeout=None)`

Double-clicks on a UI element.

```python
matt.double_click('desktop_icon')
```

### `right_click(ui=None, x=0, y=0, timeout=None)`

Right-clicks on a UI element.

```python
matt.right_click('item_row')
```

### `move_to(ui, x=0, y=0, timeout=None)`

Moves the mouse cursor to a UI element.

```python
matt.move_to('hover_menu')
```

### `hotkey(*args, **kwargs)`

Presses a hotkey combination.

```python
matt.hotkey('ctrl', 'c')
matt.hotkey('alt', 'tab')
```

### `typewrite(message, interval=0.0)`

Types a message string.

```python
matt.typewrite('Hello World!', interval=0.1)
```

### `mouse_down()` / `mouse_up()`

Holds or releases the mouse button.

```python
matt.move_to('drag_start')
matt.mouse_down()
matt.move_to('drag_end')
matt.mouse_up()
```

### `screenshot(filename=None, region=None)`

Takes a screenshot.

```python
# Save full screen screenshot
matt.screenshot('myscreen.png')

# Get screenshot object for a specific region
img = matt.screenshot(region=(0, 0, 300, 400))
```

### `ocr(region=None)`

Performs OCR on the screen or a specific region. Returns text with non-digits removed (based on current implementation).

```python
# Read numbers from a specific region
text = matt.ocr(region=(100, 100, 200, 50))
print(text)
```

### `select(region)`

Selects a region by dragging the mouse from top-left to bottom-right of the region.

```python
# Select a 100x100 square starting at 50,50
matt.select((50, 50, 100, 100))
```

### `copy()`

Performs a copy operation (`Ctrl+C`) and returns the clipboard content.

```python
# Select text then copy it
matt.select((100, 100, 200, 20))
text = matt.copy()
print(text)
```
