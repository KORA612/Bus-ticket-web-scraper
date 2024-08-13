import os
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import motor.motor_asyncio
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables
load_dotenv()

app = FastAPI()

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.bus_scraper
collection = db.search_results

class SearchQuery(BaseModel):
    origin: str
    destination: str
    date: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/search")
async def search_bus(query: SearchQuery):
    # Construct the URL
    url = f"https://safar724.com/bus/{query.origin}-{query.destination}?date={query.date}"
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver,60)
    driver.get(url)

    ticket_list = []
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
    
    print(ticket_list)    
    df = pd.DataFrame(ticket_list)
    df.to_csv('out.csv', sep='\t', encoding='utf-8', index=False, header=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)