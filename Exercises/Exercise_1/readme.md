Description for task 1-4

Task 1:
When going to the DeDiS Secure Login page and go into the scorce code for the webpage one can
find a function called "superencryption(msg,key)". This function takes in a msg, which if we
look further down in the code is the username the user supplies, and a key, which can also 
be seen to be a variable in the code called mySecureOneTimePad. So one can see that the 
function will use the username/email address and the key variable to calculate the password 
of the user and join the password with the username. So to find my password I took the 
superencryption function and copied into a online javascript compiler to run the function 
with my epfl email address and the same mySecureOneTimePad string as in the code. This gives
me the password after my email in the output. Log in to get the token.

Task 2:
Looking into the scorce code for the Evil Cors page one can see that when we trigger a click 
a function that will run a postJSON function. The reply from this function decides if we 
are allowed to hack and spy. This function uses the webpage cookie to determine if a user
has the rights to hack and spy. Inspecting the element and going to Storage let us see this
cookie. In the cookie we can see that there is a field called value, which is encoded with 
base64. Uncoding with base64 reveles that it conatins information about the user. Changing
the information about the user from user to administrator, encoding with base64 and pasting
the newly encoded string into the value field of the cookie lets us press the hack and spy 
button, which now will return a 200 response as the cookie says that we are a administrator.
We can now retrive the token.

Task 3 and 4:
For both of these exercises navigate to the mkdir directory, which you can find in the .tar
called MartinVold_300510_task3and4. Here run the following commands: 
1. sh run_dockers.sh <your_personal_epfl_email_address>
2. docker exec -it attacker /bin/bash (goes into root@attacker)
3. iptables -t nat -A POSTROUTING -j MASQUERADE
4. iptables -A FORWARD -s 172.16.0.2 -p tcp --dport 80 -j NFQUEUE --queue-num 0

For task 3:
Run python3 shared/interceptor.py (inside root@attacker), after the generator has send the 
correct packet it will be intercepted and we will change the shipping_address field and get
a 200 answer code together with the token.

For task 4: 
Run python3 shared/interceptor.py (inside root@attacker), after we have intercepted all the
packets with passwords and emails that satisfies the requirements we will post them and get
the a 200 answer code and the token.

PS: You might have to use sudo infront the first two commands