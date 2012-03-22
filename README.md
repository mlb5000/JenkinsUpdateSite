# JenkinsUpdateSite

## Purpose

If you're like me it's hard to imagine a productive development environment without a tool like Jenkins.  Part of that, however, is keeping everything up to date and in sync with the real world.  With the addition of the "update site" concept in Jenkins this became a lot easier for instances hosted in a place with reliable internet connectivity.  Locations without internet connectivity are basically left to their own devices to manually find, download, and update both Jenkins and relevant plugins on their own.

## Enter JenkinsUpdateSite

This is a simple Python script intended to make the job of managing your own Jenkins update site mirror on your internal network a breeze.

### Requirements

The script requires Python 2.6 or later and the following tools must be available in the PATH:

* wget - Used for mirroring the update site of your choice
* git - Used for managing the whole repository and creating diffs to import over time

## Instructions

Create a new directory to use for the purpose of managing the update site repository.  Don't run this script on your desktop or any folder containing other files or they will be packaged up with your mirror as well.  Simply run JenkinsUpdateSite.py on the command line with the path to your update site and any of the sections you wish to mirror (e.g. plugins, war, windows, etc.).  The updates and art directories will be selected by default so you don't need to select them.  An example call mirroring the war and plugins directories would be:

    $> python JenkinsUpdateSite.py http://mirrors.xmission.com/jenkins/ war plugins

### The First Run

On the first run the script will initialize a git repository in the current directory and start downloading the mirror.  This process will take a while the first time you do it since it has to grab every single file from your selected mirror.  Don't worry though, subsequent updates should go much faster.  Once the downloads complete it will add the files and commit them to the git repository.  Now, just pack up the entire directory (.git directory and all) and transfer it to your remote network.  Yes, it's a lot (probably a handful of DVDs) but your life will be easier from now on.

After you have the files transferred, unpack it on a server and point a web server to it.  Now just go into your Jenkins settings, change the update site URL to point to your server and you're good to go!

### Update Runs

From this point on you just need to run the script any time you want to produce an update package.  These packages will contain the changes since the last time you ran it and will be stored in a patch file stored in the current directory.  Be sure to remove the patch file after you burn it to CD/DVD or it will end up committing it to the git repository next time you run!

Now, just transfer this patch to your remote network, apply it to the git repository you transferred in your first run, and you're done.  Your Jenkins instance(s) will now have access to the latest goodies from the Jenkins community and you can grab a coffee* (or Mountain Dew**).






*, ** - Not an endorsement of coffee or Mountain Dew.