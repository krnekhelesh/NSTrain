NSTrain
=======

NSTrain is a train Scheduler for NS Railways. It provides current train travel information. NPlease note that this application is my own personal project and is in no way officially affliated with NS. 

The easiest way to run NSTrain is by adding the PPA and then installing it from there. The PPA support both Ubuntu 12.04 (Precise) and Ubuntu 12.10 (Quantal).

+ ```sudo add-apt-repository ppa:nik90/nstrain && sudo apt-get update && sudo apt-get install nstrain```
+ Search for nstrain in the Unity dash and run it.

The configuration file used by NSTrain is stored at *~/.config/NSTrain*. Delete that file if you want to start fresh.

Feature Suggestion
------------------

If you have any suggestions or feature request please create a new issue in github and I will try my best to implement. You can also otherwise just fork this project, implement the feature and then propose to merge it into the main branch.

Some of the features that I intend to implement in the near future are,

* Add support for showing travel costs, maintenance notices etc.
* Ability to save travel plans for quick use later.
* Add support for Notify my Android to provide push notifications to your Android phone
* Sync user preferences over Ubuntu One, Dropbox etc.
* NSTrain Unity Lens
* NSTrain Ubuntu Appindicator

For Developers
--------------

Github provides a very easier way to contribute to NSTrain. Simply fork the repository, and then clone the forked repository to your system. You can then start developing and then propose a merge request when you think it is ready. I will review your code and then merge it to master.


