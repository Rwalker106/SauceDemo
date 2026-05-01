

class LoginPage:
    URL = "https://www.saucedemo.com/"
    
    def __init__(self, page):
        self.page = page
        
        # Locators defined once here for better maintainability
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")   
        self.login_button = page.get_by_role("button", name="Login")    
        self.error_message = page.locator("[data-test='error']")  # Assuming error messages are shown in an element with data-test="error"
        
    def navigate(self):
        self.page.goto(self.URL)    
        return self
    
    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return self
    
    def get_error_message(self):
        return self.error_message.inner_text()
    
    
    def is_error_visible(self):
        return self.error_message.is_visible()  