@echo off
set PYTHONPATH=D:\python-packages
"C:\Users\1\AppData\Local\Python\pythoncore-3.14-64\python.exe" -c "import sys; sys.path.insert(0, 'D:\\python-packages'); from jupyterlab.labapp import LabApp; sys.argv = ['jupyter-lab', '--notebook-dir=D:\\פרויקטים\\smart-task-manager', '--no-browser=False']; LabApp.launch_instance()"
pause
