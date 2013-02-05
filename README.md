NSTrain
=======

NSTrain is a train Scheduler for NS Railways. It provides current train travel information. NPlease note that this application is my own personal project and is in no way officially affliated with NS. 

At the moment, there is no launchpad PPA nor a .deb file. The easiest way to run the application is by,
+ ```git clone git://github.com/krnekhelesh/NSTrain.git```
+ Then run ```python nstrain.py``` from the directory where you cloned the repository into.

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


