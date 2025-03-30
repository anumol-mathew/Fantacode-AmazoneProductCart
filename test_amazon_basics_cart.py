from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys

# Check if ssl module is available
try:
    import ssl
except ModuleNotFoundError:
    print("The 'ssl' module is not available in your Python environment. Please reinstall Python with SSL support.")
    sys.exit(1)


# Set ChromeDriver path
chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "chromedriver")
service = Service(executable_path=chromedriver_path)

# Setup Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-popup-blocking")

try:
    driver = webdriver.Chrome(service=service, options=options)

    # Step 1: Navigate to Amazon
    driver.get("https://www.amazon.com/")

    # Step 2: Search "amazon basics"
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_box.send_keys("amazon basics")
    search_box.send_keys(Keys.RETURN)

    # Step 3: Verify search results are displayed
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'results for')]"))
    )
    print("Search results loaded")

    # Step 4: Select "Amazon Brands" checkbox
    amazon_brands_checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[@aria-label='Amazon Brands']//input"))
    )
    driver.execute_script("arguments[0].click();", amazon_brands_checkbox)
    time.sleep(3)

    # Step 5: Select specific product
    product = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Amazon Basics Freezer Gallon Bags"))
    )
    product.click()

    # Step 6: Verify product page is displayed
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "productTitle"))
    )
    print("Product page displayed")

    # Step 7: Verify "Gallon (90 Count)" is selected
    selected_size = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Gallon (90 Count)')]"))
    )
    assert selected_size, "Correct size is not selected"
    print("Correct size selected")

    # Step 8: Click on "Add to Cart"
    add_to_cart = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
    )
    add_to_cart.click()
    time.sleep(3)

    # Step 9: Verify item added to cart
    cart_confirmation = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sw-subtotal-label-buybox"))
    )
    print("Item added to cart")

    # Step 10: Verify subtotal
    subtotal_text = driver.find_element(By.ID, "sw-subtotal-label-buybox").text
    assert "Subtotal (1 item)" in subtotal_text, "Incorrect cart subtotal"
    print("Cart subtotal verified")

except ModuleNotFoundError as mnfe:
    print("Missing module error:", mnfe)
    print("Please ensure all required packages are installed. Run: pip install selenium")

except Exception as e:
    print("Test failed:", e)

finally:
    try:
        driver.quit()
    except:
        pass
