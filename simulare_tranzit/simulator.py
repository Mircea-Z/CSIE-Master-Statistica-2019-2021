import json
from objects.app import App

settings = open('settings.json','r').read()
settings = json.loads(settings)

app = App(settings)
app.run()
settings = app.settings

with open('settings.json','w') as ef:
    ef.write(json.dumps(settings, indent=2))
