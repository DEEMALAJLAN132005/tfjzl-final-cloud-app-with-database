
**General Notes**

An `onlinecourse` app has already been provided in this repo upon which you will be adding a new assesement feature.

- If you want to develop the final project on Theia hosted by [IBM Developer Skills Network](https://labs.cognitiveclass.ai/), you will need to create the same project structure on Theia workspace and save it everytime you close the browser
- Or you could develop the final project locally by setting up your own Python runtime and IDE
- Hints for the final project are left on source code files
- You may choose any cloud platform for deployment (default is IBM Cloud Foundry)
- Depends on your deployment, you may choose any SQL database Django supported such as SQLite3, PostgreSQL, and MySQL (default is SQLite3)

**ER Diagram**
For your reference, we have prepared the ER diagram design for the new assesement feature.

![Onlinecourse ER Diagram](https://github.com/ibm-developer-skills-network/final-cloud-app-with-database/blob/master/static/media/course_images/onlinecourse_app_er.png)


## Completed final-project assessment implementation

The online-course app includes Question, Choice, and Submission models; Django
admin registration and inline editors; the Bootstrap exam form; submission
handling; question scoring; and an exam result page. The implementation also
includes automated assessment tests.

### AI-graded submission URLs

1. [Task 1 - models.py](https://github.com/DEEMALAJLAN132005/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/models.py)
2. [Task 2 - admin.py](https://github.com/DEEMALAJLAN132005/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/admin.py)
3. Task 3 - screenshot `03-admin-site.png`
4. [Task 4 - course_details_bootstrap.html](https://github.com/DEEMALAJLAN132005/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/templates/onlinecourse/course_details_bootstrap.html)
5. [Task 5 - views.py](https://github.com/DEEMALAJLAN132005/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/views.py)
6. [Task 6 - urls.py](https://github.com/DEEMALAJLAN132005/tfjzl-final-cloud-app-with-database/blob/main/onlinecourse/urls.py)
7. Task 7 - screenshot `07-final.png`

For the required screenshots, open the **Actions** tab, run
**Verify Django Online Course Assessment**, and download the
`onlinecourse-assessment-evidence` artifact. The workflow creates a disposable
SQLite database and a temporary demonstration account, runs Django tests,
launches the site, and captures screenshots from a real headless browser.
If GitHub disables Actions on this fork, enable Actions for this repository first.

### Running the application in a lab or local Python environment

Install compatible dependencies (Django 4.2, Pillow 10), then:

```bash
python3 manage.py makemigrations onlinecourse
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

The UI is under `/onlinecourse/` and the admin site is under `/admin/`.
Create a course, lesson, question with two choices (mark the correct choice),
and a learner enrollment before trying the examination form.
The tests can be run with `python3 manage.py test onlinecourse -v 2`.

**Note:** This is a teaching/demo application. The starter Django settings
use development-only defaults and are not configured for production.
