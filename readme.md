# WhatsApp Chat Analyzer

WhatsApp Chat Analyzer is a web application built with Streamlit to analyze WhatsApp chat data. It provides insights through various statistics and visualizations such as message counts, word counts, media shared, links shared, activity timelines, and emoji analysis.

## Features

- Upload and preprocess WhatsApp chat data.
- Display statistics for overall and individual users:
  - Total messages
  - Total words
  - Media shared
  - Links shared
- Monthly and daily activity timelines.
- Weekly and monthly activity maps.
- Heatmap of user activity by day and hour.
- Most active users and their statistics.
- Word cloud of the most common words.
- Emoji analysis.

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/sohamfcb/whatsapp-chat-analyzer.git
   cd whatsapp-chat-analyzer

2. **Create and activate a virtual environment:**

- On MacOS and Linux

    ```sh
    python3 -m venv env`
    source env/bin/activate

- On Windows:

  ```sh
  python -m venv env`
  .\env\Scripts\activate

### Install the dependencies:

     ```sh
     pip install -r requirements.txt

## Usage

 -   Run the Streamlit app:

     ```sh
     streamlit run app.py`
     
 -   Upload your WhatsApp chat data:
       - Export your chat from WhatsApp as a .txt file.
       - Upload the file using the file uploader in the sidebar.
       - Select a user to analyze and view the results.

## File Structure

   - `app.py`: Main Streamlit application.
   - `helper.py`: Functions for data analysis and visualization.
   - `preprocessor.py`: Functions for preprocessing chat data.
   - `requirements.txt`: Python packages required.
