@echo off
call conda activate py310
pip install taichi pybind11 pefile machomachomangler
python setup.py bdist_wheel
python scripts\win\win_auto_repair.py --py 310 --version 0.2.6
