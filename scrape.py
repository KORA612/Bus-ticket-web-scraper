import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver,120)

origin = "tehran"
destination = "tabriz"
date = "1403-5-15"

url = f"https://safar724.com/bus/{origin}-{destination}?date={date}"
driver.get(url)

ticket_list = []

# Wait for tickets to load
tickets = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ticketCard_ticket__7HRGj")))

for ticket in tickets:
    try:
        # Using XPath
        # time_hour = ticket.find_element(By.XPATH, ".//div[contains(@class, 'ticketAction_departureTime')]/p").text
        # empty_seats = ticket.find_element(By.XPATH, ".//div[contains(@class, 'ticketAction_seat')]/p").text
        # price_rial = ticket.find_element(By.XPATH, ".//div[contains(@class, 'ticketDetailBusInformation_busInformation')]/p").text

        # Alternatively, using CSS selectors
        time_departure = ticket.find_element(By.CSS_SELECTOR, "div.ticketAction_departureTime__LlKV9 > p").text
        empty_seats = ticket.find_element(By.CSS_SELECTOR, "div.ticketAction_seat__QP645 > p").text
        price_rial = ticket.find_element(By.CSS_SELECTOR, "div.ticketDetailBusInformation_busInformation__SJBAI > p").text

        ticket_item = {
            'time_departure': time_departure,
            'empty_seats': empty_seats,
            'price_rial': price_rial
        }
        ticket_list.append(ticket_item)

    except Exception as e:
        print(f"Error processing ticket: {e}")
        continue

driver.quit()

df = pd.DataFrame(ticket_list)
df.to_csv('out.csv', sep='\t', encoding='utf-8', index=False, header=True)