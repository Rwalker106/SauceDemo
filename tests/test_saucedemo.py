import json
import csv
import pytest



def test_login_success(logged_in_page):
    assert logged_in_page.url == "https://www.saucedemo.com/inventory.html" 
    #asserts that the URL is correct after logging in, which indicates a successful login.
    assert logged_in_page.title() == "Swag Labs"
    #asserts that the URL is correct after logging in, which indicates a successful login.
    assert logged_in_page.get_by_text("Products").is_visible()
    #asserts that the "Products" text is visible on the page, which indicates a successful login.
    
def test_login_wrong_password(login_page, sd_credentials) -> None:
    login_page.login(username=sd_credentials["username"], password="wrong_password")
    assert login_page.is_error_visible() #asserts that an error message is visible on the page, which indicates a failed login attempt.
    assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"
    #asserts that the error message is correct, which indicates a failed login attempt.
    
def test_login_locked_user(login_page, sd_credentials) -> None:
    login_page.login(username=sd_credentials["locked_out_user"], password=sd_credentials["password"])
    assert login_page.is_error_visible() #asserts that an error message is visible on the page, which indicates a failed login attempt.
    assert login_page.get_error_message() == "Epic sadface: Sorry, this user has been locked out."
    #asserts that the error message is correct, which indicates a failed login attempt.

@pytest.mark.parametrize("username,password,expect_error", [
    ("standard_user",   "secret_sauce", False),
    ("locked_out_user", "secret_sauce", True),
    ("standard_user",   "wrong_password",   True),
    ("",                "",             True),
])

def test_login_errors(login_page, username, password, expect_error) -> None:
    login_page.login(username=username, password=password)
    assert login_page.is_error_visible() == expect_error #asserts that an error message is visible on the page, which indicates a failed login attempt.
    if expect_error:
        assert login_page.get_error_message() != ""
    #asserts that the error message is correct, which indicates a failed login attempt. 
    
    
def test_products_export(logged_in_page):
    products = []
    for product in logged_in_page.locator(".inventory_item").all():
        item_name = product.locator(".inventory_item_name").inner_text()
        price     = product.locator(".inventory_item_price").inner_text()
        products.append({"Product Name": item_name, "Price": price})

    assert len(products) == 6

    with open("products.json", "w") as f:
        json.dump(products, f, indent=2)

    with open("products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Product Name", "Price"])
        writer.writeheader()
        writer.writerows(products)


def test_add_to_cart(logged_in_page):
    logged_in_page.get_by_role("button", name="Add to cart").first.click() #clicks the first "Add to cart" button on the inventory page
    cart_count = logged_in_page.locator(".shopping_cart_badge").inner_text() #locates the shopping cart badge and gets the number of items in the cart
    assert cart_count == "1" #asserts that there is 1 item in the cart after clicking the "Add to cart" button
        
        
        
            
            
        
        
        
    