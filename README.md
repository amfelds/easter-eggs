# Whitegold Color Corrector

[For some reason](http://www.buzzfeed.com/catesish/help-am-i-going-insane-its-definitely-blue), white and gold things appear blue and black to a large number of people. This app automatically corrects the colors in your images so they appear properly white and gold to everyone.

Read more about webhooks [the Dropbox developers site](https://www.dropbox.com/developers/webhooks/tutorial).

You can try the example yourself by visiting [whitegold.herokuapp.com](https://whitegold.herokuapp.com).

## Running the sample yourself

This sample was built with Heroku in mind as a target, so the simplest way to run the sample is via `foreman`:

1. Copy `.env_sample` to `.env` and fill in the values.
2. Run `pip install -r requirements.txt` to install the necessary modules.
3. Launch the app via `foreman start` or deploy to Heroku.

You can also just set the required environment variables (using `.env_sample` as a guide) and run the app directly with `python app.py`.

## Deploy on Heroku

You can deploy directly to Heroku with the button below. First you'll need to create an API app via the [App Console](https://www.dropbox.com/developers/apps). Make sure your app has access to files (not just datastores), and answer "Yes - My app only needs access to files it creates" to ensure your app gets created with "App folder" permissions.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

Once you've deployed, you can easily clone the app and make modifications:

```
$ heroku clone -a new-app-name
...
$ vim app.py
$ git add .
$ git commit -m "update app.py"
$ git push heroku master
...
```


Yard copy ref: 'M7Zx2DJjNXYxbjJsN3p6YQ'
client.add_copy_ref('M7Zx2DJjNXYxbjJsN3p6YQ','/Yard')