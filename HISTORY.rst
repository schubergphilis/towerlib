.. :changelog:

History
-------

0.1.0 (25-05-2018)
------------------

* First release


0.2.0 (27-07-2018)
------------------

* Refactored code to use entity managers for all tower objects saving a huge amount of network calls and implemented
  filtering

* Removed pipenv locking mechanism as this is broken for python 2.7 completely


0.3.0 (01-08-2018)
------------------

* Added capability to launch job template job


1.0.0 (27-09-2018)
------------------

* Added support for specifying http or https and certificate verifications options
* Extented the editing capabilities of hosts to name, description and enabled status


2.0.0 (16-10-2018)
------------------

* Implemented dynamic attributes in running jobs.
* Implemented cancel capabilities for running jobs.
* Updated the template to python 3.7
* Officially dropped support for python 2.7


2.0.1 (25-10-2018)
------------------

* Update template and dependencies


2.0.2 (25-10-2018)
------------------

* Reverted breaking change for upload script


2.0.3 (29-11-2018)
------------------

* Fixed reference in the package for the right github repo


2.1.0 (29-11-2018)
------------------

* Fixed issue https://github.com/schubergphilis/towerlib/issues/11 with some organization entities


2.2.0 (03-12-2018)
------------------

* Implemented group association retrieval (contribution by <aopgenoort@schubergphilis.com>)


2.3.0 (05-12-2018)
------------------

* Added group association and disassociation


2.3.1 (03-01-2019)
------------------

* Bumped Requests


2.3.2 (09-01-2019)
------------------

* Changed library.py 


2.3.3 (07-03-2019)
------------------

* update setup.py 


2.3.4 (04-04-2019)
------------------

* Added missing import of object that caused a bug in the EntityManager crashing, not being able to load it.


2.3.5 (25-07-2019)
------------------

* fix for https://github.com/schubergphilis/towerlib/pull/22


2.3.6 (31-07-2019)
------------------

* Fixed inventory host deletion.


3.0.0 (18-10-2019)
------------------

* Fixed the references to all the objects to be identified by their parent relationship to avoid ambiguity. Full test coverage.


3.0.1 (18-10-2019)
------------------

* bumped dependencies


3.1.0 (18-10-2019)
------------------

* Implemented basic inventory source addition functionality


3.2.0 (18-10-2019)
------------------

* Implemented helper method to create inventory source with an existing credential id.


3.2.1 (01-11-2019)
------------------

* fixed add_credential


3.2.2 (08-11-2019)
------------------

* Added case incensitive search
