# Password Management

All exercises to be completed on codespaces inside the assignment repo directory.
Web server configuration are all setup and the repo directory is mapped to

```
https://${CODESPACE_NAME}-80.app.github.dev/cgi-bin/
```

## Q1
Notice that for simplicity purposes, the script 
[https://github.com/env3d/jwt-lessons/blob/main/02-hmac-token.sh](https://github.com/env3d/jwt-lessons/blob/main/02-hmac-token.sh)
does not actually check for passwords.  In this exercise, we explore how passwords are stored.

The simplest way to store passwords is by storing it as simple name-value pairs, something like this passwd_plain.txt.

Make a copy of the 02-hmac-token.sh script, call it q1.sh, and modify it so that your script would check both the 
username and password against the password file [passwd_plain.txt](passwd_plain.txt.).

If the id/password combination does not exist in the passwd_plain.txt file, you will return status 401.  
Otherwise, your script would return a JWT token.

Deploy the script to a web server, and provide an example curl call.

## Q2
Using plain text to store passwords is very insecure.  If a malicious hacker got a hold of the file, 
the hacker would gain access to all the actual passwords.  A better way to store passwords is to store 
them as hashes.  The file [passwd_sha.txt](passwd_sha.txt) stores passwords as sha256sum.  

The hash in `passwd_sha.txt` is created using the `sha256sum` utility.  For example, the entry for 
the password 12345 is produced using the following command:

```console
echo '12345' | sha256sum | cut -f 1 -d ' '
```

Since sha256sum is a one-way hash, getting a hold of the password file does not mean you’ll have access 
to the actual password.

Make a copy of q1.sh and call it q2.sh.  Then modify q2.sh so that it checks against the sha256sum instead 
of the plain text file.

Since you don't have access to the original passwords, it's actually really difficult to test your login script 
against the passwd_sha.txt file.  Create a new entry in the passwd_sha.txt so you can test your q2.sh properly.  

## Q3
Using hash as password storage is much more secure than plain text, since even if a hacker has access to the password 
file (or database), they would not know the actual password. 

However, since we are using a simple sha256sum, a hacker can perform a few types of attack:

  - Discover password reuse:  We can simply run a unique on all the password hashes to discover
    if a password has been reused, as follows:

    ```console
    cut -f 2 -d ':' passwd_sha.txt | sort -u
    ```

    Looks like we have many cases of password reuse on our sample dataset ;-)

  - the hacker can still recover the original passwords quickly by performing the following steps:
    1.  pre-computing the hash on a set of potential passwords.  In the case of our sample dataset, 
        since we know that the passwords are chosen from the first 100 entries of the common password 
        list, I have calculated all the 100 password hashes into a file called `raninbow.txt`, delimited
        by ':' character
    1.  To lookup a password for a user, we simply `grep` the user's hash from `rainbow.txt`, as follows:

        ```console
        $ # Let's say we want to lookup daivd's password, we first find david's hash

        $ grep david passwd_sha.txt 
        david:6b3a55e0261b0304143f805a24924d0c1c44524821305f31d9277843b8a10f4e

        $ # We now grep this hash from the rainbow.txt to find the original password
        $ grep 6b3a55e0261b0304143f805a24924d0c1c44524821305f31d9277843b8a10f4e rainbow.txt
        password:6b3a55e0261b0304143f805a24924d0c1c44524821305f31d9277843b8a10f4e

        $ # Looks like david's password is 'password', let's test it against our q2.sh
        $ curl --head david:password@localhost/cgi-bin/q2.sh
        HTTP/1.1 200 OK
        Date: Thu, 11 Jul 2024 20:22:48 GMT
        Server: Apache/2.4.59 (Debian)
        Vary: Accept-Encoding
        Content-Type: text/plain

        ```

Write a script call q3.sh to recover all the passwords using the above concept.  Here's 
the basic script structure to get your started:

```bash
#!/bin/bash

for IDPASS in $(cat passwd_sha.txt)
do
    ID=$(echo $IDPASS | cut -f 1 -d ':')
    HASH=$(echo $IDPASS | cut -f 2 -d ':')    

    # This is where you crack the password by grepping the hash
    PASSWORD=

    echo -n "$ID:$PASSWORD"
done
```

## Q4
To mitigate the "rainbow table" attack highlighted in Q3, passwords are usually "salted".

The current best practice is to use the blowfish/bcrypt algorithm where the password and 
salt are generated together.  The openssl command will produce such a password for you.  
You can run the openssl command as follows:

```console
[ec2-user@ip-172-31-13-169 password-lessons]$ openssl passwd -1 12345
$1$X4gWLB5H$MBKnn5VEYuyoN6cS7bQo2/

[ec2-user@ip-172-31-13-169 password-lessons]$ openssl passwd -1 12345
$1$/6avCSjQ$6A31CMaSwmmzOxYlpHxrY1

[ec2-user@ip-172-31-13-169 password-lessons]$ openssl passwd -1 12345
$1$vN2MROPo$7pZX4h7r2v1KrCJJ8ndAb/
```

Notice how the output has different hash value for the same password?  That's because the random 
salt is integrated into the password hash itself.  The output string is delimited by the $ character and
has the following format:

```
${algorithm}${salt}${hash}
```

We use the algorithm "1" to encrypt passwords, and the salt value is randomly assigned.

If we know the salt, we can verify a password by providing a specific salt value to openssl,
as follows:

```console
[ec2-user@ip-172-31-13-169 password-lessons]$ openssl passwd -1 -salt vN2MROPo 12345
$1$vN2MROPo$7pZX4h7r2v1KrCJJ8ndAb/
```

There are numerous advantages in using salted passwords:

  1. We can no longer find out if passwords have been reused, since each password hash is
     unique with the injection of random salt.

  1. We need to crach each password indiviaully, instead of creating a lookup table for 
     password hashes (rainbow.txt)

The file passwd_salted.txt contains passwords encrypted using `openssl passwd` as seen above.  
Create a q4.sh that cracks all the passwords in [passwd_salted.txt](passwd_salted.txt).

Below is a starter script:

```bash
#!/bin/bash

# Cracking salted passwords

# The pool of passwords comes from the first 100 common passwords
PASSWORD_URL='https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt'
COMMON_PASSWORDS=$(curl -s $PASSWORD_URL | head -n 100)

# We now read the password file.  For each login, we try the sha256sum of each of the common password
for IDPASS in $(cat passwd_salted.txt)
do
    ID=$(echo $IDPASS | cut -f 1 -d ':')
    TARGET=$(echo $IDPASS | cut -f 2 -d ':')
    SALT=$(echo $TARGET | cut -d '$' -f 3)    
    for PASS in $COMMON_PASSWORDS
    do
	    # We need to create a SALTED version of each password
        SALTED=
	    if [[ "$SALTED" == "$TARGET" ]]
	    then
	        echo "$ID has the password $PASS"
	    fi
    done
done
```