from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 5)
try:
    # Step 1: Navigate to Amazon
    driver.get("https://www.amazon.com/")
    driver.maximize_window()

    # Step 2: Search "amazon basics"
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_box.send_keys("amazon basics")
    search_box.send_keys(Keys.RETURN)

    # Step 3: Verify search results displayed
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'results for')]"))
    )
    print("Search results for 'amazon basics' displayed.")

    # Step 4: Select "Amazon Brands" checkbox
    amazon_brands_checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li//span[text()='Amazon Brands']"))
    )
    amazon_brands_checkbox.click()

    # Step 5: Select specific product
    product = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Amazon Basics Freezer Gallon Bags, 90 Count')]"))
    )
    product.click()

    # Step 6: Verify product page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "productTitle"))
    )
    print("Product page is displayed.")

    # Step 7: Verify size selection
    size_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'selection') and contains(text(),'90 Count')]"))
    )
    print("Correct size is selected: Gallon (90 Count)")

    # Step 8: Click "Add to Cart"
    add_to_cart = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
    )
    add_to_cart.click()

    # Step 9: Verify item added
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Added to Cart')]"))
    )
    print("Item successfully added to cart.")

    # Step 10: Verify cart shows "Subtotal (1 item)"
    cart_count = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "nav-cart-count"))
    )
    if cart_count.text == '1':
        print("Cart subtotal shows 1 item.")
    else:
        print("Cart item count mismatch.")

finally:
    # Close the browser after a short wait
    time.sleep(5)
    driver.quit()
