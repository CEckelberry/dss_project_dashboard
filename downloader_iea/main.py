import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    driver = webdriver.Chrome()
    login_to_iea(username, password, driver)

    # Navigate to the target URL after logging in
    driver.get(url)

    # Wait for the schedule section to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "schedule")))

    # Check the schedule section to see if a new CSV file is available
    schedule_section = driver.find_element(By.ID, "schedule")
    latest_update_date = None

    for schedule_item in schedule_section.find_elements(
        By.CLASS_NAME, "m-product-releases-schedule-item"
    ):
        if "Scheduled" in schedule_item.text:
            latest_update_date = schedule_item.find_element(
                By.CLASS_NAME, "m-product-releases-schedule-item__date"
            ).text
            break

    if latest_update_date is not None:
        # Download the latest CSV file
        download_link = driver.find_element(By.CLASS_NAME, "a-link__label")
        download_link.click()

        # Wait for the file to be downloaded
        WebDriverWait(driver, 60).until(lambda x: len(os.listdir(download_path)) > 0)

        # Get the downloaded filename
        downloaded_files = os.listdir(download_path)
        csv_filename = [file for file in downloaded_files if file.endswith(".csv")][0]

        # Rename the downloaded file to the desired filename
        os.rename(
            os.path.join(download_path, csv_filename),
            os.path.join(download_path, "DSS_Datasets_GHG_Solar_iea_data.csv"),
        )
    else:
        print("No new CSV file available.")

    driver.quit()


def filter_csv_file(input_filename, output_filename):
    df = pd.read_csv(input_filename)

    # Filter for the Netherlands, Belgium, and Luxembourg
    countries = ["Netherlands", "Belgium", "Luxembourg"]
    df_filtered = df[df["Country"].isin(countries)]

    # Filter for the product category Solar
    df_filtered = df_filtered[df_filtered["Product"] == "Solar"]

    # Filter for just the necessary columns
    columns_to_keep = ["Country", "Time", "Balance", "Product", "Value", "Unit"]
    df_filtered = df_filtered[columns_to_keep]

    # Save the filtered data to a new CSV file
    df_filtered.to_csv(output_filename, index=False)


if __name__ == "__main__":
    url = "https://www.iea.org/data-and-statistics/data-product/monthly-electricity-statistics"
    download_path = "../data/"
    username = "cole.eckelberry@gmail.com"
    password = "wzg.vkp.YWM*zkn1ugf"

    download_latest_csv_file(url, download_path, username, password)

    # Filter the CSV file for the Netherlands, Belgium, and Luxembourg
    input_filename = os.path.join(download_path, "DSS_Datasets_GHG_Solar_iea_data.csv")
    output_filename = "../data/DSS_Datasets_GHG_Solar_iea_data.csv"
    filter_csv_file(input_filename, output_filename)
