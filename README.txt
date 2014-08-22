Programming Project #3
=======================

I've setup a working copy of this app at

http://pds.liquefied.net:8080/

This is running the django dev server and backed by sqlite, so it may explode if you hit it too hard.


Design Rational
-----------------------

Looking at the sample manifest file, I got the impression that the system might need to handle
large media files such as movies. As such I decided to make the user upload files one
file at a time for two reasons:

* HTTP browsers often have a 2 GB file upload limit
* HTTP does not really support resuming file uploads out-of-the-box

The alternative I had in mind was to upload all files in one form using a formset.

One part of the specification was a little unclear to me:

> Web application should allow user to submit files as many times as they would like
and grid should report each file record accordingly.

I wasn't sure if this meant you could re-upload a file from the grid view, or if that a single manifest
could contain files with the same filename and/or checksum. I took it to mean the latter.

The app stores all files with the filename of their MD5 checksum. They are only renamed back to their
original name on file download. This avoids keeping duplicate copies of large files on disk.

X-sendfile is used to offload file downloads to a server such as nginx.


Setup Requirements
-----------------------

* Python 2.7.x
* virtualenv


Setup
-----------------------

git checkout [...]
cd pds
virtualenv --no-site-packages venv
. venv/bin/activate
pip install -r requirements.txt
fab migrate


Running
-----------------------

fab runserver
open http://localhost:8000/


