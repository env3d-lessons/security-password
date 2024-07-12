import os
import re
import base64

def test_q1_valid_password():
    idpass = base64.b64encode(b'mark:111111').decode('utf-8')
    cmd = f'HTTP_AUTHORIZATION="Basic {idpass}" ./q1.sh'
    content = os.popen(cmd).read()    
    assert 'ey' in content

def test_q1_bad_password():
    idpass = base64.b64encode(b'aaaa:bbbb').decode('utf-8')
    cmd = f'HTTP_AUTHORIZATION="Basic {idpass}" ./q1.sh'
    content = os.popen('./q1.sh').read()
    assert '401' in content

def test_q1_no_password():
    content = os.popen('./q1.sh').read()
    assert '401' in content

def test_q2_valid_password():
    idpass = base64.b64encode(b'anna:password').decode('utf-8')
    cmd = f'HTTP_AUTHORIZATION="Basic {idpass}" ./q2.sh'
    print(cmd)
    content = os.popen(cmd).read()
    assert len(content) > 0
    assert 'ey' in content, f'{idpass}'

def test_q2_bad_password():
    idpass = base64.b64encode(b'aaaa:bbbb').decode('utf-8')  
    cmd = f'HTTP_AUTHORIZATION="Basic {idpass}" ./q2.sh'
    content = os.popen(cmd).read()
    assert '401' in content

def test_q2_no_password():
    content = os.popen('./q2.sh').read()
    assert '401' in content

def test_q3():
    content = os.popen('./q3.sh').read()
    assert re.search(r'anna.*password', content) 
    
def test_q4():
    content = os.popen('./q4.sh').read()
    assert re.search(r'anna.*daniel', content) 
