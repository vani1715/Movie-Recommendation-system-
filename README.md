# 🎬 Movie Recommendation System

> A smart movie discovery web app powered by Python, Streamlit, and the OMDb API

## 📖 Overview

The **Movie Recommendation System** is a web application that lets users search for movies and receive intelligent recommendations based on genres, ratings, and movie attributes. It integrates with the **OMDb API** to fetch real-time movie details — including posters, ratings, cast, and plot summaries — for an engaging movie discovery experience.

---

## ✨ Features

- 🔍 Search movies by title
- 🌐 Real-time movie data via OMDb API
- 🖼️ Movie posters, ratings, and plot summaries
- 🎭 Genre-based smart recommendations
- 👨‍🎤 Cast, director, and runtime details
- ⚡ Fast, responsive Streamlit UI

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core Programming Language |
| Streamlit | Web Application Framework |
| Pandas | Data Processing |
| NumPy | Numerical Operations |
| Requests | HTTP / API Communication |
| OMDb API | Movie Data Source |

---

## 📂 Project Structure

```
Movie-Recommendation-System/
│
├── app.py                  # Main Streamlit application
├── recommendation.py       # Recommendation logic
├── requirements.txt        # Project dependencies
├── .env                    # API key configuration (not committed)
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- An [OMDb API key](http://www.omdbapi.com/apikey.aspx) (free tier available)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure your API key**

Create a `.env` file in the root directory:
```
OMDB_API_KEY=your_api_key_here
```

**4. Run the app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## ⚙️ How It Works

```
User Searches a Movie
        ↓
  OMDb API Request
        ↓
 Fetch Movie Details
        ↓
Analyze Movie Attributes
        ↓
Generate Recommendations
        ↓
  Display Results
```

1. **Search** — User enters a movie title in the search bar
2. **Fetch** — App queries the OMDb API for real-time movie details
3. **Analyze** — Movie attributes (genre, rating, etc.) are processed
4. **Recommend** — Similar movies are surfaced based on shared attributes
5. **Display** — Results shown with posters, ratings, and descriptions

---

## 🎯 Example

**Input:** `Inception`

**Recommended Movies:**
- Interstellar
- The Prestige
- Shutter Island
- Tenet
- The Matrix

---

## 🔮 Roadmap

- [ ] User authentication & profiles
- [ ] Personalised recommendations
- [ ] Watchlist / save feature
- [ ] Movie reviews & sentiment analysis
- [ ] Multi-database integration (TMDB, Letterboxd)
- [ ] AI-powered recommendation engine

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📜 License

This project is intended for educational and portfolio purposes.

---

## 👩‍💻 Author

**Vani Sharma**
🎓 BCA (Data Science & AI) · Aspiring Data Scientist · AI & ML Enthusiast

⭐ If you found this project helpful, please give it a star!
