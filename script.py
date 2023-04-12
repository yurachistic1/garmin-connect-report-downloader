import argparse
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    InvalidArgumentException,
)

# Global vars
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
initial_csv_files = [f for f in os.listdir(downloads_folder) if f.endswith(".csv")]


# Function to log in to Garmin Connect and export the report
def authenticate_and_export_report(driver, wait, username, password):
    # Switch to iframe and input username and password
    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, "//iframe[@id='gauth-widget-frame-gauth-widget']")
        )
    )
    wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(
        username
    )
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(
        f"{password}\n"
    )

    # Click the Export button
    element = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Export')]"))
    )

    element.click()
    wait.until(file_downloaded)


# Check if a new CSV file has been downloaded
def file_downloaded(driver):
    global downloads_folder, initial_csv_files
    csv_files = [f for f in os.listdir(downloads_folder) if f.endswith(".csv")]
    return len(csv_files) - len(initial_csv_files) > 0


# Get the list of CSV files sorted by modification time
def get_csv_files_sorted_by_mtime(directory):
    csv_files = [f for f in os.listdir(directory) if f.endswith(".csv")]
    csv_files.sort(
        key=lambda f: os.path.getmtime(os.path.join(directory, f)), reverse=True
    )
    return csv_files


# Function to download the Garmin report
def download_garmin_report(username, password, link):
    global downloads_folder

    try:
        # Set up the Selenium WebDriver and load the report page
        driver = webdriver.Chrome()
        driver.get(link)
        wait = WebDriverWait(driver, 20)

        authenticate_and_export_report(driver, wait, username, password)
    except InvalidArgumentException:
        print("The link provided seems invalid, make sure you provide the full link.")
        return
    except NoSuchElementException:
        print("Element not found.")
        return
    except TimeoutException:
        print("Timeout exceeded.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
    finally:
        driver.close()
        time.sleep(1)
        driver.quit()

    # Read and display the content of the downloaded CSV file
    sorted_csv_files = get_csv_files_sorted_by_mtime(downloads_folder)
    file_name = sorted_csv_files[0]

    return file_name


def display_garmin_report(file_name):
    try:
        with open(
            f"{downloads_folder}/{file_name}", "r", encoding="utf-8-sig"
        ) as csvfile:
            content = csvfile.read()
            print(content)

        os.remove(f"{downloads_folder}/{file_name}")
    except FileNotFoundError:
        print("CSV file not found.")
    except PermissionError:
        print("Error: Permission denied to remove downloaded CSV.")
    except OSError as e:
        print(f"Error: {e}")


# Main script entry point
if __name__ == "__main__":
    # Report options and time periods
    base_report_url = "https://connect.garmin.com/modern/report/"
    report_options = {
        "Steps": {"path": "29/wellness/"},
        "Sleep Score": {"path": "-26/wellness/"},
        "Calories": {"path": "41/wellness/"},
    }
    time_period_options = ["last_seven_days", "last_four_weeks", "last_year"]

    # Validate the provided arguments
    def validate_command_line_args(args):
        if (
            (args.type and args.period and args.custom)
            or (args.custom and (args.type or args.period))
            or (not args.custom and not (args.type and args.period))
        ):
            parser.error(
                "Either report type and period must be provided, or custom link."
            )

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Download Garmin Connect reports.")

    parser.add_argument("-u", "--username", type=str, required=True, help="Username")
    parser.add_argument("-p", "--password", type=str, required=True, help="Password")
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=["Steps", "Sleep Score", "Calories"],
        help="Type of the report",
    )
    parser.add_argument(
        "-d",
        "--period",
        type=str,
        choices=["last_seven_days", "last_four_weeks", "last_year"],
        help="Time period of the report",
    )
    parser.add_argument("-c", "--custom", type=str, help="Custom link")

    args = parser.parse_args()
    validate_command_line_args(args)

    report_file = download_garmin_report(
        args.username,
        args.password,
        args.custom
        if args.custom
        else f'{base_report_url}{report_options[args.type]["path"]}{args.period}',
    )

    display_garmin_report(report_file)
