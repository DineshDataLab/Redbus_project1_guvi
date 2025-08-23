"""
Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit

This module scrapes bus route data from RedBus for various state 
transport corporations in India using Selenium, stores the data in a
MySQL database, and displays it in an interactive Streamlit web app 
with filtering options.

Modules used:
- time: for delays in scraping
- pandas: for data storage and manipulation
- selenium: for web scraping
- streamlit: for web app UI
- mysql.connector: for database operations
"""
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st
import mysql.connector
from sqlalchemy import create_engine

# Cache the scraped data to avoid re-scraping on every app reload
@st.cache_data 

# Function to scrape bus data from RedBus
def scrap_redbus_data():


    def extraction(x,y,z):

        """
        Extracts bus details from a route page and 
        appends them to the DATA dictionary.

        Parameters:
        x (str): State name.
        y (str): Route link.
        z (str): Route name.

        This function scrolls through the bus listings 
        on the page, collects details such as bus name, type, timing,
        duration, rating, price, and seat availability
        and stores them in the global DATA dictionary.
        """
        def scroll():

            """
            Scrolls through the bus listings page until 
            the end of the listings is reached
            or maximum scroll attempts are exceeded.
            """

            B = 0

            while True:

                BUSES = driver.find_elements(
                    By.XPATH,"//div[contains(@class,'travelsName___')]"
                )

                driver.execute_script(
                """
                arguments[0].scrollIntoView({behavior:'smooth',block:'center'});
                """,
                BUSES[-3]
                )

                time.sleep(5)

                try:

                    # Check if the end of listings is reached
                    driver.find_element(
                        By.XPATH, "//span[contains(@class,'end')]"
                    )

                    break

                except:

                    pass

                B += 1

                if B > 50:

                    break

        try:

            time.sleep(2)

            #scroll()

            #time.sleep(2)

            LE = driver.find_elements(
                By.XPATH,"//div[contains(@class , 'travelsName___')]"
            )

            # Get the total number of buses on the page
            LE = len(LE)

            # Append static data for each bus
            DATA['state'].extend([x]*(LE))

            DATA['route_link'].extend([y]*(LE))

            DATA['route_name'].extend([z]*(LE))

            # Append dynamic data for each bus
            DATA['busname'].extend([C.text for C in driver.find_elements(
                By.XPATH,"//div[contains(@class,'travelsName___')]"
                )])

            DATA['bustype'].extend([C.text for C in driver.find_elements(
                By.XPATH,"//p[contains(@class,'busType___')]"
                )])

            DATA['departing_time'].extend([C.text for C in driver.find_elements(
                By.XPATH,"//p[contains(@class,'boardingTime___')]"
                )])

            DATA['duration'].extend([C.text for C in driver.find_elements(
                By.XPATH,"//p[contains(@class,'duration___')]"
                )])

            DATA['reaching_time'].extend([C.text for C in driver.find_elements(
                By.XPATH,"//p[contains(@class,'droppingTime___')]"
                )])

            # Extract ratings
            MAINC = driver.find_elements(
                By.XPATH,"//div[contains(@class,'timeFareBoWrap___')]"
                )

            for L in MAINC:

                MAINC = driver.find_elements(
                    By.XPATH,"//div[contains(@class,'timeFareBoWrap___')]"
                    )
                
                try:

                    DATA['star_rating'].append(L.find_element(
                        By.XPATH, ".//div[contains(@class,'rating___')]"
                        ).text)
                    
                except:

                    DATA['star_rating'].append('No rating')

            # Extract price and seats available
            DATA['price'].extend(
                [
                (C.text).strip('₹')
                for C in driver.find_elements(
                    By.XPATH,"//p[contains(@class,'finalFare___')]"
                    )
                ]
            )
            
            DATA['seats_available'].extend(
                [
                C.text.split()[0] 
                for C in driver.find_elements(
                    By.XPATH,"//p[contains(@class,'totalSeats___')]"
                    )
                ]
            )
            
            # Go back to the previous page
            driver.back()

            time.sleep(3)

        except Exception as E:

            print(f"An error occurred: {E}")

            driver.back()

            time.sleep(2)

        return


    def scrap(x):

        """
        Scrapes all bus routes for a given state and extracts
        details for each bus.
        """

        # Get all route links on the current state page
        RDETAILS=driver.find_elements(By.CSS_SELECTOR,"a[class='route']")

        for i in range(len(RDETAILS)):

            # Re-fetch route elements to avoid stale element reference
            RDETAILS=driver.find_elements(By.CSS_SELECTOR,"a[class='route']")

            ROUTE_LINK = RDETAILS[i].get_attribute('href')
            
            ROUTE_TITLE = RDETAILS[i].get_attribute('title')

            # Open the route page
            driver.get(ROUTE_LINK)

            # Wait until bus listings are loaded
            wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH, "//li[contains(@class, 'tupleWrapper')]")
                )
            )

            # Get government bus listings
            GOVT_BUSES = driver.find_elements(
                By.XPATH,"//div[contains(@class,'rtcInfoWrap___')]"
            )

            for j in range(len(GOVT_BUSES)):

                # Re-fetch to prevent stale element reference
                GOVT_BUSES = driver.find_elements(
                    By.XPATH,"//div[contains(@class,'rtcInfoWrap___')]"
                )

                GOVT_BUSES[j].click()

                # Wait until the bus details are loaded
                wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH, "//li[contains(@class, 'tupleWrapper')]")
                    )
                )

                # Extract bus details for the clicked government bus
                extraction(x, ROUTE_LINK, ROUTE_TITLE)

                break #remove

            # Extract details for remaining buses on the route page
            extraction(x, ROUTE_LINK, ROUTE_TITLE)

            break #remove

        return

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()

    # Set up an explicit wait for elements to load (max 10 seconds)
    wait = WebDriverWait(driver, 10)

    # Dictionary containing state names and their 
    # corresponding RedBus government bus URLs
    GOVT_LINKS = {
        'Andhra Pradesh': 'https://www.redbus.in/online-booking/apsrtc',
        'Kerala': 'https://www.redbus.in/online-booking/ksrtc-kerala',
        'Telangana': 'https://www.redbus.in/online-booking/tsrtc',
        'Goa': 'https://www.redbus.in/online-booking/ktcl',
        'Rajasthan': 'https://www.redbus.in/online-booking/rsrtc',
        'South Bengal': (
            'https://www.redbus.in/online-booking/'
            'south-bengal-state-transport-corporation-sbstc'
        ),
        'Himachal Pradesh': 'https://www.redbus.in/online-booking/hrtc',
        'Assam': 'https://www.redbus.in/online-booking/astc',
        'Uttar Pradesh': (
            'https://www.redbus.in/online-booking/'
            'uttar-pradesh-state-road-transport-corporation-upsrtc'
        ),
        'West Bengal': 'https://www.redbus.in/online-booking/wbtc-ctc'
    }

    # Dictionary to store extracted bus data
    DATA = {
                'state':[],
                'route_name':[],
                'route_link':[],
                'busname':[],
                'bustype':[],
                'departing_time':[],
                'duration':[],
                'reaching_time':[],
                'star_rating':[],
                'price':[],
                'seats_available':[]
            }

    # Loop through each state and its corresponding RedBus URL
    for STATE,URL in GOVT_LINKS.items():

        # Navigate to the state's RedBus page
        driver.get(URL)

        # Wait until all route links are present on the page
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".route_link")
            )
        )

        try:

            # Check if pagination tabs exist on the page
            driver.find_element(
                By.XPATH, "//div[contains(@class, 'DC_117_pageTabs')]"
            )

            # Get all pagination elements
            PANUM = driver.find_elements(
                By.XPATH, "//div[contains(@class, 'DC_117_pageTabs')]"
            )

            # Iterate through each pagination tab
            for i in range(len(PANUM)):

                # Re-fetch pagination elements to avoid stale element reference
                PANUM = driver.find_elements(
                    By.XPATH, "//div[contains(@class, 'DC_117_pageTabs')]"
                )

                # Click on the pagination tab using JavaScript 
                # to avoid element intercept errors
                driver.execute_script("arguments[0].click();", PANUM[i])

                # Call scrap function to extract bus details 
                # for the current state
                scrap(STATE)
                break #remove

        except:
            
            # If no pagination exists, directly scrap the page
            scrap(STATE)

        # Go back to the main state page after scraping
        driver.back()

        break #remove

    # Close the Selenium WebDriver after scraping all data
    driver.quit()

    # Convert the collected bus data into a pandas DataFrame
    df = pd.DataFrame(DATA)

    return df

# Configure the Streamlit app page layout and title
st.set_page_config(page_title="BusGrid", layout="wide")

# Apply custom CSS styling for the app
st.markdown("""
<style>
html, body, [data-testid="stApp"] {
    background-color: #eef5ff !important;
}
.block-container {
    padding-top: 1rem;
}
.stButton > button {
    background: linear-gradient(135deg, #e3f2fd, #bbdefb);
    border: none;
    padding: 14px 20px;
    border-radius: 10px;
    color: #1a237e;
    font-weight: 600;
    font-size: 16px;
    width: 100%;
    margin: 8px 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease-in-out;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #bbdefb, #90caf9);
    transform: scale(1.03);
    color: #0d47a1;
    cursor: pointer;
}
th {
    font-weight: bold !important;
    font-size: 18px !important;
    color: #1a237e !important;
}
</style>
""", unsafe_allow_html=True)


# Get query parameters from the URL 
# (used for state and route selection)
PARAMS = st.query_params


# Extract selected state and route from query parameters
SELECTED_STATE = PARAMS.get("state", None)

SELECTED_ROUTE = PARAMS.get("route", None)


# If neither state nor route is selected, display the welcome page
if not SELECTED_STATE and not SELECTED_ROUTE:

    st.markdown("""
    <div style="
        background-color:#ffffff;
        padding:30px 20px;
        border-radius:12px;
        box-shadow:0 4px 10px rgba(0,0,0,0.1);
        border: 2px solid #e0e0e0;
    ">
        <h1 style='text-align:center;'>
            🚍 Welcome to <span style='color:#ff4b4b;'>BusGrid</span>
        </h1>
        <p style="
            text-align:center;
            color:gray;
            font-size:18px;
            margin-top:-10px;
        ">
        Your smart companion for discovering bus routes, schedules, 
        and seat availability.
        </p>
    </div>
    """, unsafe_allow_html=True)

try:

    # Connect to the local MySQL database 'bus_DETAILS'  
    mydb = mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        user="PRcdCBsrEmMi29p.root",
        password="oIyHQktds3I0RxUf",
        database=""
    )

    # Get scraped bus data (cached to avoid re-scraping)
    df = scrap_redbus_data()

    # Create a buffered cursor to execute SQL queries
    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("DROP DATABASE IF EXISTS Redbusdata")
    
    # Create a new MySQL database named Redbusdata
    mycursor.execute("CREATE DATABASE Redbusdata")


    # Connect to the new database using SQLAlchemy
    engine = create_engine(
        (
            "mysql+mysqlconnector://PRcdCBsrEmMi29p.root:"
            "oIyHQktds3I0RxUf@"
            "gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/"
            "Redbusdata"
        ),
        connect_args={"ssl_disabled": False}
    )

    # Export the pandas DataFrame to the 'bus_routes' table 
    # in chunks of 1000 rows
    
    df.to_sql(
        name='bus_routes',
        con=engine,
        if_exists='replace',
        index=True,
        chunksize=1000,
        index_label='id'
    )

    # Modify the table structure to add appropriate 
    # data types and primary key
    mycursor.execute(
        """
        USE Redbusdata;
        """
    )

    mycursor.execute(
        """
        ALTER TABLE bus_routes ADD 
        PRIMARY KEY (id)
        """
    )

    mycursor.execute(
        """
        alter table bus_routes modify column departing_time time;
        """
    )

    mycursor.execute(
        """
        alter table bus_routes modify column reaching_time time;
        """
    )

    mycursor.execute(
        """
        alter table bus_routes modify column star_rating float;
        """
    )

    mycursor.execute(
        """
        alter table bus_routes modify column price decimal(10,2);
        """
    )

    mycursor.execute(
        """
        alter table bus_routes modify column seats_available int;
        """
    )

    # Case 1: User has selected both state and route
    if SELECTED_STATE and SELECTED_ROUTE:

         # Add a "Go back" button to remove route selection
        if st.button("🔙 Go back"):

            del st.query_params["route"]

            st.rerun() # Refresh the app with updated query params

        # Fetch the minimum and maximum price for selected 
        # state & route
        mycursor.execute("""
            SELECT MIN(price), MAX(price) FROM bus_routes
            WHERE state = %s AND route_name = %s
        """, (SELECTED_STATE, SELECTED_ROUTE))

        PRICE_DETAILS = mycursor.fetchone()

        MIP, MAPR = list(PRICE_DETAILS) # Minimum and maximum prices

        # Define filtering options for the bus search
        FILTERING_OPTIONS = [
            "❄️ AC","🪟 NON-AC","🛌 SLEEPER","💺 SEATER","🌟 LUXURY",
            "⚡ ELECTRIC","🏛️ GOVERNMENT","🏢 PRIVATE","⭐ HIGHLY RATED",
            "🌞 DAY TRAVEL","🌙 NIGHT TRAVEL"
        ]

        # Split the page into filter column and data display column
        COL1, COL2 = st.columns([1, 4])

        # Filter options UI
        with COL1:

            st.markdown("""
                <h3 style="
                    color:#E86D51;
                ">
                    Filter Options
                </h3>
            """, unsafe_allow_html=True)

            FILV = st.pills(
                "",
                options=FILTERING_OPTIONS,
                key="filter_pills",
                selection_mode="multi",
                default = []
            )

            # Price slider for filtering
            SLV = st.slider(
                "Price Range (₹)",
                min_value=int(MIP),
                max_value=int(MAPR),
                value=int(MAPR),
                step=10,
                key="price_slider"
            )

        # Base SQL query to fetch bus details for 
        # selected state & route within price range
        QUERY1 = """
            SELECT busname, bustype, departing_time, duration,
                reaching_time, star_rating, price, seats_available
            FROM bus_routes 
            WHERE state = %s 
                AND route_name = %s 
                AND price <= %s
        """

        # Additional SQL filters based on selected options
        if '❄️ AC' in FILV:# Filter for AC buses

            SQUERY1 = """ and ( lower(bustype) like '%ac%' or 
                                lower(bustype) like '%a/c%' or 
                                lower(bustype) like '%a.c%') and
                                lower(bustype) not like '%non%'
                        """
        
        else:

            SQUERY1 = ""

        if '🪟 NON-AC' in FILV:# Filter for Non-AC buses

            SQUERY2 = " and lower(bustype) like '%non%'"

        else:
            
            SQUERY2 = ""

        if '❄️ AC' in FILV and '🪟 NON-AC' in FILV:

            SQUERY1,SQUERY2 = "",""

        if '🛌 SLEEPER' in FILV:# Filter for Sleeper buses

            SQUERY3 = " and upper(bustype) like '%SLEEP%'"

        else:

            SQUERY3 = ""

        if '💺 SEATER' in FILV:# Filter for Seater buses

            SQUERY4 = " and upper(bustype) like '%SEAT%'"

        else:

            SQUERY4 = ""

        if '🌟 LUXURY' in FILV:# Filter for Luxury buses

            SQUERY5 = " and upper(bustype) like '%LUXURY%'"

        else:

            SQUERY5 = ""

        if '⚡ ELECTRIC' in FILV:# Filter for Electric buses

            SQUERY6 = " and upper(bustype) like '%ELECTRIC%'"

        else:

            SQUERY6 = ""

        if '🏛️ GOVERNMENT' in FILV:# Filter for Government buses

            SQUERY7 = """ and (upper(busname) like '%APSRTC%' or
                            upper(busname) like '%KSRTC%' or
                            upper(busname) like '%TGSRTC%' or
                            upper(busname) like '%KTCL%' or
                            upper(busname) like '%RSRTC%' or
                            upper(busname) like '%SBSTC%' or
                            upper(busname) like '%HRTC%' or
                            upper(busname) like '%ASTC%' or
                            upper(busname) like '%UPSRTC%' or
                            upper(busname) like '%WBTC%')
                        """
            
        else:

            SQUERY7 = ""

        if '🏢 PRIVATE' in FILV:# Filter for Private buses

            SQUERY8 = """ and (upper(busname) not like '%APSRTC%' and
                                upper(busname) not like '%KSRTC%' and
                                upper(busname) not like '%TGSRTC%' and
                                upper(busname) not like '%KTCL%' and
                                upper(busname) not like '%RSRTC%' and
                                upper(busname) not like '%SBSTC%' and
                                upper(busname) not like '%HRTC%' and
                                upper(busname) not like '%ASTC%' and
                                upper(busname) not like '%UPSRTC%' and
                                upper(busname) not like '%WBTC%')
                        """
            
        else:

            SQUERY8 = ""

        if '🏛️ GOVERNMENT' in FILV and '🏢 PRIVATE' in FILV:

            SQUERY7, SQUERY8 = "", ""

        if '⭐ HIGHLY RATED' in FILV:# Filter for Highly rated buses

            SQUERY9 = " and star_rating >= 4.0"

        else:

            SQUERY9 = ""

        if '🌞 DAY TRAVEL' in FILV:# Filter for Day travel buses

            SQUERY10 = "and departing_time between '06:00:01' and '18:00:00'"

        else:

            SQUERY10 = ""

        if '🌙 NIGHT TRAVEL' in FILV:# Filter for Night travel buses

            SQUERY11 = "and departing_time between '18:00:01' and '06:00:00'"

        else:

            SQUERY11 = ""

        # Combine all query parts to form the final SQL query
        final_query = QUERY1 + SQUERY1 + SQUERY2 + SQUERY3 + SQUERY4

        final_query+= SQUERY5 + SQUERY6 + SQUERY7 + SQUERY8 + SQUERY9

        final_query+=SQUERY10 + SQUERY11 

        # Execute query and fetch results
        mycursor.execute(final_query, (SELECTED_STATE, SELECTED_ROUTE, SLV))

        RAW_DATA = mycursor.fetchall()

        # Convert query results into a DataFrame
        DETAILS = pd.DataFrame(RAW_DATA, columns=[
            "BUS NAME", "BUS TYPE", "DEPARTING TIME", "DURATION",
            "REACHING TIME", "STAR RATING", "PRICE (₹)", "SEATS AVAILABLE"])

        # Helper function to convert time to AM/PM format
        def format_timedelta_to_ampm(td):

            TOTAL_SECONDS = int(td.total_seconds())

            HOURS = TOTAL_SECONDS // 3600

            MINUTES = (TOTAL_SECONDS % 3600) // 60

            PERIOD = "AM" if HOURS < 12 else "PM"

            HOURS = HOURS % 12 or 12

            return f"{HOURS}:{MINUTES:02d} {PERIOD}"
        
        # Apply formatting to relevant columns
        DETAILS["DEPARTING TIME"] = DETAILS["DEPARTING TIME"].apply(
            format_timedelta_to_ampm
        )

        DETAILS["REACHING TIME"] = DETAILS["REACHING TIME"].apply(
            format_timedelta_to_ampm
        )

        DETAILS["STAR RATING"] = DETAILS["STAR RATING"].apply(
            lambda x: f"{x:.1f}"
        )

        DETAILS["PRICE (₹)"] = DETAILS["PRICE (₹)"].apply(
            lambda x: f"{x:.2f}"
        )

        DETAILS["SEATS AVAILABLE"] = DETAILS["SEATS AVAILABLE"].apply(
            lambda x: f"{x:.0f}"
        )

        # Display bus details in Streamlit
        with COL2:

            if DETAILS.empty:

                st.warning(" 😔 No buses found. Try changing the filters.")

            else:

                st.success(

                    f"🚌 {len(DETAILS)} buses found within the " 

                    "selected price range."

                )

                st.dataframe(
                    DETAILS,
                    use_container_width=True,
                    hide_index=True
                )

    # Case 2: User has selected only state
    elif SELECTED_STATE:

        if st.button("🔙 Go back"):

            st.query_params.clear()
            
            st.rerun()

        st.markdown(
            f"""
                <h3 style='color:#444;margin-top:10px;'>🗺️ Bus routes for
                    <span style='color:#ff4b4b;'>{SELECTED_STATE}
                    </span>
                </h3>
            """, unsafe_allow_html=True
        )

        # Fetch all available routes for the selected state
        mycursor.execute(
            """
            SELECT DISTINCT route_name FROM bus_routes
            WHERE state = %s
            """, (SELECTED_STATE,)
        )

        ROUTES = mycursor.fetchall()

        # Display each route as a button
        for i, (route,) in enumerate(ROUTES):

            if i % 3 == 0:

                COLS = st.columns(3)
                
            with COLS[i % 3]:

                if st.button(route):

                    st.query_params["state"] = SELECTED_STATE

                    st.query_params["route"] = route

                    st.rerun()

    # Case 3: User has not selected anything
    else:

        st.markdown(
            """
            <div style='
                text-align:center;
                margin:30px 0 10px 0;
            '>
                <h3 style='
                    color:#444;
                '>
                🚏 Please choose a state to view available bus routes
                </h3>
            </div>
        """, unsafe_allow_html=True)

        # Display all states as buttons
        mycursor.execute("""
            SELECT DISTINCT state FROM bus_routes
            ORDER BY state
        """)

        STATES = mycursor.fetchall()

        for i, (STATE,) in enumerate(STATES):

            if i % 4 == 0:

                COLS = st.columns(4)

            with COLS[i % 4]:

                if st.button(STATE):

                    st.query_params["state"] = STATE

                    st.rerun()

    # Close database connection
    mycursor.close()

    mydb.close()

# Handle database connection errors
except mysql.connector.Error as err:

    st.error(f"Database error: {err}")
