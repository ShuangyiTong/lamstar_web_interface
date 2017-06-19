# lamstar_web_interface
A web project powered by Django for artificial neural network feeding and analysis.
## What is it
This is a very early copy of the project. I lost most progress during the failure of my SanDisk SSD.

As you can see, the code here looks messy and inconsistent. I actually rewrote most stuff later, but SSDs are really difficult to do data recovery.

So I would say this project is useless now.
## Why do I put a useless project here
Ah, that is because I am applying for a summer program, and they want a web project. (I know this one looks crappy! But this is the only one I've done!)
## The future of this project
A loss may turn out to be a gain (Chinese: 塞翁失马，焉知非福). I might start this project again, but definitely looks very different.

It seems not a good idea to directly integrate computation part into a web project, I probably will write a command line program first.

In the newest version of the project, which is already lost, all operations are divided into three categories, model computation, script execution (for data pre-processing and post-processing), and DB operations. Three categories are managed by three different modules. I want to combine everything in to one basic element, maybe just call it a `function`. Of course, these are very general ideas, and require much more considerations before starting the real job.
## To start it
Need extra files

* jquery
* jquery.tagsinput
* bootstrap
* nprogress
* switchery

this files can be obtained from https://github.com/puikinsh/gentelella/vendors

put under `/lamstar_web_interface/main/static/main/vendors`

then start Django development server `python3 manage.py runserver`

Tested on python 3.5.2, chrome 59

Windows 10.0.14393 and Fedora 25
## About backup
* I would never put anything important just on SSDs (I would very subjectively say Intel has better quality SSDs)
* I would write a small script to auto-sync important files on at least two disks
