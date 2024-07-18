from selenium.webdriver.chrome.options import Options   
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import logging


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/api/link_aadhar_status', methods=['POST'])
def link_aadhar_status():
    logger.info('Received request to link Aadhar status')
    
    data = request.json
    logger.debug(f'Request JSON data: {data}')

    pan = data.get('pan')
    aadhaar = data.get('aadhaar')

    if not pan or not aadhaar:
        return jsonify({'error': 'PAN and Aadhaar are required fields.'}), 400

    # Setup Selenium and open the webpage
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    

    capabilities = {
        "browserName": "chrome",
        "unexpectedAlertBehaviour": "accept"  
        }

    try:
        
       
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
            desired_capabilities=capabilities
        )
        driver.get("https://eportal.incometax.gov.in/iec/foservices/#/pre-login/link-aadhaar-status")
        logger.debug('Navigated to Aadhaar linking status page')

        # Wait for the page to load and elements to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mat-input-0')))

        # Fill in the PAN and Aadhaar details
        pan_input = driver.find_element(By.ID, 'mat-input-0')
        aadhaar_input = driver.find_element(By.ID, 'mat-input-1')

        pan_input.send_keys(pan)
        aadhaar_input.send_keys(aadhaar)
        aadhaar_input.send_keys(Keys.RETURN)

       
        for _ in range(3):  
            try:
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                logger.debug('Alert accepted')
                break  # Exit the loop if alert is successfully handled
            except:
                pass  # No alert found, continue
     
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="maincontentid"]/app-link-aadhaar-status/div[1]/div/div[2]/form/div[2]/div/button[1]')))
        view_status_button = driver.find_element(By.XPATH, '//*[@id="maincontentid"]/app-link-aadhaar-status/div[1]/div/div[2]/form/div[2]/div/button[1]')
        view_status_button.click()
        logger.debug('Clicked on View Link Aadhaar Status button')
        
        for _ in range(3):  
            try:
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                logger.debug('Alert accepted after clicking button')
                break  
            except:
                pass  

       
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ng-star-inserted')))

    
        response_message = driver.find_element(By.CLASS_NAME, 'ng-star-inserted').text
        logger.info(f'Response message received: {response_message}')
        return jsonify({'message': response_message})

    except Exception as e:
        logger.error(f'Error occurred: {str(e)}')
        return jsonify({'error': str(e)}), 500

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

