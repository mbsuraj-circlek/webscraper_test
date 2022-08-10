from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
import time
import pandas as pd

def get_options():
    # PROXY_STR = "111.222.111.222:1234"
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--incognito")
    # options.add_argument('--proxy-server=%s' % PROXY_STR)
    # options.add_argument("user-agent=THis")
    # options.add_argument("--headless")
    options.add_argument("disk-cache-size=0")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return options
driver = webdriver.Chrome(options=get_options())
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = "https://www.7-eleven.com/"
driver.get(url)
time.sleep(2)
# food_elem = driver.find_element(by=By.XPATH, value='//*[@id="navigation"]/li[2]/a')
# food_elem_value = food_elem.text
# food_elem.click()
# bakery_elem = driver.find_element(by=By.XPATH, value='//*[@id="sub-navitation-0"]/li[2]/a')
# bakery_elem_value = bakery_elem.text
# bakery_elem.click()


order7nowdelivery_elem = driver.find_element(by=By.XPATH, value='//*[@id="navigation"]/li[5]/a')
order7nowdelivery_elem.click()
driver.switch_to.window(driver.window_handles[1])

search_elem = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div[1]/div/section[2]/div[1]/div/input')
search_elem.send_keys("Milk\n")

prod_descrip_title_elems = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/search-results/")]//div[@class="product-description-title"]')
prod_descrip_size_elems = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/search-results/")]//div[@class="product-description-size"]')
prod_descrip_min_price_elems = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/search-results/")]//span[contains(@class, "from")]')

prod_descr_title = [x.text for x in prod_descrip_title_elems]
prod_descr_size = [x.text.lower().replace("size: ", "") for x in prod_descrip_size_elems]
prod_descr_min_price = [x.text.lower().replace("from $", "") for x in prod_descrip_min_price_elems]

output_dict = {
    "product_title": prod_descr_title,
    "product_size": prod_descr_size,
    "product_min_price": prod_descr_min_price
}

output_df = pd.DataFrame(data=output_dict)
output_df.to_csv("7_eleven_milk_products.csv", index=False)