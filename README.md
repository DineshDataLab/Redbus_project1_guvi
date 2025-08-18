🚌 BusGrid: RedBus Data Scraper & Interactive Bus Explorer

A Python project that scrapes bus route data from RedBus for multiple state transport corporations in India using Selenium, stores it in a MySQL database, and displays it in an interactive Streamlit web app with dynamic filtering options.

✨ Features

📝 Bus Details Scraping:

Bus name, type, departing & arriving times

Duration, price, available seats

Star ratings (if available)

🌏 Supports multiple state transport corporations in India.

🔄 Handles dynamic content including lazy loading and pagination.

🖥️ Interactive Streamlit Dashboard with:

State & route selection

Multi-option filters: ❄️ AC, 🪟 Non-AC, 🛌 Sleeper, 💺 Seater, 🌟 Luxury, ⚡ Electric, 🏛️ Government, 🏢 Private, ⭐ Highly Rated, 🌞 Day Travel, 🌙 Night Travel

Price range slider

Real-time display of filtered buses

🗄️ MySQL Database Integration for storing and querying bus data efficiently.

🛠️ Technologies Used

Python

Selenium – Web scraping with dynamic scrolling & element handling

Streamlit – Interactive web UI for filtering & visualization

MySQL – Database for storing extracted bus data

Pandas – Data manipulation & storage

🚀 Installation

Clone the repository:

git clone <your-repo-url>
cd <repo-folder>


Install required Python packages:

pip install pandas selenium streamlit mysql-connector-python


Set up MySQL database:

Create a database named bus_details.

Ensure table bus_routes exists with relevant columns for bus data.

Update credentials in the Python script if needed.

⚡ Usage

Run the scraping script to populate the database:

python your_scraper_script.py


Scrapes bus data for all specified states from RedBus.

Run the Streamlit app for interactive exploration:

streamlit run your_scraper_script.py


Open the displayed link in your browser to explore the dashboard.

🔍 How It Works

Data Scraping:

Selenium navigates through each state’s RedBus page.

Handles scrolling, lazy-loading, and government/private bus listings.

Extracts bus details: name, type, timings, duration, rating, price, seats.

Database Storage:

Stores extracted data in MySQL.

Streamlit fetches filtered data from MySQL in real-time.

Interactive Dashboard:

Users select state and route.

Apply filters and price range.

View buses dynamically in a responsive table.

“Go back” buttons allow easy navigation between states and routes.

📂 Project Structure

your_scraper_script.py – Main scraping + Streamlit app

DATA – Temporary storage dictionary for bus info

GOVT_LINKS – Mapping of state names to RedBus URLs

⚠️ Notes

Make sure Google Chrome is installed for Selenium WebDriver.

Handles exceptions and missing data gracefully (e.g., buses without ratings).

Interactive filtering supports: ❄️ AC, 🪟 Non-AC, 🛌 Sleeper, 💺 Seater, 🌟 Luxury, ⚡ Electric, 🏛️ Government, 🏢 Private, ⭐ Highly Rated, 🌞 Day Travel, 🌙 Night Travel.

📷 Screenshots / Demo

(You can add screenshots of your Streamlit dashboard here for better presentation.)

📝 License

This project is open source and free to use for educational purposes.

If you want, Dinesh, I can also add color-coded emojis for database, filtering, and scraping sections to make it even more visually fun and easy to skim.

Do you want me to do that next?

Tools
ChatGPT can make mistakes. Check important info. See Cookie Preferences.
