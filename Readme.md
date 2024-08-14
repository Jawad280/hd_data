# HDMall Database Integration #

This repo has the tools & scripts to clean, format and upload raw .xlsx data into our Azure Database.

### Connecting & Viewing Database ###

- We can locally view the database using pgAdmin4
- Since we are using Azure, we need to login via Azure CLI for AzureCredentials to generate the token, thus login with `az login` in terminal
- **Register a new server** : In the pgAdmin 4 interface, right-click on "Servers" in the left-side browser tree, and select "Register” -> “Server"
- **Configure server details** : In the "Register - Server" window, you will see multiple tabs - "General", "Connection", "SSL", and others
    - **General Tab** : 
        - Name - provide a name
    - **Connection Tab** : 
        - Hostname/address : ***.postgres.database.azure.com
        - Port : (Default) 5432
        - Username : < username > 
        - Password : Use `get_token.py` to fetch key

### Clean & Format Data ###
- In the clean_data.ipynb, replace the pd.read_excel(< .xlsx raw data >)
- Once the notebook is ran, the `packages.csv` will be generated in the directory

### Uploading Data into the database ### 
- To upload, simply run the `seed_hd_data.py`
- You will be prompted to enter a table name
    - `packages_all` -> Main table used by the bot
    - `packages_all_staging` -> Secondary table for holding current data when we update new data
    - `test` -> Table for testing
- The upload of data can take quite a long time, roughly 2h for 20300~ rows

### Granting Access to New Microsoft Entra User ###
```
\c postgres

GRANT CONNECT ON DATABASE postgres TO "microsoft_entra_admin_name";

GRANT USAGE ON SCHEMA public TO "microsoft_entra_admin_name";

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "microsoft_entra_admin_name";

GRANT USAGE ON SCHEMA public TO "microsoft_entra_admin_name";
```