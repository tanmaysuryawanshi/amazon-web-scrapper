import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

st.set_page_config("Amazon Web Scrapper",layout="wide")


def main():
    st.title("Amazon Web Scraper")
    url = st.text_input("Enter the URL of the product on Amazon:")
    if st.button("Scrape"):
        if url:
            product_data = scrape_amazon_product_data(url)
            if product_data:
                st.write(product_data)
            else:
                st.write("Error: Unable to scrape the product data.")
        else:
            st.write("Please enter a valid Amazon product URL.")


def scrape_amazon_product_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the desired data from the soup object
        # Example: Extracting the product title
        title = soup.find("span", attrs={"id": "productTitle"}).get_text().strip()

        # Create a dictionary with the scraped data
        
     
        ratings = soup.find("span", {"class": "a-icon-alt"}).get_text()
        mrp = soup.find("span", attrs={"class": "a-offscreen"}).get_text().strip()
        #ratings = soup.find("span", attrs={"class": "a-size-base a-color-base"}).get_text().strip()
        #ratings = soup.select('a-size-base a-color-base')[0].get_text().split(' ')[0].replace(".", "")
        #asin = soup.find("span", {"id": "ASIN"}).get_text()
        review_count = soup.select('#acrCustomerReviewText')[0].get_text().split(' ')[0].replace(".", "")
        
        #common_containers = soup.findAll("li", {"class":"s-result-item celwidget "})

        try:
            soup.select('#availability .a-color-state')[0].get_text().strip()
            stock = 'Out of Stock'
        except:
            stock = 'Available'

        product_data = {
            "Product Name": title,
         
            "status":stock,
           
             "Mrp":mrp,
            #"Rating":ratings,
            #"asin":common_containers[3],
            "Reviews":review_count

            
        }
       
        return product_data
    except requests.exceptions.HTTPError as errh:
        st.write(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        st.write(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        st.write(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        st.write(f"An error occurred: {err}")
    except Exception as e:
        st.write(f"An error occurred: {e}")


if __name__ == "__main__":
    main()