# Frontend setup steps

## Dependencies setup
Run the following commands in order in beat-metrics-app:
```bash
npm i
npm run build
rm -r gae/build
mv build/ gae/
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
  cd beat-metrics-app/gae
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