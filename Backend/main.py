from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


load_dotenv()
app = FastAPI()

app.mount("/static", StaticFiles(directory="Frontend"), name="static")

api_keyf = os.getenv("FIRECRAWL_API")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

model = FirecrawlApp(api_key=api_keyf)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict it later
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
@app.get("/")
async def read_index():
    return FileResponse(os.path.join("Frontend", "index.html"))

class URLRequest(BaseModel):
    url: str

class SourceMaterialSchema(BaseModel):
    summary: str
    key_points: str
    content_type: str 



@app.post("/processText/")
async def process_text(request: URLRequest):
    url = request.url
    result = model.extract(
        [ url],
     {
        'prompt': (
            "Read the content and extract: "
            "1. A brief summary of what the page is about, "
            "2. Key points or highlights, "
            "3. What kind of content it is (e.g., document, research data, blog draft, product specs, course outline)."
        ),
        'schema': SourceMaterialSchema.model_json_schema()
    }
    )
    x = result["data"]["summary"]
    y = result["data"]["key_points"]
    summary = x + " " + y

    # Chrome options for visible headless
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,1024")

    # Launch browser
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    try:
        # 1. Go to the login page
        driver.get("https://app.getalai.com")
        print("Opened:", driver.current_url)

        wait = WebDriverWait(driver, 20)

        # 2. Click on the email sign-in button (anchor tag)
        email_login_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@href, '#auth-sign-in')]")
        ))
        email_login_btn.click()
        print("Clicked Email Sign-In")

        # 3. Enter email
        email_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@id='email']")
        ))
        email_input.send_keys(email)
        print("Entered Email")

        # 4. Enter password
        password_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@id='password']")
        ))
        password_input.send_keys(password)
        print("Entered Password")

        # 5. Click Sign In
        sign_in_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit' and contains(text(), 'Sign in')]")
        ))
        sign_in_btn.click()
        print("Clicked Sign In")

        # 6. Wait and take screenshot
        time.sleep(5)

        # Step 6: Click "Create new presentation"
        create_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//span[contains(text(), 'Create new presentation')]"
        )))
        create_button.click()
        print("Clicked: Create new presentation")
        time.sleep(5)

        big_create_ai_box = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[contains(@class, 'rt-Box') and contains(@style, 'cursor: pointer')]"
        )))
        big_create_ai_box.click()
        print("Clicked: Big 'Create With AI' area")


        # Step 7: Click the dropdown
        dropdown_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[@role='combobox']"
        )))
        dropdown_button.click()

        # Step 2: Wait and select "2-5 slides" option
        # Replace '2-5 slides' with exact text from the dropdown (case sensitive)
        option = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//span[contains(text(), '2-5 slides')]"
        )))
        option.click()
        print("Selected: 2-5 slides")

        # Step 8: Wait for textarea
        textarea = wait.until(EC.presence_of_element_located((
            By.XPATH, "//textarea[contains(@placeholder, 'Paste your source')]"
        )))
        textarea.send_keys(summary)
        print("Pasted text into textarea")

        edit_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(text(), 'Review & Edit Outline')]"
        )))
        edit_btn.click()
        print("Clicked Review & Edit Outline")
        time.sleep(20)

        # Step 9: Click "Calibrate Tone & Verbosity"
        calibrate_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(text(), 'Calibrate Tone & Verbosity')]"
        )))
        calibrate_btn.click()
        print("Clicked Calibrate Tone & Verbosity")
        time.sleep(10)

        # Step 10: Click "Generate Slide"
        generate_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(text(), 'Generate Slide')]"
        )))
        generate_btn.click()
        print("Clicked Generate Slide")
        time.sleep(30)

        # Step 11: Final Screenshot
        driver.save_screenshot("final_result.png")
        print("Saved final_result.png")

        share_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class, 'rt-variant-surface') and contains(@class, 'rt-Button') and @aria-haspopup='dialog']"
        )))

        share_button.click()
        print("Clicked share button")
        # time.sleep(2)

        driver.save_screenshot("fafter share.png")



        # Wait for the dialog to appear (this ensures modal is fully loaded)
        # Step 2: Wait for the dialog to appear with "Share Presentation" header
        # wait.until(EC.presence_of_element_located((
        #     By.XPATH, "//div[@role='dialog' and .//h1[contains(text(), 'Share Presentation')]]"
        # )))

        # Step 3: Now locate and click the "Generate Share Link" button inside the dialog
        generate_link_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[@role='dialog']//button[contains(text(), 'Generate Share Link')]"
        )))
        generate_link_button.click()
        print("Clicked Generate Share Link")

        # Step 4: Wait for the input field with the generated link
        share_link_input = wait.until(EC.presence_of_element_located((
            By.XPATH, "//div[@role='dialog']//input[@readonly and contains(@value, 'https://app.getalai.com/view/')]"
        )))

        # Extract the value (URL) from the input field
        shareable_link = share_link_input.get_attribute("value")
        print("Extracted Shareable Link:", shareable_link)

        return {"query_received": url, "response": shareable_link}




    finally:
        driver.quit()

        # return {"query_received": url, "response": result}
    
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=True)

    