from app import app

app.config["MONGODB_SETTINGS"] = {'DB': 'lemcoff'}
app.config["SECRET_KEY"] = '1234'
