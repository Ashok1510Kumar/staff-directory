import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_page(url):
    """
    Fetches and parses the content of a given URL to extract staff information.

    Args:
    url (str): The URL of the webpage to scrape.

    Returns:
    list: A list of dictionaries containing staff details.
    BeautifulSoup object: The BeautifulSoup object of the parsed HTML page for further use.
    """
    print(f"Scraping page: {url}")  # Debug: print the URL being scraped
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extracting dynamic school name
    school_name = soup.select_one('.site-name a').text.strip() if soup.select_one('.site-name a') else "School name not found"
    
    # List to store all staff data dictionaries
    staff_data = []
    # Find all staff member elements in the page
    staff_elements = soup.select('.node.staff.teaser')
    for staff in staff_elements:
        # Extract individual staff details and handle missing information gracefully
        address = staff.select_one('.field.locations .field-content span').text.strip() if staff.select_one('.field.locations .field-content span') else "Address not found"
        name = staff.select_one('.title').text.strip()
        # Assuming the name format is 'Last, First'
        first_name, last_name = name.split(', ')[1], name.split(', ')[0]
        job_title = staff.select_one('.field.job-title').text.strip()
        phone = staff.select_one('.field.phone a').text.strip()
        email = staff.select_one('.field.email a').text.strip()
        
        # Append a dictionary for each staff member to the list
        staff_data.append({
            "School Name": school_name,
            "Address": address,
            "State": "N/A",  # No dynamic extraction provided
            "Zip": "N/A",  # No dynamic extraction provided
            "First Name": first_name,
            "Last Name": last_name,
            "Title": job_title,
            "Phone": phone,
            "Email": email
        })
    
    return staff_data, soup

def main():
    """
    Main function to initiate scraping process.
    
    Continuously scrapes each page of the staff directory until there are no more pages left to scrape,
    then saves the data to a CSV file.
    """
    base_url = "https://isd110.org/our-schools/laketown-elementary/staff-directory"
    url = base_url
    total_data = []

    # Loop through all pages using pagination
    while url:
        data, soup = scrape_page(url)
        total_data.extend(data)
        next_page_link = soup.select_one('li.next a[rel="next"]')
        # Construct the next page URL if the link exists
        if next_page_link and 'href' in next_page_link.attrs:
            url = base_url + next_page_link['href']
            print(f"Next page URL: {url}")  # Debug: print the next page URL
        else:
            url = None  # Terminate if no more pages

    # Save all data to a CSV file
    if total_data:
        df = pd.DataFrame(total_data)
        df.to_csv('staff_directory.csv', index=False)
        print("Data collected and saved to CSV.")
    else:
        print("No data collected.")

if __name__ == "__main__":
    main()
