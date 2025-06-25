# tools/twitter_automation_robust.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class RobustTwitterPoster:
    """Enhanced Twitter automation with multiple fallback methods"""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome driver with enhanced options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Enhanced options for better compatibility
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User data directory for persistent sessions
        import os
        user_data_dir = os.path.expanduser("~/chrome_twitter_profile")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            print(f"❌ Chrome driver setup failed: {str(e)}")
            return False
    
    def wait_for_login(self):
        """Wait for user to log in manually"""
        print("🔐 Please log in to Twitter in the browser window")
        print("📍 Navigate to the home feed after logging in")
        print("⏳ Waiting for you to reach the home page...")
        
        # Wait for home page indicators
        home_indicators = [
            "//span[contains(text(), 'Home')]",
            "//h1[contains(text(), 'Home')]",
            "//div[@data-testid='primaryColumn']",
            "//div[contains(@aria-label, 'Timeline')]"
        ]
        
        for _ in range(60):  # Wait up to 60 seconds
            for indicator in home_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, indicator)
                    if element:
                        print("✅ Detected Twitter home page!")
                        time.sleep(2)
                        return True
                except NoSuchElementException:
                    continue
            time.sleep(1)
        
        print("⚠️ Couldn't detect login. Proceeding anyway...")
        return True
    
    def find_compose_box(self):
        """Try multiple methods to find the tweet compose box"""
        
        # Method 1: Try clicking "Post" or "Tweet" button first
        post_button_selectors = [
            "//span[text()='Post']",
            "//span[text()='Tweet']", 
            "//div[@data-testid='SideNav_NewTweet_Button']",
            "//a[@data-testid='SideNav_NewTweet_Button']",
            "//div[contains(@aria-label, 'Post')]"
        ]
        
        for selector in post_button_selectors:
            try:
                button = self.driver.find_element(By.XPATH, selector)
                self.driver.execute_script("arguments[0].click();", button)
                print("✅ Clicked compose button")
                time.sleep(2)
                break
            except NoSuchElementException:
                continue
        
        # Method 2: Try multiple compose box selectors
        compose_selectors = [
            # New Twitter interface
            "//div[@data-testid='tweetTextarea_0']",
            "//div[@data-testid='tweetTextarea_0_label']//div[@contenteditable='true']",
            "//div[@role='textbox'][@data-testid='tweetTextarea_0']",
            
            # Alternative selectors
            "//div[@contenteditable='true'][contains(@aria-label, 'Post text')]",
            "//div[@contenteditable='true'][contains(@aria-label, 'Tweet text')]", 
            "//div[@contenteditable='true'][contains(@placeholder, 'What')]",
            
            # Fallback selectors
            "//div[@role='textbox'][@contenteditable='true']",
            "//div[@data-contents='true']",
            "//div[contains(@class, 'public-DraftEditor-content')]"
        ]
        
        for selector in compose_selectors:
            try:
                element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                print(f"✅ Found compose box with selector: {selector}")
                return element
            except TimeoutException:
                continue
        
        return None
    
    def post_to_twitter(self, content: str) -> bool:
        """Enhanced Twitter posting with multiple fallback methods"""
        
        if not self.driver:
            if not self.setup_driver():
                return False
        
        try:
            # Navigate to Twitter
            print("🌐 Opening Twitter...")
            self.driver.get("https://twitter.com")
            time.sleep(3)
            
            # Check if we need to log in
            current_url = self.driver.current_url
            if "login" in current_url or "oauth" in current_url:
                if not self.wait_for_login():
                    return False
            
            # Try to find and use compose box
            compose_box = self.find_compose_box()
            
            if compose_box:
                try:
                    # Clear any existing content
                    compose_box.click()
                    time.sleep(1)
                    
                    # Use JavaScript to set the content (more reliable)
                    self.driver.execute_script(
                        "arguments[0].textContent = arguments[1];", 
                        compose_box, content
                    )
                    
                    # Trigger input event
                    self.driver.execute_script("""
                        arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
                        arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                    """, compose_box)
                    
                    time.sleep(2)
                    
                    # Find and click post button
                    post_selectors = [
                        "//div[@data-testid='tweetButtonInline']",
                        "//div[@data-testid='tweetButton']",
                        "//span[text()='Post']//ancestor::div[@role='button']",
                        "//span[text()='Tweet']//ancestor::div[@role='button']"
                    ]
                    
                    for selector in post_selectors:
                        try:
                            post_button = self.driver.find_element(By.XPATH, selector)
                            self.driver.execute_script("arguments[0].click();", post_button)
                            print("✅ Posted to Twitter successfully!")
                            time.sleep(3)
                            return True
                        except NoSuchElementException:
                            continue
                    
                    print("❌ Could not find post button")
                    return False
                    
                except Exception as e:
                    print(f"❌ Error while posting: {str(e)}")
                    return False
            else:
                print("❌ Could not find compose box")
                return False
                
        except Exception as e:
            print(f"❌ Twitter posting error: {str(e)}")
            return False
    
    def guided_posting_mode(self, content: str):
        """Interactive guided posting when automation fails"""
        print("\n" + "="*60)
        print("🎯 GUIDED POSTING MODE")
        print("="*60)
        print(f"\n📝 Your content is ready:")
        print(f"📱 Content: {content}")
        print(f"📏 Length: {len(content)} characters")
        print("\n📋 Manual steps:")
        print("1. Go to https://twitter.com")
        print("2. Click the compose/post button")
        print("3. Copy and paste the content above")
        print("4. Click 'Post' or 'Tweet'")
        print("\n💡 The browser will stay open for you to post manually.")
        
        input("Press Enter when you've posted the content...")
        print("🎉 Great! Your content should now be live on Twitter!")
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()

# Simple test function
def test_twitter_posting():
    """Test the Twitter posting functionality"""
    poster = RobustTwitterPoster(headless=False)
    
    test_content = "Testing my AI content automation system! 🤖 This is a test post. #AI #Automation #Test"
    
    print("🧪 Testing Twitter automation...")
    success = poster.post_to_twitter(test_content)
    
    if not success:
        print("🎯 Falling back to guided posting mode...")
        poster.guided_posting_mode(test_content)
    
    poster.close()

if __name__ == "__main__":
    test_twitter_posting()