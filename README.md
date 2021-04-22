towerlib
========

This repo was originally forked from https://github.com/schubergphilis/towerlib. To have a look at the original readme,
refer to the README.rst file.

'towerlib' is a python library to interface with ansible tower's (awx) api. We (spirit/21) have added many additional 
functions in `towerlib.py` file on top of the orignal file from schubergphilis's towerlib project.


* Documentation: https://towerlib.readthedocs.org/en/latest



Development and Testing
====================
The following high level methods have been added to the `towerlib.py` file:
1. `get_all_projects`
2. `update_all_projects`
3. `update_project_by_id`
4. `update_project_by_scm_url`
5. `update_project_by_branch_name`
6. `get_all_job_templates`
7. `get_job_templates_by_project`
8. `change_job_data`
9. `change_project_of_job_template`
10. `change_project_of_job_template_to_prod_branch_project`
11. `change_job_type`
12. `project_exists`
13. `get_all_credential_types`
14. `get_credential_id_from_existing_project`
15. `get_project_id_by_branch_name`
16. `get_production_branch_project_id`
17. `get_playbooks_by_branch_name`
18. `get_production_branch_playbooks`
19. `get_ansible_facts_by_host_id`
20. `get_all_inventories`
21. `get_all_hosts`
22. `get_all_credentials`
23. `get_hosts_by_inventory_id`
24. `get_all_jobs`
25. `get_jobs_by_name`
26. `get_project_updates`
27. `get_project_updates_by_project_name`
28. `get_all_hosts_from_non_smart_inventories`
29. `get_project_updates_by_project_id`
30. `get_job_events_by_host`
31. `get_job_dates_by_host`
32. `get_groups_with_inventory_host_id`
33. `get_all_groups`
34. `get_groups_by_host`
35. `disable_scm_update_on_launch_for_all_projects`
36. `search_generic_item_by_keyword`

For further development, one needs to create a branch from the master branch and develop in the new branch.

CI/CD
=====================
- ### Development in Spirit/21 ###
After the intended development is done, before the development or feature branch is merged with the master branch, 
one must change(upgrade) the version number in the `.VERSION` file. Once the development or feature branch is merged 
with master, there should be a build in the jenkins server, which will publish the newest towerlib in the nexus server. 
To understand more about CI/CD part, one can have a look at the jenkinsfile in this repository. Related link to the
Jenkins Pipeline is: https://javadev.spirit21.de/jenkins/job/s21-automation/job/Multibranch-pipeline-for-towerlib-module/

- ### Development in the Upstream Towerlib ###
When there is newer code/version published in the upstream (github towerlib) version, there should be an automatic pull
request created in the bitbucket towerlib repo. This is done with the help of two jenkins job:
 1. https://javadev.spirit21.de/jenkins/job/s21-automation/job/towerlib-upstream-sync-1/ : this job gets triggered upon 
 new commits in the master branch of upstream (github towerlib) version and then it triggers the following job.
 2. https://javadev.spirit21.de/jenkins/job/s21-automation/job/towerlib-upstream-sync-2/ : this pipeline job runs a 
 python script, which creates a pull request in the bitbucket towerlib repo.

Installation
=====================
To install in the local machine one can run the following command and provide necessary credentials when asked:
```
python3 -m pip install --upgrade towerlib --index-url https://nexus.spirit21.com/repository/pypi-all/simple -v --trusted-host nexus.spirit21.com'''
```

Usage
================
```python
from towerlib import Tower
tower_host = 'spsdekarlscf002'
tower_user = "tower_user"
tower_pass = "tower_pass"
towerlib_obj = Tower(tower_host, tower_user, tower_pass, secure=True, ssl_verify=False)
```

After we have initiated the towerlib object, if we want to retrieve all the projects fo that tower host for example, we 
can code like the following:

```python
projects = towerlib_obj.get_all_projects()
```
This would store all the projects in the `projects` variable as `project` entity of of the towerlib. 

Author
================
Iqbal Nazir
