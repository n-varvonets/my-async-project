# my-async-project 

1. During project development Python 3.6 and the operating system Windows 10 were used.<br>
2. Run this command to install requirements:\
<b>pip install -r requirements.txt</b>

3. To run the server:\
<b>python server.py</b>

4. To run the client:\
<b>python client.py</b>  
5. To check allure report make sure you have <a href="https://docs.qameta.io/allure/#_installing_a_commandline">allure</a> installed.\
Generate allure report:\
<b>python -m pytest --alluredir results  tests/ </b>\
Run allure to watch report:\
<b>allure serve ./results </b>

