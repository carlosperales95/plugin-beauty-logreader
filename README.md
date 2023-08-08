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

3. Activate the virtual environment
```
source {name_of_your_env}/bin/activate
```

4. Install all of the `pip` dependencies (all are exported into `requirements.txt`)
```
python -m pip install -r requirements.txt
```

5. [TEMPORARY] As of now, there is no import file feature (coming soon), so the app opens any file with the following hardcoded name ([code line where filename is defined](https://github.com/carlosperales95/plugin-beauty-logreader/blob/main/app.py#L42)). Make sure that this file is in the root directory of the project (`/plugin-beauty-logreader`). If you want to replace the filename to open (e.g. `notification.log`), you can change the codeline linked above with the desired filename.
6. Run the app
```
flask run
```
Ready! Now plugin files are prettier to look at
![image](https://github.com/carlosperales95/plugin-beauty-logreader/assets/8956411/48c854c3-63f1-4152-babd-a27858adcbf1)
