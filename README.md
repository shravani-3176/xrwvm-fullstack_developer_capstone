# Cars Dealership Full-Stack Web Application

A cloud-native, full-stack car dealership web application built as the Capstone Project for the **IBM Full Stack Software Developer Professional Certificate**.

## Project Architecture & Overview

The dealership portal connects car buyers and enthusiasts with a national network of automotive dealerships across the United States. Users can browse dealerships, search and filter by state, review vehicle details, read customer reviews with integrated AI sentiment analysis, register accounts, and post their own verified dealership reviews.

### Architecture Components

1. **Frontend**:
   - Modern dynamic Single-Page Application (SPA) built with **React** and **Bootstrap 5**.
   - Static informational landing pages for About Us and Contact Us.
   - Dynamic dealership directory, state-level filtering, dealer profile views, and review submission forms.

2. **Backend Services & User Management**:
   - Built with **Python** and **Django**.
   - User authentication, registration, session management, and admin dashboard.
   - Car Make and Car Model relational models with Django ORM and SQLite.
   - Proxy API layer communicating with distributed microservices.

3. **Dealership & Reviews Microservice**:
   - Powered by **Node.js**, **Express**, and **MongoDB**.
   - Manages dealership records across 50 US states and customer reviews database.

4. **Sentiment Analysis AI Microservice**:
   - Python & Flask microservice utilizing **NLTK (Natural Language Toolkit)** and VADER sentiment intensity analyzer.
   - Evaluates sentiment (positive, neutral, negative) for incoming customer reviews in real-time.

5. **DevOps, CI/CD, and Containerization**:
   - Automated testing and Python code linting via **GitHub Actions**.
   - Containerized services configured for **Docker** and scalable **Kubernetes** cloud deployment.

---

## API Endpoints

- `GET /djangoapp/get_dealers` — Retrieve all national dealerships.
- `GET /djangoapp/get_dealers/<state>` — Retrieve dealerships filtered by state (e.g. Kansas).
- `GET /djangoapp/dealer/<id>` — Retrieve detailed information for a specific dealership.
- `GET /djangoapp/reviews/dealer/<id>` — Retrieve reviews with AI sentiment analysis for a dealership.
- `POST /djangoapp/add_review` — Submit a new customer review for a dealership.
- `GET /djangoapp/get_cars` — Retrieve all car makes and models.
- `POST /djangoapp/login` — Authenticate an existing user.
- `GET /djangoapp/logout` — Terminate user session.
- `POST /djangoapp/register` — Register a new customer user account.

---

## Author

- **Developer**: Shravani Gat
- **GitHub**: [@shravani-3176](https://github.com/shravani-3176)
- **Repository**: [xrwvm-fullstack_developer_capstone](https://github.com/shravani-3176/xrwvm-fullstack_developer_capstone)