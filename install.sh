pip uninstall hyde -y
pip install -e .

python setup.py install

echo 'print "----Welcome to Hyde!----";' \
     'print "If you can see this message,";' \
     'print "Hyde is installed correctly!";' | hyde