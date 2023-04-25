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


3.2.3 (06-12-2019)
------------------

* Fix pagination for filtering.


3.2.4 (12-12-2019)
------------------

* fixed pagination!!


3.2.5 (19-12-2019)
------------------

* Fixed underlying _update_values method to prevent overwrite of nested dicts in AWX 9.0.1.


3.2.6 (19-12-2019)
------------------

* Linting and pipfile dependency fixes.


3.2.7 (14-03-2020)
------------------

* Added support for python 3.6 by adding dataclasses package with marker


3.2.8 (14-03-2020)
------------------

* Removed unwanted development files from the final package.


3.2.9 (29-05-2020)
------------------

* Added support for Schedules


3.2.10 (09-06-2020)
-------------------

* bumped requests


3.3.0 (06-07-2020)
------------------

* Implemented capabilities to add organization object roles to team permissions.


3.4.0 (09-10-2020)
------------------

* bump requests


3.4.1 (16-10-2020)
------------------

* Bumped dependencies


3.4.2 (06-11-2020)
------------------

* Added missing development dependency and bumped dependencies to latest patch versions.


3.5.0 (02-12-2020)
------------------

* Changed the credential creation process to make team and Owner name optional


3.6.0 (06-01-2021)
------------------

* Extended JobTemplate with some methods and made credential not required on job template creation.


3.6.1 (06-01-2021)
------------------

* Loosened up dependencies.


3.6.2 (04-02-2021)
------------------

* Fix missing f-string.


3.7.0 (09-03-2021)
------------------

* Implemented survey specification retrieval.


3.7.1 (26-04-2021)
------------------

* Bumped dependencies.


3.7.2 (26-04-2021)
------------------

* Bumped dependencies.


3.7.3 (02-06-2021)
------------------

* Bumped dependencies and fixed a couple of bugs on job attribute retrieval.


3.8.0 (01-07-2021)
------------------

* Features implemented by spirit21.


3.9.0 (01-07-2021)
------------------

* Features implemented by spirit21.


3.9.1 (10-09-2021)
------------------

* Added the capability to launch a job template with non-default SCM branches.


3.9.2 (10-09-2021)
------------------

* Linted.


3.9.3 (11-07-2022)
------------------

* Fixed bug with job execution.


3.9.4 (01-09-2022)
------------------

* Fixed some redirects, bumped dependencies.


3.10.0 (04-10-2022)
-------------------

* Allows unsetting of default values in launch job courtesy of https://github.com/EliasBoulharts


3.11.0 (11-11-2022)
-------------------

* added summary_fields in JobTemplate


3.12.0 (10-03-2023)
-------------------

* Implement aws credentials and expose input sources.


3.13.0 (25-04-2023)
-------------------

* Add default timeout.
