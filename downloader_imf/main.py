import pandas as pd
import os
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import shutil


def download_latest_csv_file(urls, download_path):
    # Set up Chrome options to specify the download directory
    chrome_options = Options()
    prefs = {"download.default_directory": download_path}
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        for url in urls:
            # Navigate to the website
            driver.get(url)

            # Wait for the download button to be present
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//a[normalize-space()='Download']//div[@class='stacked-icon']//*[name()='svg']",
                    )
                )
            )

            # Find the download button and click it
            download_button = driver.find_element(
                By.XPATH,
                "//a[normalize-space()='Download']//div[@class='stacked-icon']//*[name()='svg']",
            )
            download_button.click()

            # Wait for the download to complete (adjust time as necessary)
            time.sleep(10)

    finally:
        # Close the browser
        driver.quit()


def process_csv_files(directory, file_names):
    for file in os.listdir(directory):
        if file.endswith(".zip"):
            zip_path = os.path.join(directory, file)
            temp_dir = os.path.join(directory, "temp")
            os.makedirs(temp_dir, exist_ok=True)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            for file_name in file_names:
                extracted_file_path = os.path.join(temp_dir, file_name + ".csv")
                if os.path.exists(extracted_file_path):
                    final_file_path = os.path.join(directory, file_name + ".csv")
                    if os.path.exists(final_file_path):
                        existing_df = pd.read_csv(final_file_path)
                        new_df = pd.read_csv(extracted_file_path)
                        combined_df = pd.concat([existing_df, new_df])
                        combined_df.to_csv(final_file_path, index=False)
                    else:
                        shutil.move(extracted_file_path, final_file_path)

            # Clean up: remove the temporary directory and the zip file
            shutil.rmtree(temp_dir)
            os.remove(zip_path)


def rename_and_move_files(source_directory, target_directory, file_mappings):
    os.makedirs(target_directory, exist_ok=True)  # Ensure the target directory exists
    for old_name, new_name in file_mappings.items():
        old_file_path = os.path.join(source_directory, old_name + ".csv")
        new_file_path = os.path.join(target_directory, new_name + ".csv")

        if os.path.exists(old_file_path):
            shutil.move(old_file_path, new_file_path)
            print(f"File renamed and moved: {new_name}")


# Set the download path to the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the target data directory relative to the script location
data_dir = os.path.abspath(os.path.join(script_dir, "..", "data"))

# URLs of the websites
urls = [
    "https://climatedata.imf.org/datasets/4336ea7f6ea443bb80f83f2cd53f2672/about",
    "https://climatedata.imf.org/datasets/a984f9c8f4e54094b80ac7e203986fc9/about",
    "https://climatedata.imf.org/datasets/74c27e7285fd4bd18927e459221e63a2/about",
]

# Specific CSV files to keep
csv_files_to_keep = [
    "National_Greenhouse_Gas_Emissions_Inventories_and_Implied_National_Mitigation_Nationally_Determined_Contributions_Targets",
    "CO2_Emissions_Emissions_Intensities_and_Emissions_Multipliers",
]

# Mapping of old file names to new file names
file_mappings = {
    "National_Greenhouse_Gas_Emissions_Inventories_and_Implied_National_Mitigation_Nationally_Determined_Contributions_Targets": "DSS_Datasets_GHG_Solar_National_Greenhouse_Gas_Emissions_Inventories_and_Implied_National_Mitigation_Nationally",
    "CO2_Emissions_Emissions_Intensities_and_Emissions_Multipliers": "DSS_Datasets_GHG_Solar_CO2_Emissions_Emissions_Intensities_and_Emissions_Multipliers",
}

# Call the function to download the CSV files
download_latest_csv_file(urls, script_dir)

# Process the CSV files
process_csv_files(script_dir, csv_files_to_keep)

# Rename and move the files
rename_and_move_files(script_dir, data_dir, file_mappings)
