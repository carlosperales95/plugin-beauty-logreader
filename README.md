# plugin-beauty-logreader


> [!IMPORTANT]
> At the moment the only supported plugin format is for `Adobe Commerce`
> - `Shopware6` - Planed Soon
> - `SFCC` - Planned Soon

## Getting Started
1. Clone the repo
2. `cd` into the project folder (`/plugin-beauty-logreader`) and create a virtual environment for this python app, replacing `{name_of_your_env}` (example: `env`)
```
python -m venv {name_of_your_env}
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
<details>
  
<summary><b>Ready!</b></summary>

Now plugin files are prettier to look at (Should start in your [localhost](http://127.0.0.1:5000/))

![image](https://github.com/carlosperales95/plugin-beauty-logreader/assets/8956411/f3264ebf-d397-4881-9de1-2d953f33a30d)

</details>


## How To import logs into the app

You can select one (or many) files using the File Import functionality. App will add all of the log entries together and display them as a table (same as above). 
It will also save the case to avoid having to reimport everything again each time the app is closed.

![image](https://github.com/carlosperales95/plugin-beauty-logreader/assets/8956411/b1e48d68-63be-4df2-be20-be7c81121ddc)

