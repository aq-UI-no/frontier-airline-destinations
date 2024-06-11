import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Function to initialize selenium webdriver
def init_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

# Function to fetch flight data from Frontier Airlines website
def fetch_flight_data():
    driver = init_driver()
    url = "https://flights.flyfrontier.com/en/sitemap/city-to-city-flights/page-1"
    driver.get(url)

    # Wait for the dynamic content to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "route-map__destination")))

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    flights = []

    # Extracting the flight details
    destinations = soup.find_all('div', class_='route-map__destination')
    for destination in destinations:
        takeoff = destination.find('div', class_='takeoff').text
        landing = destination.find('div', class_='landing').text
        stops = destination.find('div', class_='stops').text
        stop_duration = destination.find('div', class_='stop-duration').text
        flight_duration = destination.find('div', class_='flight-duration').text
        ticket_price = destination.find('div', class_='ticket-price').text

        flights.append({
            'Takeoff': takeoff,
            'Landing': landing,
            'Stops': stops,
            'Stop Duration': stop_duration,
            'Flight Duration': flight_duration,
            'Ticket Price': ticket_price
        })

    return flights

# Fetch flight data
flight_data = fetch_flight_data()

# Convert to pandas DataFrame
df = pd.DataFrame(flight_data)

# Save to CSV
df.to_csv('frontier_airlines_flight_data.csv', index=False)

print("Flight data has been saved to frontier_airlines_flight_data.csv")
