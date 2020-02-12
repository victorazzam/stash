Another day, another CTF challenge. 

This one should be super straight forward. Before you go on, go read this article: https://thehackernews.com/2019/10/unix-bsd-password-cracked.html
<hr>
Ok, did you read that article? Good. So your challenge is to crack a password. Just like Ken Thompson, our password will be in a 'known format'.

The format we'll use is: `color-random_year-neverlan_team_member's_name`. (all lowercase)

A sample password could be: `red-1991-s7a73farm`

Here's your hash: `267530778aa6585019c98985eeda255f`. The hashformat is md5.
<hr>
Useful Links:
https://hashcat.net/wiki/doku.php?id=combinator_attack
https://hashcat.net/forum/thread-7571.html

> -BashNinja

**Your flag doesn't need to be in the normal *flag{flagGoesHere}* syntax**