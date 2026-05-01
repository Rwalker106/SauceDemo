# Conftest.py is a special configuration file for pytest that allows you to define fixtures, hooks, and other configurations that can be shared across multiple test files. In this case, we can use conftest.py to set up any necessary configurations or fixtures for our Playwright tests.
import pytest
import os
from dotenv import load_dotenv  
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage  

load_dotenv() # Load environment variables from .env file

@pytest.fixture(scope="session")
def sd_credentials(): # for SauceDemo credentials, which are stored in the .env file and accessed using environment variables for better security and flexibility.
    creds: dict[str, str | None] = {
        "username": os.getenv("SAUCE_USER"),
        "password": os.getenv("SAUCE_PASSWORD"),
        "locked_out_user": os.getenv("LOCKED_OUT_USER"),
        "problem_user": os.getenv("PROBLEM_USER"),
        "performance_glitch_user": os.getenv("PERFORMANCE_GLITCH_USER"),
        "visual_user": os.getenv("VISUAL_USER"),    
        "error_user": os.getenv("ERROR_USER"),
    }

    return creds

    
@pytest.fixture
def page():
    with sync_playwright() as playwright:   
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=1000, #to slow down the test execution for better visibility
            args=[
                "--disable-save-password-bubble", #to disable the save password pop-up from Chrome
                "--disable-features=PasswordLeakDetection", #to disable the password leak detection pop-up from Chrome
                ]
            )
        context = browser.new_context() 
        page = context.new_page()
        yield page
        context.close() 
        browser.close()
        
        
@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page=page).navigate()

        
@pytest.fixture
def logged_in_page(page, sd_credentials):# This fixture will log in to the application using the provided credentials and return the page object for further interactions in the tests.
    login_page = LoginPage(page=page)
    login_page.navigate().login(username=sd_credentials["username"], password=sd_credentials["password"])
    assert page.url == "https://www.saucedemo.com/inventory.html"
    return page