# Custom Python Web Browser

A simple web browser built using Python and PyQt5 with basic functionalities such as navigation, bookmarking, history, private browsing, and zoom control.

## Features

- **Navigation**: Back, forward, reload.
- **Address Bar**: Enter URLs to navigate to websites.
- **Zoom Control**: Zoom in and zoom out functionality.
- **Bookmarks**: Add and view bookmarks.
- **History**: View browsing history.
- **Private Browsing**: Toggle private browsing mode.
- **Custom User Agent**: Set a custom user agent.
- **Ad Blocking**: Basic ad blocking setup (optional).

## Installation

### Prerequisites

- Python 3.7 or higher
- `pipenv` for managing virtual environments

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/custom-python-web-browser.git
    cd custom-python-web-browser
    ```

2. Create and activate a virtual environment using `pipenv`:

    ```bash
    pip install pipenv
    pipenv --python 3.10
    pipenv install
    pipenv shell
    ```

3. Install the required packages:

    ```bash
    pipenv install PyQt5 PyQtWebEngine
    ```

4. Run the application:

    ```bash
    python main.py
    ```

## Usage

- **Back**: Navigate to the previous page.
- **Forward**: Navigate to the next page.
- **Reload**: Reload the current page.
- **Address Bar**: Enter the URL and press Enter to navigate.
- **Zoom In**: Increase the zoom level of the page.
- **Zoom Out**: Decrease the zoom level of the page.
- **Bookmark**: Add the current page to bookmarks.
- **History**: View browsing history.
- **Private Mode**: Toggle private browsing mode.

## Code Overview

### `main.py`

The main script that initializes and runs the web browser application. It sets up the UI, connects actions to buttons, and manages the browser's state.

#### Key Methods

- `__init__`: Sets up the main window, navigation bar, and connects signals.
- `setup_profile`: Configures the web engine profile for ad blocking and user agent.
- `navigate_to_url`: Navigates to the URL entered in the address bar.
- `update_url`: Updates the address bar with the current URL.
- `add_bookmark`: Adds the current page to bookmarks.
- `show_history`: Prints the browsing history.
- `toggle_private_mode`: Toggles private browsing mode.
- `zoom_in`: Increases the zoom level.
- `zoom_out`: Decreases the zoom level.
- `reload_page`: Reloads the current page.
- `apply_zoom_factor`: Applies the current zoom factor to the browser.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- PyQt5 documentation
- Stack Overflow community

