from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_inventory_modification():
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Step 1: Navigate to Home page
        driver.get("http://127.0.0.1:5000/")
        print("Opened app homepage.")

        # Step 2: Navigate to Inventory
        inventory_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="navbarNav"]/ul/li[2]/a'))
        )
        inventory_button.click()
        print("Found inventory.")


        #Step 3: Test Inventory Add
        modify_inventory_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="modInvenButton"]'))
        )
        modify_inventory_button.click()
        print("Clicked modify inventory Button")

        #Step 4: Input fields
        name_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'name'))
        )
        name_field.click()
        name_field.send_keys("Test 1")
        print("Input Name")

        qty_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'qty'))
        )
        qty_field.click()
        qty_field.send_keys("2")
        print("Input Quantity")

        operation_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'mode'))
        )
        operation_field.click()

        driver.find_element(By.XPATH, '//*[@id="mode"]/option[3]').click()
        print("Select add operation")

        #Step 5: Confirm and check our test worked
        driver.find_element(By.XPATH, '//*[@id="modInvenModal"]/div/div/form/div[2]/button[2]').click()
        
        page_source = driver.page_source
        if "Test 1" in page_source:
            print("Drug successfully added")

        # Step 6: Test subtract opetarion
        modify_inventory_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="modInvenButton"]'))
        )
        modify_inventory_button.click()
        print("Clicked modify inventory Button")

        name_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'name'))
        )
        name_field.click()
        name_field.send_keys("Test 1")
        print("Input Name")

        qty_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'qty'))
        )
        qty_field.click()
        qty_field.send_keys("1")
        print("Input Quantity")

        operation_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'mode'))
        )
        operation_field.click()

        driver.find_element(By.XPATH, '//*[@id="mode"]/option[4]').click()
        print("Select subtract operation")

        driver.find_element(By.XPATH, '//*[@id="modInvenModal"]/div/div/form/div[2]/button[2]').click()
        
        page_source = driver.page_source
        if "Test 1" in page_source:
            print("Drug successfully subtracted")


        #Step 7: Test removing drug from inventory
        modify_inventory_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="modInvenButton"]'))
        )
        modify_inventory_button.click()
        print("Clicked modify inventory Button")

        name_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'name'))
        )
        name_field.click()
        name_field.send_keys("Test 1")
        print("Input Name")

        qty_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'qty'))
        )
        qty_field.click()
        qty_field.send_keys("1")
        print("Input Quantity")

        operation_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'mode'))
        )
        operation_field.click()

        driver.find_element(By.XPATH, '//*[@id="mode"]/option[5]').click()
        print("Select remove operation")

        driver.find_element(By.XPATH, '//*[@id="modInvenModal"]/div/div/form/div[2]/button[2]').click()
        
        page_source = driver.page_source
        if "Test 1" not in page_source:
            print("Drug successfully removed")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    test_inventory_modification()

