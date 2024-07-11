import os
import re

def test_q1_valid_password():
    content = os.popen('cat passwd_plain.txt | shuf | head -1 | xargs -I{} curl -s --head http://{}@localhost/cgi-bin/q1.sh').read()
    assert '200 OK' in content

def test_q1_bad_password():
    content = os.popen('curl -s --head http://asdf:asdf@localhost/cgi-bin/q1.sh').read()
    assert '401 Unauthorized' in content

def test_q1_no_password():
    content = os.popen('curl -s --head http://localhost/cgi-bin/q1.sh').read()
    assert '401 Unauthorized' in content

def test_q2_valid_password():
    content = os.popen('curl -s --head http://anna:password@localhost/cgi-bin/q2.sh').read()
    assert '200 OK' in content

def test_q2_bad_password():
    content = os.popen('curl -s --head http://asdf:asdf@localhost/cgi-bin/q2.sh').read()
    assert '401 Unauthorized' in content

def test_q2_no_password():
    content = os.popen('curl -s --head http://localhost/cgi-bin/q2.sh').read()
    assert '401 Unauthorized' in content

def test_q3():
    content = os.popen('./q3.sh').read()
    assert re.search(r'anna.*password', content) 
    
def test_q4():
    content = os.popen('./q4.sh').read()
    assert re.search(r'anna.*daniel', content) 
