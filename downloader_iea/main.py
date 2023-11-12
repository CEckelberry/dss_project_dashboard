import os
import shutil
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def login_to_iea(username, password, driver):
    driver.get("https://www.iea.org/account/login")
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "input-page-login-email"))
    )
    email_input.send_keys(username)
    password_input = driver.find_element(By.ID, "input-page-login-password")
    password_input.send_keys(password)
    password_input.submit()

def download_latest_csv_file(url, download_path, username, password):
    chrome_options = Options()
    prefs = {"download.default_directory": download_path}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    downloaded_file_name = None

    try:
        login_to_iea(username, password, driver)
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "m-product-releases-schedule__items")
            )
        )
        time.sleep(5)
        download_link = driver.find_element(
            By.XPATH, "(//span[normalize-space()='CSV'])[1]"
        )
        download_link.click()
        time.sleep(10)

        files = os.listdir(download_path)
        files = [f for f in files if f.endswith(".csv")]
        if files:
            downloaded_file_name = max(
                files, key=lambda x: os.path.getctime(os.path.join(download_path, x))
            )
        else:
            print("No CSV files found in the download directory.")
    except Exception as e:
        print(f"An error occurred while attempting to download the CSV: {e}")
    finally:
        driver.quit()

    return downloaded_file_name

def filter_csv_file(input_filename, output_filename):
    try:
        df = pd.read_csv(input_filename, skiprows=8, encoding="utf-8")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(input_filename, skiprows=8, encoding="iso-8859-1")
        except UnicodeDecodeError:
            df = pd.read_csv(input_filename, skiprows=8, encoding="cp1252")
    countries = ["Netherlands, The", "Belgium", "Luxembourg"]
    df_filtered = df[df["Country"].isin(countries)]
    df_filtered = df_filtered[df_filtered["Product"] == "Solar"]
    df_filtered.to_csv(output_filename, index=False)

def create_benelux_energy_csv(input_filename, output_filename):
    try:
        df = pd.read_csv(input_filename, skiprows=8, encoding="utf-8")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(input_filename, skiprows=8, encoding="iso-8859-1")
        except UnicodeDecodeError:
            df = pd.read_csv(input_filename, skiprows=8, encoding="cp1252")
    countries = ["Netherlands", "Belgium", "Luxembourg"]
    df_filtered = df[df["Country"].isin(countries)]
    df_filtered.to_csv(output_filename, index=False)

def move_and_rename_file(source_path, target_directory, new_name):
    os.makedirs(target_directory, exist_ok=True)
    new_file_path = os.path.join(target_directory, new_name)
    if os.path.exists(source_path):
        shutil.move(source_path, new_file_path)
        print(f"File moved and renamed to {new_name}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_path = script_dir
    data_dir = os.path.abspath(os.path.join(script_dir, "..", "data"))

    username = "cole.eckelberry@gmail.com" # Replace with your username
    password = "wzg.vkp.YWM*zkn1ugf" # Replace with your password
    url = "https://www.iea.org/data-and-statistics/data-product/monthly-electricity-statistics"

    downloaded_csv_name = download_latest_csv_file(url, download_path, username, password)

    if downloaded_csv_name:
        input_filename = os.path.join(download_path, downloaded_csv_name)

        # Process for Benelux energy production
        benelux_output_filename = "DSS_Datasets_GHG_energy_production_benelux.csv"
        create_benelux_energy_csv(input_filename, os.path.join(download_path, benelux_output_filename))
        move_and_rename_file(os.path.join(download_path, benelux_output_filename), data_dir, benelux_output_filename)

        # Process for Solar data
        solar_output_filename = "DSS_Datasets_GHG_Solar_iea_data.csv"
        filter_csv_file(input_filename, os.path.join(download_path, solar_output_filename))
        move_and_rename_file(os.path.join(download_path, solar_output_filename), data_dir, solar_output_filename)
    else:
        print("No CSV file was downloaded. Please check the download process.")