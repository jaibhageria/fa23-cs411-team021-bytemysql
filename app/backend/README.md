# Backend setup steps

## Dependencies setup
Run the following commands in order in app/backend:
```python
python3 -m venv env
source env/bin/activate
cd code
pip install -r requirements.txt
```

## Run locally
- For running the app on local system, make sure your IP is whitelisted on the SQL instance with IP `35.225.155.122`
- You can achieve that by navigating to the SQL instance on the GCP project `cs411-bytemysql` with SQL instance name `spotifydata`
- Now just run the below command in app/backend/code:
  ```python
  python3 main.py
  ```

## Run app on Google App Engine (GAE)
- Install the `gcloud` CLI tool compatible for your system
- Run the below command to set the project ID:
  ```bash
  gcloud config set project cs411-bytemysql
  ```
  You may be prompted to sign-in before the above command can run
- To deploy:
  ```bash
  cd app/backend/code
  gcloud app deploy
  ```

That's it!
You can use `gcloud app browse` to hit the URL of the service deployed. This will re-direct to your default browser.
Further, you may find the following list of commands useful:
```bash
# List the services deployed on GAE
gcloud app services list
# List the versions of the services deployed on GAE and their current status
gcloud app versions list
# Stop all services
gcloud app services stop
# Stop a particular service version
gcloud app versions stop <version id from versions list> # example: gcloud app versions stop 20231127t033136
```
For more operations navigate to the app engine dashboard on your GCP project