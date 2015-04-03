live version: http://easter-eggs.herokuapp.com/

blog post: https://blogs.dropbox.com/developers/2015/04/get-easter-eggs-in-your-dropbox/

This app was built with heroku as the target for deployment. Heroku makes it easy to create a python app and get a redis add-on.

If you're deploying this app yourself, you'll need to create the copy_refs for the easter egg images and the Yard folder. You'll also need to make your own Yard folder tree (it's fun!) (you can also copy mine by running the app and linking it to your Dropbox account, then copy/pasting the whole app folder to another spot in your Dropbox - make sure you remove the egg files, or the game will be too easy!)

You need your own copy_refs to match with your Dropbox API app key (see https://www.dropbox.com/developers/apps). 

0. Copy .env_sample to an .env file and change the values to match your own config vars in heroku.

1. To create the copy refs, follow the first part of the python tutorial for connecting to your Dropbox app: https://www.dropbox.com/developers/core/start/python

2. Once you have a client object, use it to call create_copy_ref() (see: https://www.dropbox.com/developers/core/docs/python) from the directory where your own easter egg images and Yard folder are located.

>>> egg_ref_1 = client.create_copy_ref('<path to egg file 1>')['copy_ref']
etc.
>>> yard_ref = client.create_copy_ref('<path to /Yard root>')['copy_ref']

3. Add the egg egg_ref_<#> strings to the egg_refs object in app.py (line 26)
4. Add the yard_ref string to the add_copy_ref statement in the process_user function in app.py (line 81)

IMPORTANT: Don't move, delete, or rename your egg files or your /Yard folder - if you do, your copy_refs will break and your app won't work :(