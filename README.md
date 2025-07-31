# F1 Database - Step-by-Step Guide & README for GitHub

This guide and README will help you set up, run, and manage the F1 Database project locally and prepare it for GitHub.

## Project Overview

The F1 Database is a FastAPI web application that enables authenticated users to manage a database of Formula 1 drivers and teams, powered by Google Firestore for storage and using Firebase for authentication.

## 1. Prerequisites

- Python 3.8 or higher.
- Google Cloud Project with Firestore enabled.
- Firebase project with Authentication configured.
- The following Python packages:
  - fastapi
  - uvicorn
  - google-cloud-firestore
  - google-auth
  - firebase-admin
  - jinja2

## 2. Project Structure

```
f1-database/
├── main.py
├── requirements.txt
├── static/
│   └── (static files)
├── templates/
│   ├── main.html
│   ├── drivers.html
│   ├── teams.html
│   ├── driver_details.html
│   ├── team_details.html
│   ├── edit_drivers.html
│   ├── edit_teams.html
│   ├── compare.html
│   ├── compare-results.html
│   └── compare_teams.html
```

## 3. Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/f1-database.git
cd f1-database
```

### Step 2: Set Up Google Cloud Service Account

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a project.
3. Enable Firestore.
4. Go to IAM & Admin > Service Accounts.
5. Create a service account and generate a JSON key file.
6. Save your credentials JSON (e.g., `serviceAccount.json`) in your project root.

### Step 3: Set Up Firebase

1. [Go to Firebase Console](https://console.firebase.google.com/).
2. Create a new project or use existing.
3. Enable Authentication (e.g., with Email/Password, Google, etc.).
4. Save your Firebase config snippet for later use on the frontend.

### Step 4: Install Python Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Sample `requirements.txt`:**
```
fastapi
uvicorn
google-cloud-firestore
google-auth
firebase-admin
jinja2
```

### Step 5: Setup Environment Variables

Set the following environment variable to point to your service account key:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="serviceAccount.json"
```

## 4. Running the Application

Start the FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

The app will be accessible at `http://127.0.0.1:8000/`

## 5. Usage

- Visit `/` to view all drivers and teams (read-only until signed in).
- Log in (using Firebase Auth on frontend).
- Once authenticated, you can:
  - Add, edit, or delete drivers and teams.
  - Query/filter drivers and teams by stats.
  - Compare two drivers or two teams.

## 6. Project Features

- Firebase Authentication integration.
- Google Firestore backend.
- Add/edit/delete drivers and teams.
- Query drivers or teams by attributes and comparison operators.
- Cross-template rendering via Jinja2.
- Static and template file structure for easy UI edits.

## 7. Deployment

Official deployments (GCP, Azure, or Heroku) require you to configure appropriate environment variables and secrets, as well as potentially update `main.py` for production settings.

## 8. Contributing

- Fork the repository.
- Create a new branch.
- Make your changes.
- Submit a Pull Request describing your modifications.

## 9. Notes and Troubleshooting

- Ensure your Google service account has Firestore access.
- Set up CORS if you use a separate domain for the frontend.
- Debug authentication by logging errors from `validateFirebaseToken()`.

## 10. License

MIT License (add your license file as needed).
    ```
## Installation

1. Clone the repo:

   ```
   git clone https://github.com/yourusername/f1-database.git
   cd f1-database
   ```

2. Install dependencies:

   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set Google credentials for Firestore:

   ```
   export GOOGLE_APPLICATION_CREDENTIALS="serviceAccount.json"
   ```

## Running

```
uvicorn main:app --reload
```

Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to start using the app.

## Deployment

- Provide environment variables and server setup according to your platform (GCP, Azure, Heroku, etc).
- Use production server (e.g., Gunicorn) for scalable deployment.

## Screenshot

![WhatsApp Image 2025-08-01 at 00 20 43_e129423c](https://github.com/user-attachments/assets/4b66dbcf-59ed-4075-a5d2-b00b908919a8)
 
![WhatsApp Image 2025-08-01 at 00 22 29_119c2d8e](https://github.com/user-attachments/assets/8da40489-44d2-434f-b6db-9272c9b8ec15)

## Contributing

Open an issue or submit a PR!

