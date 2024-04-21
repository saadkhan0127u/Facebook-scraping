import csv
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration file reader
config = configparser.ConfigParser()

class FacebookScraper:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.navigate_to("https://www.facebook.com/")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(username)
        self.driver.find_element(By.ID, "pass").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[name='login']").click()

    def navigate_to(self, url):
        self.driver.get(url)

    def search_facebook(self, term):
        self.navigate_to("https://www.facebook.com/search/top/?q=" + term)

    def extract_profile_links(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/friends/")][not(@aria-hidden="true")]')))
        friends_links = self.driver.find_elements(By.XPATH, '//a[contains(@href, "/friends/")][not(@aria-hidden="true")]')
        profile_links = [link.get_attribute("href") for link in friends_links]
        self.save_to_csv(profile_links, "profile_links.csv")

    def extract_contact_info(self):
        # Placeholder: Extract contact information (emails, phone numbers) from profiles
        # Example: Use XPath to locate email and phone number elements
        # Example: Extract relevant data and save to a CSV file using save_to_csv method
        pass

    def scrape_comments(self, post_url):
        self.navigate_to(post_url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Comment"]')))
        comment_elements = self.driver.find_elements(By.XPATH, '//div[@aria-label="Comment"]')
        comments_data = []
        for comment in comment_elements:
            author = comment.find_element(By.CSS_SELECTOR, "a[role='link']").text
            text = comment.find_element(By.CSS_SELECTOR, "span[dir='auto']").text
            timestamp = comment.find_element(By.CSS_SELECTOR, "abbr").get_attribute("title")
            comments_data.append([author, text, timestamp])
        self.save_to_csv(comments_data, "comments.csv")

    def save_to_csv(self, data, file_name):
        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in data:
                # Ensure the row is a list so that writerow writes it as a single string
                if isinstance(row, str):
                    row = [row]
                writer.writerow(row)

# Main execution
if __name__ == "__main__":
    config.read('settings.ini')
    driver = webdriver.Chrome()
    fb_scraper = FacebookScraper(driver)

    fb_scraper.login(config['Facebook']['username'], config['Facebook']['password'])

    # Navigate to the specific profile URL
    profile_url = 'https://www.facebook.com/profile.php?id=61555203757147'
    fb_scraper.navigate_to(profile_url)

    # Extract profile links from the current profile page
    fb_scraper.extract_profile_links()

    driver.quit()
