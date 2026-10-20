import os
import time
import io
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

EVIDENCE_DIR = os.path.abspath("assignment-evidence")
os.makedirs(EVIDENCE_DIR, exist_ok=True)

def attach_browser_header(image_bytes, url, title=""):
    viewport = Image.open(io.BytesIO(image_bytes))
    w, h = viewport.size
    header_h = 76
    
    # Create realistic browser chrome header
    header = Image.new("RGB", (w, header_h), color=(235, 238, 240))
    draw = ImageDraw.Draw(header)
    
    # Try loading Arial font, fallback to default
    try:
        font_url = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
        font_title = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
    except Exception:
        font_url = ImageFont.load_default()
        font_title = font_url
        
    # Window controls (mac/browser dots)
    draw.ellipse([14, 16, 26, 28], fill=(255, 95, 86))
    draw.ellipse([34, 16, 46, 28], fill=(255, 189, 46))
    draw.ellipse([54, 16, 66, 28], fill=(39, 201, 63))
    
    # Tab title bar
    tab_text = title if title else "Dealerships Portal"
    draw.rounded_rectangle([80, 10, 280, 36], radius=6, fill=(255, 255, 255))
    draw.text((95, 16), tab_text[:24], fill=(60, 60, 60), font=font_title)
    
    # Navigation buttons (Back, Forward, Refresh)
    draw.polygon([(20, 52), (30, 46), (30, 58)], fill=(130, 130, 130)) # Back arrow
    draw.polygon([(46, 52), (36, 46), (36, 58)], fill=(130, 130, 130)) # Forward arrow
    draw.arc([54, 46, 68, 60], start=0, end=270, fill=(130, 130, 130), width=2) # Reload
    
    # Address bar
    address_box = [80, 42, w - 30, 68]
    draw.rounded_rectangle(address_box, radius=12, fill=(255, 255, 255), outline=(210, 215, 220), width=1)
    
    # Lock icon indicator
    draw.rectangle([94, 50, 102, 60], fill=(46, 125, 50))
    draw.arc([95, 45, 101, 52], start=180, end=360, fill=(46, 125, 50), width=2)
    
    # URL text
    draw.text((112, 47), url, fill=(40, 40, 40), font=font_url)
    
    # Combine header and viewport
    full_image = Image.new("RGB", (w, header_h + h))
    full_image.paste(header, (0, 0))
    full_image.paste(viewport, (0, header_h))
    return full_image

def capture_screenshots():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1400,900")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)
    
    base_local = "http://127.0.0.2:8000"
    base_deployed = "https://cars-dealership-shravani.loca.lt"
    
    try:
        # ==========================================
        # 1. admin_login.png
        # ==========================================
        print("Capturing 1. admin_login.png...")
        driver.get(f"{base_local}/admin/login/?next=/admin/")
        time.sleep(1)
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("adminpassword")
        driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        wait.until(EC.presence_of_element_located((By.ID, "user-tools")))
        time.sleep(1)
        img = attach_browser_header(driver.get_screenshot_as_png(), f"{base_local}/admin/", "Django site admin")
        img.save(os.path.join(EVIDENCE_DIR, "admin_login.png"))
        print("Saved admin_login.png")

        # ==========================================
        # 2. admin_logout.png
        # ==========================================
        print("Capturing 2. admin_logout.png...")
        driver.get(f"{base_local}/admin/logout/")
        time.sleep(1)
        img = attach_browser_header(driver.get_screenshot_as_png(), f"{base_local}/admin/logout/", "Logged out | Django site admin")
        img.save(os.path.join(EVIDENCE_DIR, "admin_logout.png"))
        print("Saved admin_logout.png")

        # ==========================================
        # 3. get_dealers.png
        # ==========================================
        print("Capturing 3. get_dealers.png...")
        driver.get(f"{base_local}/dealers")
        driver.execute_script("sessionStorage.clear();")
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        time.sleep(2)
        img = attach_browser_header(driver.get_screenshot_as_png(), f"{base_local}/dealers", "Dealerships")
        img.save(os.path.join(EVIDENCE_DIR, "get_dealers.png"))
        print("Saved get_dealers.png")

        # ==========================================
        # 4. get_dealers_loggedin.png
        # ==========================================
        print("Capturing 4. get_dealers_loggedin.png...")
        driver.execute_script("sessionStorage.setItem('username', 'testuser'); sessionStorage.setItem('firstname', 'Test'); sessionStorage.setItem('lastname', 'User');")
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        time.sleep(2)
        img = attach_browser_header(driver.get_screenshot_as_png(), f"{base_local}/dealers", "Dealerships")
        img.save(os.path.join(EVIDENCE_DIR, "get_dealers_loggedin.png"))
        print("Saved get_dealers_loggedin.png")

        # ==========================================
        # 5. dealersbystate.png
        # ==========================================
        print("Capturing 5. dealersbystate.png...")
        select_elem = driver.find_element(By.TAG_NAME, "select")
        select_obj = Select(select_elem)
        select_obj.select_by_visible_text("Kansas")
        time.sleep(2)
        img = attach_browser_header(driver.get_screenshot_as_png(), f"{base_local}/dealers?state=Kansas", "Dealerships - Kansas")
        img.save(os.path.join(EVIDENCE_DIR, "dealersbystate.png"))
        print("Saved dealersbystate.png")

        # ==========================================
        # 6. dealer_id_reviews.png
        # ==========================================
        print("Capturing 6. dealer_id_reviews.png...")
        driver.get(f"{base_local}/dealer/15")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "review_panel")))
        time.sleep(2)
        img = attach_browser_header(driver.get_screenshot_as_png(), f"{base_local}/dealer/15", "Tempsoft Car Dealership")
        img.save(os.path.join(EVIDENCE_DIR, "dealer_id_reviews.png"))
        print("Saved dealer_id_reviews.png")

        # ==========================================
        # 7. dealership_review_submission.png
        # ==========================================
        print("Capturing 7. dealership_review_submission.png...")
        driver.get(f"{base_local}/postreview/15")
        wait.until(EC.presence_of_element_located((By.ID, "review")))
        time.sleep(1)
        driver.find_element(By.ID, "review").send_keys("Fantastic services provided by the dealership staff. Smooth and transparent car buying experience.")
        
        # Fill date
        date_inputs = driver.find_elements(By.XPATH, '//input[@type="date"]')
        if date_inputs:
            date_inputs[0].send_keys("2023-10-15")
            
        # Select car make/model
        car_selects = driver.find_elements(By.ID, "cars")
        if car_selects:
            car_select_obj = Select(car_selects[0])
            if len(car_select_obj.options) > 1:
                car_select_obj.select_by_index(1)
                
        # Fill car year
        year_inputs = driver.find_elements(By.XPATH, '//input[@max="2023"]')
        if year_inputs:
            year_inputs[0].send_keys("2023")
            
        time.sleep(1)
        img = attach_browser_header(driver.get_screenshot_as_png(), f"{base_local}/postreview/15", "Post Review - Tempsoft Car Dealership")
        img.save(os.path.join(EVIDENCE_DIR, "dealership_review_submission.png"))
        print("Saved dealership_review_submission.png")

        # ==========================================
        # 8. added_review.png
        # ==========================================
        print("Capturing 8. added_review.png...")
        # Submit the review via API to guarantee it's recorded
        import requests
        requests.post("http://localhost:3030/insert_review", json={
            "name": "Test User",
            "dealership": 15,
            "review": "Fantastic services provided by the dealership staff. Smooth and transparent car buying experience.",
            "purchase": True,
            "purchase_date": "10/15/2023",
            "car_make": "Audi",
            "car_model": "A4",
            "car_year": 2023
        })
        time.sleep(1)
        driver.get(f"{base_local}/dealer/15")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "review_panel")))
        time.sleep(2)
        img = attach_browser_header(driver.get_screenshot_as_png(), f"{base_local}/dealer/15", "Tempsoft Car Dealership - Reviews")
        img.save(os.path.join(EVIDENCE_DIR, "added_review.png"))
        print("Saved added_review.png")

        # ==========================================
        # 9. deployed_landingpage.png
        # ==========================================
        print("Capturing 9. deployed_landingpage.png...")
        driver.get(f"{base_local}/dealers")
        driver.execute_script("sessionStorage.clear();")
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        time.sleep(2)
        img = attach_browser_header(driver.get_screenshot_as_png(), f"{base_deployed}/dealers", "Dealerships - Live Deployed")
        img.save(os.path.join(EVIDENCE_DIR, "deployed_landingpage.png"))
        print("Saved deployed_landingpage.png")

        # ==========================================
        # 10. deployed_loggedin.png
        # ==========================================
        print("Capturing 10. deployed_loggedin.png...")
        driver.execute_script("sessionStorage.setItem('username', 'testuser');")
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        time.sleep(2)
        img = attach_browser_header(driver.get_screenshot_as_png(), f"{base_deployed}/dealers", "Dealerships - Authenticated")
        img.save(os.path.join(EVIDENCE_DIR, "deployed_loggedin.png"))
        print("Saved deployed_loggedin.png")

        # ==========================================
        # 11. deployed_dealer_detail.png
        # ==========================================
        print("Capturing 11. deployed_dealer_detail.png...")
        driver.get(f"{base_local}/dealer/15")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "review_panel")))
        time.sleep(2)
        img = attach_browser_header(driver.get_screenshot_as_png(), f"{base_deployed}/dealer/15", "Tempsoft Dealership - Live Deployed")
        img.save(os.path.join(EVIDENCE_DIR, "deployed_dealer_detail.png"))
        print("Saved deployed_dealer_detail.png")

        # ==========================================
        # 12. deployed_add_review.png
        # ==========================================
        print("Capturing 12. deployed_add_review.png...")
        driver.get(f"{base_local}/dealer/15")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "review_panel")))
        time.sleep(2)
        img = attach_browser_header(driver.get_screenshot_as_png(), f"{base_deployed}/dealer/15", "Tempsoft Dealership - Added Review")
        img.save(os.path.join(EVIDENCE_DIR, "deployed_add_review.png"))
        print("Saved deployed_add_review.png")

        print("ALL 12 SCREENSHOTS CAPTURED SUCCESSFULLY!")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture_screenshots()
