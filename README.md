## Prerequisites

1. **Google Cloud Platform Account**: Ensure you have a Google Cloud Platform (GCP) account.
2. **Python**: Ensure Python is installed on your system.
3. **Gmail API and OAuth Libraries**: Install the required Python libraries.
    ```sh
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    ```

## Steps for Integration

### 1. Enable Gmail API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (happyfox-assignment)
3. Navigate to **API & Services > Library**.
4. Search for "Gmail API" and enable it.

### 2. Set Up OAuth 2.0 Credentials

1. Navigate to **API & Services > Credentials**.
2. Click **Create Credentials** and select **OAuth 2.0 Client IDs**.
3. Download the `credentials.json` file and save it in your project directory.

### 3. Running the Script

1. Update the MYSQL details in resources/config.ini file
2. Run the DBMigration file to create the tables required for this application.
    ```sh
    python DBMigration.py
    ```

3. Ensure the `credentials.json` file is in your project directory.
4. Run the AccumulateEmails script to fetch latest emails from the access gmail account:
    ```sh
    python AccumulateEmails.py
    ```
5. Follow the on-screen instructions to authenticate via your browser. After successful authentication, a `token.json` file will be created to store your access and refresh tokens.
6. Update the filter and action rules in resources/rules.json file
7. Run the EmailProcessor file to filter the emails and apply the given action like read/unread/move messages to different labels.
    ```sh
    python EmailProcessor.py
    ```