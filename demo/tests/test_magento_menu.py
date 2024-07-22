import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Configuration
URL = "https://trulyfreehome.dev"
OTP = "1111"  # Replace with dynamic retrieval if needed
CARD_NUMBER = "4242424242424242"
CVV = "111"
EXPIRY_MONTH = "05"
EXPIRY_YEAR = "2026"
FIRST_NAME = "John"
LAST_NAME = "Doe"
PHONE_NUMBER = "987654321"
EMAIL = "vik@gmail.com"
ADDRESS = "pune"
ZIP_CODE = "411048"
CITY = "pune"
STATE = "MH"
COUNTRY = "India"


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()  # Ensure the chromedriver executable is in your PATH
    driver.maximize_window()
    yield driver
    driver.quit()


def test_signup(driver):
    driver.get(URL)
    try:
       #Sign me up for Free Today" button
        sign_up_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign me up for Free Today')]"))
        )
        sign_up_button.click()

        # Enter phone number and continue
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "phone"))
        ).send_keys(PHONE_NUMBER)
        driver.find_element(By.NAME, "terms").click()
        driver.find_element(By.NAME, "continue").click()

        # Enter OTP and complete the signup
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "otp"))
        ).send_keys(OTP)
        driver.find_element(By.NAME, "done").click()

    except Exception as e:
        print("Error during signup:", e)
        print(driver.page_source)
        pytest.fail("Signup test failed.")


def test_mega_menu(driver):
    driver.get(URL)
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Brands"))
        ).click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Emani"))
        ).click()
    except Exception as e:
        print("Error in mega menu navigation:", e)
        pytest.fail("Mega menu test failed.")


def test_plp(driver):
    driver.get(URL)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-item"))
        )
        product_names = []
        product_prices = []

        products = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        for product in products:
            name = product.find_element(By.CSS_SELECTOR, ".product-name").text
            price = product.find_element(By.CSS_SELECTOR, ".product-price").text
            product_names.append(name)
            product_prices.append(price)

        with open("product_details.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Product Name", "Product Price"])
            writer.writerows(zip(product_names, product_prices))

        products[0].click()  # Click on the first product
    except Exception as e:
        print("Error in PLP test:", e)
        pytest.fail("PLP test failed.")


def test_pdp(driver):
    driver.get(URL)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".product-details"))
        )
        quantity_input = driver.find_element(By.NAME, "quantity")
        quantity_input.clear()
        quantity_input.send_keys("2")
        driver.find_element(By.NAME, "add_to_cart").click()
        time.sleep(2)
        cart_count = driver.find_element(By.CSS_SELECTOR, ".cart-count").text
        assert cart_count == "2"
    except Exception as e:
        print("Error in PDP test:", e)
        pytest.fail("PDP test failed.")


def test_cart(driver):
    driver.get(URL)
    try:
        driver.find_element(By.CSS_SELECTOR, ".cart-icon").click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-page"))
        )
        product = driver.find_element(By.CSS_SELECTOR, ".cart-product")
        assert product is not None
        product_price = product.find_element(By.CSS_SELECTOR, ".cart-product-price").text
        assert product_price != ""
    except Exception as e:
        print("Error in Cart test:", e)
        pytest.fail("Cart test failed.")


def test_checkout(driver):
    driver.get(URL)
    try:
        driver.find_element(By.CSS_SELECTOR, ".checkout-button").click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "shipping_first_name"))
        ).send_keys(FIRST_NAME)
        driver.find_element(By.NAME, "shipping_last_name").send_keys(LAST_NAME)
        driver.find_element(By.NAME, "shipping_phone").send_keys(PHONE_NUMBER)
        driver.find_element(By.NAME, "shipping_email").send_keys(EMAIL)
        driver.find_element(By.NAME, "shipping_address").send_keys(ADDRESS)
        driver.find_element(By.NAME, "shipping_zip").send_keys(ZIP_CODE)
        driver.find_element(By.NAME, "shipping_city").send_keys(CITY)
        driver.find_element(By.NAME, "shipping_state").send_keys(STATE)
        driver.find_element(By.NAME, "shipping_country").send_keys(COUNTRY)
        driver.find_element(By.NAME, "continue").click()
    except Exception as e:
        print("Error in Checkout test:", e)
        pytest.fail("Checkout test failed.")


def test_place_order(driver):
    driver.get(URL)
    try:
        driver.find_element(By.NAME, "card_name").send_keys(FIRST_NAME + " " + LAST_NAME)
        driver.find_element(By.NAME, "card_number").send_keys(CARD_NUMBER)
        driver.find_element(By.NAME, "cvv").send_keys(CVV)
        driver.find_element(By.NAME, "expiry_month").send_keys(EXPIRY_MONTH)
        driver.find_element(By.NAME, "expiry_year").send_keys(EXPIRY_YEAR)
        driver.find_element(By.NAME, "confirm_order").click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".exclusive-deals-cross"))
        ).click()
        time.sleep(8)
        order_id = driver.find_element(By.CSS_SELECTOR, ".order-id").text
        print(f"Order ID: {order_id}")
    except Exception as e:
        print("Error in Place Order test:", e)
        pytest.fail("Place Order test failed.")


def test_logout(driver):
    driver.get(URL)
    try:
        driver.find_element(By.CSS_SELECTOR, ".profile-icon").click()
        driver.find_element(By.LINK_TEXT, "Logout").click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "login"))
        )
    except Exception as e:
        print("Error in Logout test:", e)
        pytest.fail("Logout test failed.")


if __name__ == "__main__":
    pytest.main()
