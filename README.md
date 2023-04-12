# Garmin Connect Report Downloader

This script downloads Garmin Connect reports for a specified report type and time period or a custom link. It uses Selenium WebDriver to interact with the Garmin Connect website, authenticate the user, and download the requested report. After downloading, it displays the report's content on the command line and removes the downloaded CSV file.

## Requirements

- Python 3.11.3 (will probably work with 3.7 onwards)
- Python Selenium package

## Installation

1. Clone this repository.

2. Install the required dependencies:

    ```
    pip install selenium
    ```
    or 
    ```
    pip install -r requirements.txt
## Usage

1. Run the script, providing the required arguments. For example:

    ```
    python3 script.py -u your_username -p your_password -t Steps -d last_seven_days
    ```

2. The script supports the following command line arguments:

    - `-u`, `--username`: Garmin Connect username (required)
    - `-p`, `--password`: Garmin Connect password (required)
    - `-t`, `--type`: Type of the report (Steps, Sleep Score, or Calories)
    - `-d`, `--period`: Time period of the report (last_seven_days, last_four_weeks, or last_year)
    - `-c`, `--custom`: Custom link to a Garmin Connect report (e.g. https://connect.garmin.com/modern/report/4/running/last_seven_days)

3. The `-t` and `-d` arguments are mutually exclusive with the `-c` argument. Either the report type and period should be provided, or a custom link.

## Credits

This script was created with the help of OpenAI's ChatGPT.
