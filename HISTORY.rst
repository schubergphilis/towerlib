.. :changelog:

History
-------

0.1 (2018-05-25)
----------------

* First release


0.2.0 (2018-07-27)
------------------

* Refactored code to use entity managers for all tower objects saving a huge amount of network calls and implemented
  filtering

* Removed pipenv locking mechanism as this is broken for python 2.7 completely


0.3.0 (2018-08-01)
------------------

* Added capability to launch job template job


1.0.0 (2018-09-27)
------------------

* Added support for specifying http or https and certificate verifications options
* Extented the editing capabilities of hosts to name, description and enabled status


2.0.0 (2018-10-16)
------------------

* Implemented dynamic attributes in running jobs.
* Implemented cancel capabilities for running jobs.
* Updated the template to python 3.7
* Officially dropped support for python 2.7
