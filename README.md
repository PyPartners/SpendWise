# SpendWise - Modern Expense Tracker 📊💸

SpendWise is a desktop application designed for personal income and expense tracking. Built with Python and PyQt5, it offers a clean, user-friendly interface with dynamic theming (Light/Dark) and multi-language support (English/Arabic).

## ✨ Features

*   **Core Transaction Management:** 📝
    *   **Add Transactions:** Users can add new income or expense records, specifying details like date, description, type (income/expense), amount, and category.
    *   **Edit Transactions:** Existing transactions can be modified to correct or update information.
    *   **Delete Transactions:** Unwanted transactions can be permanently removed.
*   **Data Persistence:** 💾
    *   All transaction data is stored locally in a `spendwise_data.json` file.
    *   This file is located in the standard application data directory for the user's operating system (e.g., `~/.local/share/SpendWiseOrg/SpendWise/` on Linux, `C:\Users\<User>\AppData\Local\SpendWiseOrg\SpendWise\` on Windows).
*   **Dashboard & Visualization:** 📈
    *   **Balance Summary:** The main window displays the current overall balance (Total Income - Total Expenses).
    *   **Expense Pie Chart:** A dynamic pie chart visualizes expense distribution by category for the selected filter period.
*   **Filtering & Sorting:** 🔍↕️
    *   **Date Range Filter:** Transactions can be filtered by a custom start and end date.
    *   **Category Filter:** Users can filter transactions to show records from a specific category or all categories.
    *   **Table Sorting:** The transaction table can be sorted by clicking on column headers (e.g., sort by date, amount).
*   **Customization & Theming:** 🎨⚙️
    *   **Light/Dark Themes:** Switch between a light ☀️ and dark 🌙 user interface theme. The selected theme is saved and applied on subsequent launches. The application uses a modern Teal color palette (`#4d99a6` as the primary accent).
    *   **Language Support:** 🌐
        *   Currently supports English 🇬🇧 and Arabic 🇸🇦.
        *   The application dynamically switches UI text and layout direction (Left-to-Right for English, Right-to-Left for Arabic) based on the selected language.
        *   Language preference is saved.
    *   **Currency Customization:** 💲
        *   **Predefined Currencies:** Select from a list of common currencies (e.g., USD, EUR, GBP, JPY, INR, SAR).
        *   **Language-Based Default:** Option to use the default currency symbol associated with the currently selected application language (e.g., "$" for English, "ر.س" for Arabic).
        *   **Custom Symbol:** Users can manually input their own currency symbol (e.g., "CAD", "د.ك").
        *   The chosen currency symbol is applied across all displays of monetary values and is saved for future sessions.
*   **User Interface & Experience:** 💻🤝
    *   **Modern Design:** Clean, intuitive, and responsive layout.
    *   **Splash Screen:** An elegant splash screen 🚀 is displayed during application startup.
    *   **About Dialog:** Provides information ℹ️ about the application, its version, and developer details.
    *   **Input Validation:** Forms for adding/editing transactions include input validation ✅ to ensure data integrity.
    *   **Logo Integration:** The application loads and displays a `logo.png` file (if present in `resources/app_icons/`). Fallback visuals are used if the logo is missing.
    *   **Status Bar:** Provides feedback to the user (e.g., "Ready", "Currency settings updated.").
*   **Cross-Platform (Potentially):** 🌍
    *   Built with PyQt5, a cross-platform framework, allowing the application to run on Windows, macOS, and Linux.

## 📂 Project Structure

The project is organized into several key directories and files:

*   `SpendWise/` (Main project directory)
    *   `spendwise/` (The main Python package)
        *   `__init__.py`
        *   `main.py` (Application entry point 🚪)
        *   `main_window.py` (Main UI 🖼️)
        *   `core/` (Core logic & data 🧠)
            *   `__init__.py`
            *   `transaction.py` (Transaction data model)
            *   `data_manager.py` (Data loading, saving, management)
        *   `widgets/` (Custom UI components 🧩)
            *   `__init__.py`
            *   `transaction_dialog.py`
            *   `statistics_dialog.py`
            *   `splash_screen.py`
            *   `about_dialog.py`
            *   `chart_widget.py`
        *   `utils/` (Utility classes 🛠️)
            *   `__init__.py`
            *   `translator.py` (Language translation)
            *   `theme_manager.py` (Theme management)
    *   `resources/` (Static assets 🖼️💄)
        *   `__init__.py`
        *   `app_icons/`
            *   `logo.png` (Application logo)
        *   `images.py` (Image path helper)
        *   `i18n/` (Internationalization files)
            *   `__init__.py`
            *   `translations.py` (UI strings)
        *   `styles/` (QSS theme files)
            *   `__init__.py`
            *   `light_theme.py`
            *   `dark_theme.py`
    *   `requirements.txt` (Python dependencies 📦)
    *   `README.md` (This file)

## 🚀 Setup and Running the Application

1.  **Prerequisites:**
    *   Python 3.6+
    *   PyQt5 (`pip install PyQt5`)
    *   PyQtChart (`pip install PyQtChart`)

2.  **Clone or Download the Project:**
    Obtain the project files and navigate to the root `SpendWise` directory.

3.  **Install Dependencies:**
    It's highly recommended to use a virtual environment.
    ```bash
    # Create a virtual environment (optional but good practice)
    python -m venv venv
    # Activate it:
    # Windows:
    # venv\Scripts\activate
    # macOS/Linux:
    # source venv/bin/activate

    # Install requirements
    pip install -r requirements.txt
    ```

4.  **Run the Application:**
    Ensure you are in the root `SpendWise` directory.
    *   **Recommended method:**
        ```bash
        python -m spendwise.main
        ```
    *   Alternative method:
        ```bash
        python spendwise/main.py
        ```

## 🛠️ Technical Details

*   **GUI Framework:** PyQt5
*   **Charting:** PyQtChart
*   **Data Storage:** JSON
*   **Styling:** Qt Style Sheets (QSS)
*   **Internationalization (i18n):** Custom dictionary-based translation.
*   **Settings Persistence:** `QSettings`

---