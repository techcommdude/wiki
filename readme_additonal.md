
# Some of the commands necessary to set it up:

**Test it on local first found here:**

 http://127.0.0.1:5000/

**Run this command.  Will likely need to run the collectstatic command before this one to have the latest css files:**

heroku local

**To shut down the local:**

sudo fuser -k 5000/tcp

* **Note:** Will likely need to run "heroku login" in order to connect to Heroku.  Log in to Heroku before you do this.

**Connect to the remote repository:**

heroku git:remote -a wiki-markdown-gfarnell

**Perhaps do this and make sure everything is committed to Git:**

git add .

**Commit the files**

git commit -am "make it better"

**Push the changes to the remote repository on Heroku:**

git push heroku master

Note: the branch could also be called "main" in Git.

* Whitenoise should be installed at the latest version.

**Also sometimes need to run collectstatic locally in the Python command line before pushing to Heroku:**

python ./manage.py collectstatic
