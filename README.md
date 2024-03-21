## How to run the project:
1. Clone the repository or download the zip file.
2. Create a virtual environment using the following command:
    
    Windows:
    ```
    python -m venv venv
    ```
    for linux or mac:
    ```
    python3 -m venv venv
    ```
3. Activate the virtual environment using the following command:

    Windows:
    ```
    venv\Scripts\activate
    ```
    Linux or mac:
    ```
    source venv/bin/activate
    ```

4. Install the required packages using the following command:

    ```
    pip install -r requirements.txt
    ```
5. Create a `.env` file in the root directory of the project and add the following lines:

    ```
    SECRET_KEY=your_secret_key
    DEBUG=True
    ```
    Replace `your_secret_key` with a secret key.
    you cna follow the example file `.env-example` to create the `.env` file.

6. Run the following command to create the database:

    ```
    python manage.py migrate
    ```

7. Run the following command to create a superuser:

    ```
    python manage.py createsuperuser
    ```

8. Run the following command to start the server:

    ```
    python manage.py runserver
    ```
9. Open the browser and go to the following link:

    ```
    http://localhost:8000/
    ```
10. To stop the server, press `Ctrl + C` in the terminal.

## How to use the project:
1. Open the browser and go to the following link:

    ```
    http://localhost:8000/
    ```
2. Click on the `Dashboard` button.
3. Enter the username and password and click on the `Login` button. for example:
    ```
    username: admin
    password: admin
    ```
4. After logging in, you will be redirected to the dashboard.
