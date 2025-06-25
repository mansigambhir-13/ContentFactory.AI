# tools/browser_automation.py
"""
Free browser automation using Selenium (no API keys needed!)
This directly automates posting to social media platforms
"""
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from typing import Dict, Optional

class BrowserPoster:
    """Automate posting using browser automation (100% FREE)"""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Add user data directory to maintain login sessions
        user_data_dir = os.path.expanduser("~/chrome_profile_social")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            return True
        except Exception as e:
            print(f"❌ Chrome driver setup failed: {str(e)}")
            print("💡 Install ChromeDriver: https://chromedriver.chromium.org/")
            return False
    
    def post_to_twitter(self, content: str, login_required: bool = True) -> bool:
        """Post content to Twitter using browser automation"""
        if not self.driver:
            if not self.setup_driver():
                return False
        
        try:
            # Go to Twitter
            self.driver.get("https://twitter.com")
            time.sleep(3)
            
            if login_required:
                print("🔐 Please log in to Twitter in the browser window that opened")
                print("⏳ Waiting 30 seconds for login...")
                time.sleep(30)
            
            # Find the tweet compose box
            try:
                # Try multiple selectors for the tweet box
                tweet_selectors = [
                    '[data-testid="tweetTextarea_0"]',
                    '[placeholder="What is happening?!"]',
                    '[aria-label="Tweet text"]',
                    '.public-DraftEditor-content'
                ]
                
                tweet_box = None
                for selector in tweet_selectors:
                    try:
                        tweet_box = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        break
                    except:
                        continue
                
                if tweet_box:
                    # Clear and type content
                    tweet_box.clear()
                    tweet_box.send_keys(content)
                    
                    # Find and click tweet button
                    tweet_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetButtonInline"]')
                    tweet_button.click()
                    
                    print("✅ Posted to Twitter successfully!")
                    time.sleep(2)
                    return True
                else:
                    print("❌ Could not find tweet compose box")
                    return False
                    
            except Exception as e:
                print(f"❌ Twitter posting error: {str(e)}")
                return False
                
        except Exception as e:
            print(f"❌ Twitter navigation error: {str(e)}")
            return False
    
    def post_to_linkedin(self, content: str, login_required: bool = True) -> bool:
        """Post content to LinkedIn using browser automation"""
        if not self.driver:
            if not self.setup_driver():
                return False
        
        try:
            # Go to LinkedIn feed
            self.driver.get("https://www.linkedin.com/feed/")
            time.sleep(3)
            
            if login_required:
                print("🔐 Please log in to LinkedIn in the browser window")
                print("⏳ Waiting 30 seconds for login...")
                time.sleep(30)
            
            # Find the post compose area
            try:
                # Click "Start a post" button
                start_post_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-control-name="share_to_feed"]'))
                )
                start_post_button.click()
                time.sleep(2)
                
                # Find text area in the modal
                text_area = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.ql-editor[data-placeholder]'))
                )
                
                # Clear and type content
                text_area.clear()
                text_area.send_keys(content)
                
                # Find and click post button
                post_button = self.driver.find_element(By.CSS_SELECTOR, '[data-control-name="share.post"]')
                post_button.click()
                
                print("✅ Posted to LinkedIn successfully!")
                time.sleep(2)
                return True
                
            except Exception as e:
                print(f"❌ LinkedIn posting error: {str(e)}")
                return False
                
        except Exception as e:
            print(f"❌ LinkedIn navigation error: {str(e)}")
            return False
    
    def guided_posting(self, content: Dict) -> None:
        """Guide user through manual posting process"""
        print("\n" + "="*60)
        print("🚀 GUIDED POSTING MODE")
        print("="*60)
        
        if content.get('twitter'):
            print(f"\n🐦 TWITTER CONTENT:")
            print("-" * 40)
            print(f"{content['twitter']}")
            print(f"\nCharacter count: {len(content['twitter'])}/280")
            input("\n👆 Copy the content above, go to twitter.com, and paste it. Press Enter when done...")
        
        if content.get('linkedin'):
            print(f"\n💼 LINKEDIN CONTENT:")
            print("-" * 40)
            print(f"{content['linkedin']}")
            print(f"\nCharacter count: {len(content['linkedin'])}")
            input("\n👆 Copy the content above, go to linkedin.com/feed, and paste it. Press Enter when done...")
        
        print("\n🎉 Great job! Your content is now posted!")
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()

# Install instructions for selenium
def install_selenium_instructions():
    return """
🔧 SELENIUM SETUP INSTRUCTIONS:

1. Install Selenium:
   pip install selenium

2. Install ChromeDriver:
   - Download from: https://chromedriver.chromium.org/
   - Or use: pip install webdriver-manager
   
3. Alternative - Use webdriver-manager (easier):
   pip install webdriver-manager
   
   Then modify the code to use:
   from webdriver_manager.chrome import ChromeDriverManager
   service = Service(ChromeDriverManager().install())
   driver = webdriver.Chrome(service=service, options=chrome_options)

🎯 This gives you 100% free posting automation!
"""