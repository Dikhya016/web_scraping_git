import requests
from bs4 import BeautifulSoup
import threading
import psycopg2

#Here is the Function for scraping flipkart website product page
def scrape_flipkart(url):
    try:
        req = requests.get(url)             # Sending request to the web
        req.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    try:
        soup = BeautifulSoup(req.content, 'html.parser')     
        outer_cont = soup.find('div', attrs={'class': "DOjaWF gdgoEp"})   #I'm trying to find out main_product container class
        if not outer_cont:
            return []

        all_prods = outer_cont.find_all('div', attrs={'class': "_75nlfW"}) #getting each product container class
        products = []

        for each_div in all_prods:
            product_info = {}
            name = each_div.find('div', attrs={'class': "KzDlHZ"})
            price = each_div.find('div', attrs={'class': "Nx9bqj _4b5DiR"})
            rating = each_div.find('div', attrs={'class': "XQDdHH"})
            review = each_div.find('span', attrs={'class': "Wphh3N"})
            pro_url = each_div.find('div', attrs={'class': "tUxRFH"})
            
            if name:
                product_info['name'] = name.text
            if price:
                product_info['price'] = price.text[1:]
            if rating:
                product_info['rating'] = rating.text
            if review:
                product_info['review'] = review.text.split('&')[1].strip() if '&' in review.text else review.text
            if pro_url and pro_url.a:
                product_info['url'] = 'https://www.flipkart.com' + pro_url.a["href"]
            
            if product_info:
                products.append(product_info)           #Adding all the product information to to product list.
        
        return products

    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return []

# URLs to scrape
urls = [
    'https://www.flipkart.com/monitors/pr?sid=6bo,g0i,9no&page=1',
    'https://www.flipkart.com/monitors/pr?sid=6bo,g0i,9no&page=2'
]

# Here is the Function to scrape URLs using threading

def scrape_with_threads(urls):
    threads = []
    results = []
    lock = threading.Lock()  
    def worker(url):
        nonlocal results
        products = scrape_flipkart(url)
        with lock:
            results.extend(products)

    for url in urls:
        thread = threading.Thread(target=worker, args=(url,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return results

# Here Function to create a connection to the PostgreSQL database
def create_connection():
    try:
        connection = psycopg2.connect(                   # Settings/ Connecting Database
            dbname="your_database_name",
            user="postgres",
            password="your_password",
            host="localhost",
            port="your_port"
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# Here Function to create a table in the database
def create_table(connection):
    try:
        cursor = connection.cursor()                      # Creating table Schema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT,
                price TEXT,
                rating TEXT,
                review TEXT,
                url TEXT
            )
        """)
        connection.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")

# Here Function to insert scraped data into the database
def insert_data(connection, products):
    try:
        cursor = connection.cursor()
        for product in products:                                # Data stored in products that will add to the table 
            cursor.execute("""
                INSERT INTO products (name, price, rating, review, url)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                product.get('name', ''),
                product.get('price', ''),
                product.get('rating', ''),
                product.get('review', ''),
                product.get('url', '')
            ))
        connection.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")

#Here Main function to handle the database operations
def main():
    connection = None
    try:
        # Here Scrape URLs using threading
        all_products = scrape_with_threads(urls)
        
        # Create connection
        connection = create_connection()                  
        if connection is None:
            return
        
        # Create table
        create_table(connection)                        
        
        # Insert data
        insert_data(connection, all_products)               #Calling function for storing data to the table
        
        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

# For Execute main the function
if __name__ == "__main__":
    main()
