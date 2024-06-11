# Flipkart Product Scraper

This project is a web scraper designed to extract product information from Flipkart's monitor category and store the data in a PostgreSQL database. 
The scraper uses Python with the `requests`, `BeautifulSoup`, and `threading` libraries for web scraping, and `psycopg2` for database interactions.

## Prerequisites

- Python 3.x
- PostgreSQL database
- Python libraries: `requests`, `beautifulsoup4`, `psycopg2`

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/flipkart-scraper.git
   cd flipkart-scraper
2. **Install the required Python libraries:**
   ```sh
   pip install requests beautifulsoup4 psycopg2
3. **Setup PostgreSQL:**
   ```sh
    Install PostgreSQL on your machine.
    Create a database for the project.
    Update the create_connection function in scraper.py with your database name, user, password, host, and port.

## Usage

1. **Run the scraper:**
   ```sh
   python scraper.py
2. **The scraper will:**
   ```sh
   Fetch product data from the specified Flipkart URLs using multi-threading.
   Store the scraped data in a PostgreSQL database table named 'products'.
