# test_execution_web_app
A web application that provides a central place to run Python-based tests.

** How to run this application **
- First confirm if you have all dependancies:

    `cd test_execution_web_app`

    `pip install -r requirements.txt`
- Then setup mysql db:

    `python make_db.py`
- Above command will create mysql database and table
- Run application:

    `python server.py`
- Then open browser and enter url: http://127.0.0.1:5000/
- You will see HTML form. Fill proper values and submit it.
  I have added sample test file under autotest/tests. You can use it for custom path.
  Templates are just names of different test functions.
  If test fails, status shows Failed with hyperlink which directs to stacktrace of failed test.
