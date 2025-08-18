# 🚌 **BusGrid: RedBus Data Scraper & Interactive Bus Explorer**

A **Python project** that scrapes bus route data from **RedBus** for multiple state transport corporations in India using **Selenium**, stores it in a **MySQL database**, and displays it in an **interactive Streamlit web app** with dynamic filtering options.  

---

## ✨ **Features**
- 📝 **Bus Details Scraping:**  
  - **Bus name, type, departing & arriving times**  
  - **Duration, price, available seats**  
  - **Star ratings** (if available)  
- 🌏 **Supports multiple state transport corporations** in India.  
- 🔄 **Handles dynamic content** including lazy loading and pagination.  
- 🖥️ **Interactive Streamlit Dashboard** with:  
  - **State & route selection**  
  - **Multi-option filters:** ❄️ AC, 🪟 Non-AC, 🛌 Sleeper, 💺 Seater, 🌟 Luxury, ⚡ Electric, 🏛️ Government, 🏢 Private, ⭐ Highly Rated, 🌞 Day Travel, 🌙 Night Travel  
  - **Price range slider**  
  - **Real-time display** of filtered buses  
- 🗄️ **MySQL Database Integration** for storing and querying bus data efficiently.  

---

## 🛠️ **Technologies Used**
- **Python**  
- **Selenium** – Web scraping with dynamic scrolling & element handling  
- **Streamlit** – Interactive web UI for filtering & visualization  
- **MySQL** – Database for storing extracted bus data  
- **Pandas** – Data manipulation & storage  
