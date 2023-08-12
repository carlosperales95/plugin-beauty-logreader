# plugin-beauty-logreader

Current Compatibilities:
- Adyen Adobe Commerce plugin logs
- Shopware6 plugin logs (NOT YET, PLANNED SOON)
- SFCC cartrdige logs (NOT YET, PLANNED SOON)

1. Clone the repo
2. `cd` into the project folder (`/plugin-beauty-logreader`) and create a virtual environment for this python app (replace `{name_of_your_env}`)
```
python -m venv {name_of_your_env (e.g. testenv)}
```
3. Create `/cases` folder
The app needs a cases folder to save all of your imports. This way you can access them later!
```
mkdir cases
```
4. Activate the virtual environment
```
source {name_of_your_env}/bin/activate
```

5. Install all of the `pip` dependencies (all are exported into `requirements.txt`)
```
python -m pip install -r requirements.txt
```

6. Run the app
```
flask run
```
Ready! Now plugin files are prettier to look at (Should start in your [localhost](http://127.0.0.1:5000/))
![image](https://github.com/carlosperales95/plugin-beauty-logreader/assets/8956411/48c854c3-63f1-4152-babd-a27858adcbf1)

7. To import logs into the app
You can select one (or many) files using the File Import functionality. App will add all of the log entries together and display them as a table (same as above)
![image](https://github.com/carlosperales95/plugin-beauty-logreader/assets/8956411/038e84e5-e777-4900-af0b-92b0965fc435)

