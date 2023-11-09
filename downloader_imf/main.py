from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Set up the Selenium webdriver (make sure you have the appropriate webdriver executable in your PATH)
driver = webdriver.Chrome()

try:
    # Navigate to the ArcGIS website
    driver.get(
        "https://experience.arcgis.com/experience/86e7e1aa0e6c4b07818ba3d36ba10ebe/page/Page-1/?data_id=dataSource_3-0%3A128&views=Select-a-Country"
    )

    # Wait for the search input element to be present (wait for a maximum of 20 seconds)
    search_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
    )

    # Interact with the search input
    search_input.send_keys("Netherlands, The")
    search_input.send_keys(Keys.RETURN)

    # Wait for the download button to be clickable (wait for a maximum of 20 seconds)
    download_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".widget-button-text"))
    )

    # Click on the download button to download the CSV
    download_button.click()

except TimeoutException as e:
    # Handle timeout exception
    print(f"TimeoutException: {str(e)}")
except Exception as e:
    # Handle any other exceptions that might occur during the process
    print(f"Error: {str(e)}")
finally:
    # Close the webdriver
    driver.quit()
