pip install wheel
pip uninstall cluedo -y
python setup.py sdist bdist_wheel
pip install dist/cluedo-0.0.1.tar.gz