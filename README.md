BusGrid: RedBus Data Scraper & Interactive Bus Explorer

A Python project that scrapes bus route data from RedBus for various state transport corporations in India using Selenium, stores it in a MySQL database, and displays it in an interactive Streamlit web app with dynamic filtering options.

Features

Scrapes bus details including:

Bus name, type, departing & arriving times

Duration, price, available seats

Ratings (if available)

Supports multiple state transport corporations in India.

Handles dynamic content, lazy loading, and pagination.

Interactive Streamlit dashboard with:

State and route selection

Multi-option filters: AC, Non-AC, Sleeper, Seater, Luxury, Electric, Government, Private, Highly Rated, Day/Night travel

Price range slider

Real-time display of filtered buses

Connects to MySQL to store and query bus data efficiently.

Technologies Used

Python

Selenium – Web scraping with dynamic scrolling and element handling

Streamlit – Interactive web UI for filtering and visualization

MySQL – Storing extracted bus data

Pandas – Data manipulation and storage

Installation

Clone the repository:

git clone <your-repo-url>
cd <repo-folder>


Install required Python packages:

pip install pandas selenium streamlit mysql-connector-python


Set up MySQL database:

Create a database named bus_details.

Ensure table bus_routes exists with relevant columns for bus data.

Update connection credentials in the Python script if needed.

Usage

Run the scraping script to populate the database:

python your_scraper_script.py


This scrapes bus data for all specified states from RedBus.

Run the Streamlit app for interactive exploration:

streamlit run your_scraper_script.py


Open the displayed link in your browser to interact with the dashboard.

How It Works

Data Scraping:

Selenium navigates through each state’s RedBus page.

Handles scrolling, lazy-loading, and government/private bus listings.

Extracts bus details: name, type, timings, duration, rating, price, seats.

Database Storage:

Extracted data is stored in MySQL for efficient querying.

Streamlit fetches filtered data from MySQL in real-time.

Interactive Streamlit Dashboard:

Users can select state and route.

Apply filters and price range sliders.

View buses dynamically in a responsive table.

“Go back” buttons allow easy navigation between states and routes.

Project Structure

your_scraper_script.py – Main script for scraping and Streamlit app

DATA – Dictionary storing extracted bus information before DB insert

GOVT_LINKS – Dictionary mapping state names to RedBus URLs

Notes

Make sure Google Chrome is installed for Selenium WebDriver.

Handles exceptions and missing data gracefully (e.g., buses without ratings).

Interactive filtering allows exploration of AC, Non-AC, Sleeper, Luxury, Electric, Government, Private, Highly Rated, Day/Night travel buses.

License

This project is open source and free to use for educational purposes.
