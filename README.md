# Data Management Algorithms for Decision Making

This project is part of the Data Management Algorithms for Decision Making course. It implements selection algorithms for decision-making problems, specifically static and online problem-solving approaches.

## Project Overview

The project provides a web-based interface using Streamlit to allow users to upload datasets and apply decision-making algorithms for optimal item selection. The selection process is based on constraints such as category-based limits and score-based rankings.

## Features

- **Static Problem Algorithm**: Selects the top K items based on predefined constraints.
- **Online Problem Algorithm (Secretary Problem Variant)**: Dynamically selects K items from an incoming data stream.
- **User Interface**: A simple and intuitive web-based UI for dataset upload and parameter selection.
- **Visualization**: Graphical representation of item selection process.

## Installation

To run this project locally, follow these steps:

### Clone the Repository

```sh
git clone <repository-url>
cd <repository-folder>
```

### Create a Virtual Environment (Optional but Recommended)

```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate   # On Windows
```

### Run the Streamlit Application

```sh
streamlit run app.py
```

## Project Structure

```
📂 project-root
 ├── app.py                 # Streamlit-based frontend UI
 ├── main.py                # Core algorithms for static and online selection
 ├── SanityTests.py         # Unit tests for validation
 ├── README.md              # Documentation (this file)
```

## Usage

1. Open the web application using Streamlit.
2. Select an algorithm type (Static or Online).
3. Set parameters such as K (number of items to select), category constraints, and total items (for online algorithm).
4. Upload an Excel file (.xlsx) containing the dataset with columns:
   - **ID**: Unique identifier for each item.
   - **Score**: Numeric score used for ranking.
   - **Category Number**: The category to which the item belongs.
5. Click **Run Algorithm** to process the data.
6. View results and download the selected items as a CSV file.


## Dependencies

Ensure you have the following Python libraries installed:

- `streamlit`
- `pandas`
- `matplotlib`
- `openpyxl`

## Contributors

- **Kamil Bokaae**
- **Mohammed Magamsey**

