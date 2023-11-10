import os
from datetime import datetime
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


def login_to_iea(username, password, driver):
    driver.get("https://www.iea.org/account/login")

    # Wait for the email input field to be present
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "input-page-login-email"))
    )
    email_input.send_keys(username)

    # Find the password input field and enter the password
    password_input = driver.find_element(By.ID, "input-page-login-password")
    password_input.send_keys(password)

    # Submit the login form
    password_input.submit()


def download_latest_csv_file(url, download_path, username, password):
    # Set up Chrome options to specify the download directory
    chrome_options = Options()
    prefs = {"download.default_directory": download_path}
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize the Chrome WebDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)

    login_to_iea(username, password, driver)

    # Navigate to the target URL after logging in
    driver.get(url)

    # Wait for the necessary elements to load
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "m-product-releases-schedule__items")
            )
        )
        time.sleep(5)  # Additional wait for the page to fully load

        # Find the download link using the provided XPath
        download_link = driver.find_element(
            By.XPATH, "(//span[normalize-space()='CSV'])[1]"
        )
        download_link.click()

        time.sleep(10)  # Wait for the download to complete
        files = os.listdir(download_path)
        files = [f for f in files if f.endswith(".csv")]
        if files:
            downloaded_file_name = max(
                files, key=lambda x: os.path.getctime(os.path.join(download_path, x))
            )

        print(
            "Download started. Please check the specified download folder for the CSV file."
        )
    except Exception as e:
        print(f"An error occurred while attempting to download the CSV: {e}")
    finally:
        driver.quit()

    return downloaded_file_name


def filter_csv_file(input_filename, output_filename):
    # Read the CSV data into a DataFrame
    try:
        df = pd.read_csv(input_filename, skiprows=8, encoding="utf-8")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(input_filename, skiprows=8, encoding="iso-8859-1")
        except UnicodeDecodeError:
            df = pd.read_csv(input_filename, skiprows=8, encoding="cp1252")

    # Filter for the Netherlands, Belgium, and Luxembourg
    countries = [
        "Netherlands, The",
        "Belgium",
        "Luxembourg",
    ]  # Adjusted country names to match your data
    df_filtered = df[df["Country"].isin(countries)]

    # Filter for the product category Solar (if applicable)
    df_filtered = df_filtered[df_filtered["Product"] == "Solar"]

    # Save the filtered data to a new CSV file
    df_filtered.to_csv(output_filename, index=False)


if __name__ == "__main__":
    url = "https://www.iea.org/data-and-statistics/data-product/monthly-electricity-statistics"

    # Set the download path to the current script directory
    script_dir = os.path.dirname(__file__)
    download_path = script_dir

    # User credentials
    username = "cole.eckelberry@gmail.com"
    password = "wzg.vkp.YWM*zkn1ugf"

    # Download the latest CSV file and get its name
    downloaded_csv_name = download_latest_csv_file(
        url, download_path, username, password
    )

    if downloaded_csv_name:
        # Define the input file path using the downloaded file name
        input_filename = os.path.join(download_path, downloaded_csv_name)

        # Define the output file path in the 'data' directory
        data_dir = os.path.join(script_dir, "..", "data")
        output_filename = os.path.join(data_dir, "DSS_Datasets_GHG_Solar_iea_data.csv")

        # Check if the 'data' directory exists; create it if it doesn't
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Filter and transform the CSV file
        filter_csv_file(input_filename, output_filename)
    else:
        print("No CSV file was downloaded. Please check the download process.")
