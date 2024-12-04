from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_inventory_modification():
    print("Testing inventory modification:")
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Step 1: Navigate to App Home page
        driver.get("http://127.0.0.1:5000/")
        print("Opened app homepage.", flush=True)

        # If navbar is closed open it
        nav_bar = driver.find_element(By.ID, "navbarNav")
        if nav_bar.is_displayed() == False:
            toggle_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/div/button'))
            )
            toggle_button.click()
            print("Clicked navigation toggle button.")

        # Step 2: Navigate to Inventory
        inventory_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="navbarNav"]/ul/li[2]/a'))
        )
        inventory_button.click()
        print("Found inventory.", flush=True)


        #Step 3: Test Inventory Add
        modify_inventory_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="modInvenButton"]'))
        )
        modify_inventory_button.click()
        print("Clicked modify inventory Button", flush=True)

        #Step 4: Input fields
        name_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'name'))
        )
        name_field.click()
        name_field.send_keys("Test 1")
        print("Input Name", flush=True)

        qty_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'qty'))
        )
        qty_field.click()
        qty_field.send_keys("2")
        print("Input Quantity", flush=True)

        operation_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'mode'))
        )
        operation_field.click()

        driver.find_element(By.XPATH, '//*[@id="mode"]/option[3]').click()
        print("Select add operation", flush=True)

        #Step 5: Confirm and check our test worked
        driver.find_element(By.XPATH, '//*[@id="modInvenModal"]/div/div/form/div[2]/button[2]').click()
        
        page_source = driver.page_source
        if "Test 1" in page_source:
            print("Drug successfully added", flush=True)
        else:
            raise ValueError("Failed to add drug")

        # Step 6: Test subtract opetarion (Repeat Steps 3 - 5)
        modify_inventory_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="modInvenButton"]'))
        )
        modify_inventory_button.click()
        print("Clicked modify inventory Button", flush=True)

        name_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'name'))
        )
        name_field.click()
        name_field.send_keys("Test 1")
        print("Input Name", flush=True)

        qty_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'qty'))
        )
        qty_field.click()
        qty_field.send_keys("1")
        print("Input Quantity", flush=True)

        operation_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'mode'))
        )
        operation_field.click()

        driver.find_element(By.XPATH, '//*[@id="mode"]/option[4]').click()
        print("Select subtract operation", flush=True)

        driver.find_element(By.XPATH, '//*[@id="modInvenModal"]/div/div/form/div[2]/button[2]').click()
        
        page_source = driver.page_source
        if "Test 1" in page_source:
            print("Drug successfully subtracted", flush=True)
        else:
            raise ValueError("Failed to subtract drug qty")

        #Step 7: Test removing drug from inventory
        nav_bar = driver.find_element(By.ID, "navbarNav")
        if nav_bar.is_displayed() == False:
            toggle_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/div/button'))
            )
            toggle_button.click()
            print("Clicked navigation toggle button.")
        
        modify_inventory_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="modInvenButton"]'))
        )
        modify_inventory_button.click()
        print("Clicked modify inventory Button", flush=True)

        name_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'name'))
        )
        name_field.click()
        name_field.send_keys("Test 1")
        print("Input Name", flush=True)

        qty_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'qty'))
        )
        qty_field.click()
        qty_field.send_keys("1")
        print("Input Quantity", flush=True)

        operation_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'mode'))
        )
        operation_field.click()

        driver.find_element(By.XPATH, '//*[@id="mode"]/option[5]').click()
        print("Select remove operation", flush=True)

        driver.find_element(By.XPATH, '//*[@id="modInvenModal"]/div/div/form/div[2]/button[2]').click()
        
        page_source = driver.page_source
        if "Test 1" not in page_source:
            print("Drug successfully removed", flush=True)
        else:
            raise ValueError("Failed to remove drug")

    finally:
        # Close the browser
        print("Inventory modification testing complete\n", flush=True)
        driver.quit()

def test_order_modification():
    print("Testing order modification:", flush=True)
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Start at home page
        driver.get("http://127.0.0.1:5000/")
        print("Opened Home page.", flush=True)
        
        # If nav bar is closed open it
        nav_bar = driver.find_element(By.ID, "navbarNav")
        if nav_bar.is_displayed() == False:
            toggle_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/div/button'))
            )
            toggle_button.click()
            print("Clicked navigation toggle button.")

        # Navigate to Inventory
        inventory_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="navbarNav"]/ul/li[2]/a'))
        )
        inventory_button.click()
        print("Navigated to Inventory", flush=True)

        # Add Inventory Item
        modify_inventory_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="modInvenButton"]'))
        )
        modify_inventory_button.click()
        print("Clicked modify inventory Button", flush=True)

        name_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'name'))
        )
        name_field.click()
        name_field.send_keys("Test Drug")
        print("Inputted Name", flush=True)

        qty_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'qty'))
        )
        qty_field.click()
        qty_field.send_keys("42")
        print("Inputted Quantity", flush=True)

        operation_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'mode'))
        )
        operation_field.click()

        driver.find_element(By.XPATH, '//*[@id="mode"]/option[3]').click()
        print("Selected add drug mode", flush=True)

        driver.find_element(By.XPATH, '//*[@id="modInvenModal"]/div/div/form/div[2]/button[2]').click()
        print("Clicked confirm to add drug to inventory", flush=True)
        
        page_source = driver.page_source
        if "Test Drug" in page_source:
            print("Drug successfully added", flush=True)
        else:
            raise ValueError("Failed to add drug")

        # Navigate back to Orders page
        nav_bar = driver.find_element(By.ID, "navbarNav")
        if nav_bar.is_displayed() == False:
            toggle_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/div/button'))
            )
            toggle_button.click()
            print("Clicked navigation toggle button.")
        
        inventory_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a'))
        )
        inventory_button.click()
        print("Navigated to Orders page", flush=True)

        # Click add order button
        add_order_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="createOrderButton"]'))
        )
        add_order_button.click()
        print("Clicked add order button", flush=True)

        # Add order
        name_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'name'))
        )
        name_field.click()
        name_field.send_keys("Aleyssu")
        print("Inputted Name", flush=True)

        drug_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'drug'))
        )
        drug_field.click()
        drug_field.send_keys("Test Drug")
        print("Inputted Drug", flush=True)

        qty_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'qty'))
        )
        qty_field.click()
        qty_field.send_keys("10")
        print("Inputted Quantity", flush=True)

        driver.find_element(By.XPATH, '//*[@id="inputOrderModal"]/div/div/form/div[2]/button[2]').click()
        print("Clicked confirm to add order", flush=True)

        page_source = driver.page_source
        if "Aleyssu" in page_source:
            print("Order successfully added", flush=True)
        else:
            raise ValueError("Failed to add order")

        # Modify order
        modify_order_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="orders"]/div[1]/div/div/div/div[2]/button'))
        )
        modify_order_button.click()
        print("Clicked modify order button", flush=True)

        qty_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'mod_qty'))
        )
        qty_field.click()
        qty_field.clear()
        qty_field.send_keys("12")
        print("Inputted Quantity", flush=True)

        driver.find_element(By.NAME, 'confirm_mod_order').click()
        print("Clicked confirm to modify order", flush=True)
        
        page_source = driver.page_source
        if "12" in page_source:
            print("Order successfully modified", flush=True)
        else:
            raise ValueError("Failed to modify order")

        # Complete Order
        modify_order_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="orders"]/div[1]/div/div/div/div[1]/button'))
        )
        modify_order_button.click()
        print("Clicked complete order button", flush=True)

        modify_order_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'confirm_complete_order'))
        )
        modify_order_button.click()
        print("Clicked confirm to complete order", flush=True)
        
        page_source = driver.page_source
        if "Aleyssu" not in page_source:
            print("Order successfully completed", flush=True)
        else:
            raise ValueError("Failed to complete order")

    finally:
        # Close the browser
        print("Order modification testing complete\n", flush=True)
        driver.quit()

def test_search():
    print("Testing search:")
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Step 1: Navigate to App Home page
        driver.get("http://127.0.0.1:5000/")
        print("Opened app homepage.", flush=True)
        
        # Check if navbar is open, if not open it
        nav_bar = driver.find_element(By.ID, "navbarNav")
        if nav_bar.is_displayed() == False:
            toggle_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/div/button'))
            )
            toggle_button.click()
            print("Clicked navigation toggle button.")

        #Step 2: Navigate to Order
        inventory_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a'))
        )
        inventory_button.click()
        print("Found orders.", flush=True)
        

        #Step 3: Input search
        search_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'search_query'))
        )
        search_field.click()
        search_field.send_keys("Charlie")
        print("Enter search name", flush=True)

        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'search_button'))
        )
        search_button.click()
        print("Click search", flush=True)

        #Step 4: Confirm and check our test worked
        topSearch = driver.find_element(By.XPATH, '//*[@id="orders"]/div[1]/div/div/h5')
        name = topSearch.text
        print("Check name of Top Search", flush=True)
        
        if name == "Charlie":
            print("Order search successful", flush=True)
        else:
            raise ValueError("Order sarch failed")

        #Step 5: repeat for inventory

        nav_bar = driver.find_element(By.ID, "navbarNav")
        if nav_bar.is_displayed() == False:
            toggle_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/div/button'))
            )
            toggle_button.click()
            print("Clicked navigation toggle button.")

        #Navigate to Inventory
        inventory_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="navbarNav"]/ul/li[2]/a'))
        )
        inventory_button.click()
        print("Found inventory.", flush=True)

        #Input search
        search_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'search_query'))
        )
        search_field.click()
        search_field.send_keys("H2O")
        print("Enter search name", flush=True)
        

        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'search_button'))
        )
        search_button.click()
        print("Click search", flush=True)

        #Confirm and check our test worked
        topSearch = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[1]/div/div/h5')
        name = topSearch.text
        print("Check name of Top Search", flush=True)
        
        if name == "H2O":
            print("Inventory search successful", flush=True)
        else:
            raise ValueError("Inventory search failed")

    finally:
        # Close the browser
        print("Search Testing Complete\n", flush=True)
        driver.quit()

if __name__ == "__main__":
    test_inventory_modification()
    test_order_modification()
    test_search()

