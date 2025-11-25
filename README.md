# Saigeware Internship Assignment

This repository contains my solutions for the Saigeware internship assignment.

I have completed **two tasks**:

- **Task 1 – Flask + Firestore (Customer Management App)**
- **Task 3 – Anomaly Detection in Wellness Data**

---

## Task 1: Flask + Firestore – Customer Management

Location: `task1_flask_firestore/`

### What it does

- Connects a Flask application to Google Firestore.
- Uses a `customers` collection with fields: `name`, `email`, `phone`.
- Supports full CRUD:
  - Add customer
  - List all customers
  - Edit customer
  - Delete customer
- Search/filter customers by **name or email**.
- Simple web UI using HTML (Jinja templates) and CSS.

### How to run (locally)

1. Create a Google Cloud project and enable **Firestore** (Native mode).
2. Create a service account and download the JSON key.
3. Save the key as:

   `task1_flask_firestore/serviceAccountKey.json`

4. Install dependencies:

   ```bash
   cd task1_flask_firestore
   pip install -r requirements.txt
