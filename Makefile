pip_install:
	pip install -U -r requirements/base.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn --default-timeout=100

start_pilgrimage:
	venv/bin/python3 manage.py runserver 0.0.0.0:8080
