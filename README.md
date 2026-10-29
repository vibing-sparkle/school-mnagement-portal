# School Management Portal

A beginner-friendly Python web app built with Streamlit.

## Features
- Dashboard with student totals and class chart
- Add student records
- Search student records by name or ID
- Download records as CSV
- Delete a student record

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

## Deploy to Streamlit Community Cloud
1. Push these files to a GitHub repository.
2. Open https://share.streamlit.io/ and sign in with GitHub.
3. Choose **Create app**, select your repository and branch, and set the main file path to `app.py`.
4. Click **Deploy**.

## Demo and privacy
This is an educational demo. Do not enter real student personal information into a public deployment.
The app uses a local CSV file for simple demonstration storage. For production use, configure a persistent database and authentication.
