pip uninstall hyde-lang -y
pip install hyde-lang

python setup.py install

echo 'print "----Welcome to Hyde!----";' \
     'print "If you can see this message,";' \
     'print "Hyde is installed correctly!";' | hyde