# 🎯 Faceit Match Analyzer

This project is a **Chrome Extension** and a **Flask backend** that analyzes a **Faceit CS2 match** and predicts which maps are most likely to be banned based on the players' recent statistics.

---

## 🚀 Features
✅ Automatically retrieves **Match ID** from the Faceit website  
✅ Analyzes **maps per team** and predicts ban probability  
✅ Fetches data from **the last 100 matches**  
✅ Displays statistics in a modern and clear **HTML report**  

---

## 📥 Installation

### **1️⃣ Clone the project**
```sh
git clone https://github.com/your-github-username/faceit-match-analyzer.git
cd faceit-match-analyzer
```

### **2️⃣ Install Python dependencies**
Create and activate a virtual environment:
```sh
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```
Install Flask and other dependencies:
```sh
pip install -r requirements.txt
```

---

## 🖥️ **Start the Flask server**

1️⃣ Create a `.env` file and add your **Faceit API Key**:
```ini
FACEIT_API_KEY=your-api-key-here
```

2️⃣ Run the server:
```sh
python server.py
```

✅ The Flask server will start at `http://127.0.0.1:5000`

---

## 🌐 **Install the Chrome Extension**
1️⃣ Open **Chrome** and go to `chrome://extensions/`  
2️⃣ Enable **Developer Mode**  
3️⃣ Click **"Load unpacked"** and select the `chrome_extension/` folder  
4️⃣ Start the analysis by clicking on the extension icon on a **Faceit match page**  

---

## 🛠 **Technologies Used**
🔹 **Python (Flask)** – Backend  
🔹 **JavaScript (Chrome Extension)** – Frontend  
🔹 **HTML + CSS** – Report visualization  
🔹 **Faceit API** – Data retrieval  

---

## 🏆 **Contributions**
🔹 Have suggestions? Create an **Issue**!  
🔹 Want to contribute? Open a **Pull Request**!  

👨‍💻 Built by **Hampus Hillborg**

