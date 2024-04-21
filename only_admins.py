import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import requests
import os
from selenium.webdriver.common.keys import Keys
import urllib.request


# Load credentials
credentials = {}
with open('facebook_credentials.txt') as file:
    for line in file:
        key, value = line.strip().split('=')
        credentials[key] = value
user_ids = []
id = "355575617485053"
access_token = "EAAGfynRZCFqIBO1GErZASVr48Vn7qJm01o4U8YKdWNclHFE52F0fCbos62pAsXU7cvk9JLx6yG0oefdOcWCZA4538W9ZBAjiJPbQ3RlOOcLy8U0TfaSA6Hcvhzaxibp8qo1ZAb7nlPeOKc7epiozMx5nWqJAQkT4ZAbzk9CrIkTeIlcTDQ2ZB81m2mUA3MySfJpxHZCyKwMKRZAogcxp0y0Ai8RJ3HX6wI0aKeDwUHzZBZBRuNpbZCZAvexgy"
# Initialize WebDriver
chrome_driver_path = r'C:\Users\yusra Ashfaq\Desktop\Facebook scrapper\chromedriver-win64\chromedriver.exe'
service = Service(executable_path=chrome_driver_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(service=service, options=chrome_options)


# chrome_options = webdriver.ChromeOptions()
# chrome_options.page_load_strategy = 'normal'
# prefs = {"profile.default_content_setting_values.notifications": 2}
# chrome_options.add_experimental_option("prefs", prefs)
# driver = webdriver.Chrome(options=chrome_options)
# Function definitions (Aboutinfo, contactinfo, extract_image_links, extract_name) go here
def Aboutinfo():
    profile_info = {
        "Workplace": [],
        "Studies": "Not provided",
        "Lives in": "Not provided",
        "From": "Not provided"
    }

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='x1hq5gj4']//span[@dir='auto']"))
        )
        text_elements = driver.find_elements(By.XPATH, "//div[@class='x1hq5gj4']//span[@dir='auto']")
        
        for element in text_elements:
            text = element.text.strip()
            if " and " in text or "Works at" in text or " at" in text or " works" in text:
                profile_info["Workplace"].append(text)
            # if text.startswith("Works at"):
            #     profile_info["Workplace"] = text.replace("Works at", "").strip()
            elif text.startswith("Studied at") or text.startswith("Studies at"):
                profile_info["Studies"] = text.replace("Studied at", "").replace("Studies at", "").strip()
            elif text.startswith("Lives in"):
                profile_info["Lives in"] = text.replace("Lives in", "").strip()
            elif text.startswith("From"):
                profile_info["From"] = text.replace("From", "").strip()

    except TimeoutException:
        print("Timed out waiting for page to load")

    # return [profile_info[key] for key in ["Workplace","Studies", "Lives in", "From"]]
    return [profile_info[key] if profile_info[key] else "Not provided" for key in ["Workplace", "Studies", "Lives in", "From"]]

# contacts
def contactinfo(heading_text):
    try:
        contact_and_basic_info_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'about_contact_and_basic_info')]"))
        )
        contact_and_basic_info_link.click()

        heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{heading_text}')]"))
        )
        # The section containing the links and text you're interested in is the sibling of the heading
        section = heading.find_element(By.XPATH, "./following-sibling::div | ./following::div")

        # Initialize an empty list to hold the text and links
        content = []

        # Extracting text
        texts = section.find_elements(By.XPATH, ".//span[not(a)]")
        for text in texts:
            content.append(text.text)

        # Extracting links
        links = section.find_elements(By.XPATH, ".//a")
        for link in links:
            # Getting the text and href for each link
            link_text = link.text
            link_href = link.get_attribute('href')
            content.append(f"{link_text}: {link_href}")

        return content if content else ["No information to show"]
    except NoSuchElementException:
        return ["Information not found"]
def extract_image_links(name):
    # cover_image_link = ''
    # profile_image_link = ''

    cover_image_link = None
    profile_image_link = None

    try:
        # Find the profile cover image element using XPath and get its src attribute
        cover_img_element = driver.find_element(By.XPATH, "//img[@data-imgperflogname='profileCoverPhoto']")
        cover_image_link = cover_img_element.get_attribute("src")
        # Construct the path for the cover image dynamically
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        imgs_path = os.path.join(desktop_path, "imgs")
        os.makedirs(imgs_path, exist_ok=True)  # Ensure the directory exists
        cover_image_path = os.path.join(imgs_path, f"{name}_cover.jpg")
        urllib.request.urlretrieve(cover_image_link, cover_image_path)
        print("Cover image link extracted:", cover_image_link)
        # urllib.request.urlretrieve(cover_image_link, f"C:\\Users\\yusra Ashfaq\\Desktop\\imgs\\{name}_cover.jpg")
        current = driver.current_url
        # Find the profile image element using XPath and get its src attribute
        element = driver.find_element(By.XPATH,f"//a[@aria-label='{name}']")
    except NoSuchElementException:
        print(f"Cover image of {name} is not found.")
    

    try:
# Get the value of the href attribute
        href_value = element.get_attribute("href")
        driver.get(href_value)
        img_element = driver.find_element(By.XPATH, "//img[@data-visualcompletion='media-vc-image']")
        profile_image_link = img_element.get_attribute("src")
        print("Profile image link extracted:", profile_image_link)

        # Construct the path for the profile image dynamically
        profile_image_path = os.path.join(imgs_path, f"{name}_profile.jpg")
        urllib.request.urlretrieve(profile_image_link, profile_image_path)

    except NoSuchElementException:
        print(f"Profile image of {name} is not found.")

    return cover_image_link, profile_image_link
def extract_name():
    try:
        # Assuming the first h1 tag within a span with dir="auto" consistently contains the name.
        name_element_xpath = "//div[contains(@class, 'x1e56ztr')]//span[contains(@class, 'x193iq5w')]/h1"
        name_element = driver.find_element(By.XPATH, name_element_xpath)
        name = name_element.text.strip()
        if name:
            print("Name extracted:", name)
            return name
        else:
            
            print("Found the name element, but it contains no text.")
            return "Name not provided"
    except NoSuchElementException as e:
       
        print("Name element not found:", e)
        return "Name not provided"

def append_data_to_csv(file_path, data):
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:  # Append mode
        writer = csv.writer(file)
        writer.writerow(data)

def login():
    driver.get("http://www.facebook.com")
    driver.maximize_window()
    username = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='Email address or phone number']")))
    password = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='Password']")))
    username.clear()
    username.send_keys("ireg.member67@gmail.com")
    password.clear()
    password.send_keys("ZXCVB@123")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    time.sleep(10)
    print(" Log in Successfully!")

def navigate_to_group():
    group_url = "https://www.facebook.com/groups/localbusinessownersusa/"
    driver.get(group_url)
    time.sleep(5)  
def click_see_all():
        try:
            
            
            # Wait for the "See All" button to be clickable, and then click it
            see_all_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='See All']"))
        )
            if see_all_button:
                see_all_button.click()  # Click the button if it's found and clickable.
                time.sleep(2)  # Allow time for the page to react to the click.
                return True
            else:
                print ("No 'See All' button found or clickable.")
                return False
        except TimeoutException as e:
            print(f"Timeout when trying to click 'See All': {str(e)}")
            return False
        except Exception as e:
            print(f"An error occurred while trying to click 'See All': {str(e)}")
            return False
        
def collect_admins_data():
        admins_data_set = set()
        people = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='People']"))
        )
        ActionChains(driver).move_to_element(people).click().perform()
        time.sleep(5)  # Wait for the page to load
        driver.execute_script("window.scrollBy(0, 900);")
        time.sleep(2) 
        print("At members page....")

        clicked_see_all = click_see_all()
        if clicked_see_all:
            print("Collecting expanded admins data...")
            time.sleep(5) 
        else:
            print("Collecting visible admins data...")

        
        
        list_container = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='list']"))
        )
        admin_elements = list_container.find_elements(By.CSS_SELECTOR, "a[role='link']")  # Adjust as needed
       
        for element in admin_elements:
            link = element.get_attribute('href')
            if link: 
                admins_data_set.add(link)  # Add to set, duplicates are ignored

        # Convert the set to a list for iteration
        admins_data_list = list(admins_data_set)

        print(f"Number of Unique Admins Found: {len(admins_data_list)}")
        for link in admins_data_list:
            print(link)

        return admins_data_list
    
def process_admin(admin_data):
            try:
                    driver.get(admin_data)# Directly navigate to admin's profile
                    
                    # View profile
                    view_profile_button = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, "//span[text()='View profile']"))
                    )
                    driver.execute_script("arguments[0].click();", view_profile_button)
                    print("At view")
                    time.sleep(2)
                    # about
                    about_profile_button = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, "//span[text()='About']")))
                    driver.execute_script("arguments[0].click();", about_profile_button)
                    print("at about")
                    time.sleep(4)
                        # Scroll down a bit
                    driver.execute_script("window.scrollBy(0, 500);")  
                    time.sleep(2)
                    # Extract information and write to CSV
                    name = extract_name()
                    about_data = Aboutinfo()
                    contact_info_data = contactinfo("Contact info")
                    websites_and_links_data = contactinfo("Websites and social links")
                    basic_info_data = contactinfo("Basic info")
                    cover_image_link, profile_image_link = extract_image_links(name)
                        # Prepare the data row for the current member
                    admin_info = [
                            name,
                            ', '.join(about_data[0]) if isinstance(about_data[0], list) else about_data[0],
                            ', '.join(about_data[1]) if isinstance(about_data[1], list) else about_data[1],
                            ', '.join(about_data[2]) if isinstance(about_data[2], list) else about_data[2],
                            ', '.join(about_data[3]) if isinstance(about_data[3], list) else about_data[3],
                            ', '.join(websites_and_links_data) if isinstance(websites_and_links_data, list) else websites_and_links_data,
                            ', '.join(contact_info_data) if isinstance(contact_info_data, list) else contact_info_data,
                            ', '.join(basic_info_data) if isinstance(basic_info_data, list) else basic_info_data,
                            cover_image_link,
                            profile_image_link
                        ]
                    # admin_info = [
                    #         name,
                    #         about_data[0],
                    #         about_data[1],
                    #         about_data[2],
                    #         about_data[3],
                    #         websites_and_links_data,
                    #         contact_info_data,
                    #         basic_info_data,
                    #         cover_image_link,
                    #         profile_image_link
                    #     ]
                    append_data_to_csv(csv_file_path, admin_info)                            
            except Exception as e:
                print(f"An error occurred while processing {admin_data}: {e}")

def download_image(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved as {file_path}")
    else:
        print(f"Failed to download image from {url}")

def download_profile_images(user_id):
    # Fetch user's profile picture
    profile_picture_url = f"https://graph.facebook.com/{user_id}/picture?type=large"
    download_image(profile_picture_url, f"profile_picture_{user_id}.jpg")

    # Fetch user's cover photo
    cover_photo_url = f"https://graph.facebook.com/{user_id}?fields=cover&access_token={access_token}"
    response = requests.get(cover_photo_url)
    if response.status_code == 200:
        cover_photo_data = response.json().get('cover')
        if cover_photo_data:
            cover_photo_url = cover_photo_data['source']
            download_image(cover_photo_url, f"cover_photo_{user_id}.jpg")
        else:
            print(f"User {user_id} does not have a cover photo.")
    else:
        print(f"Failed to fetch cover photo for user {user_id}")
if __name__ == "__main__":
        try:
            login()
            navigate_to_group()
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            csv_file_path = os.path.join(desktop_path, "final.csv")

        # Ensuring the directory exists (in this case, the desktop path already exists, but you can create a new directory if needed)
            os.makedirs(desktop_path, exist_ok=True)
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Profile URL", "Workplace", "Studies", "Lives In", "From", "Websites and Links", "Contact Info", "Basic Info", "Cover Image Link", "Profile Image Link", "Profile Locked"])
            navigate_to_group()
            error_message = ""  # Initialize an empty error message
            try:
                admins_data = collect_admins_data()
                for admin_data in admins_data:
                    process_admin(admin_data)
            except Exception as e:
                error_message = str(e)  # Store the exception message

        finally:
                driver.quit()
                if error_message:  # If there was an error, update the status with it
                    print(f"A general error occurred: {error_message}")
                else:  # If no error, indicate scraping completed successfully
                    print("Scraping completed successfully.")


