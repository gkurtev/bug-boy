# This file is only for experimenting small feature ideas/implementations
import subprocess, os


urls = [
"images/logo.gif",
"https://www.acunetix.com/vulnerability-scanner/",
"index.php",
"categories.php",
"artists.php",
"disclaimer.php",
"cart.php",
"guestbook.php",
"AJAX/index.php",
"search.php?test=query",
"login.php",
"userinfo.php",
"http://www.acunetix.com",
"https://www.acunetix.com/vulnerability-scanner/php-security-scanner/",
"sklasd",
"https://www.acunetix.com/blog/articles/prevent-sql-injection-vulnerabilities-in-php-applications/",
"http://www.eclectasy.com/Fractal-Explorer/index.html",
"http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,29,0",
"Flash/add.swf",
"http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash",
"application/x-shockwave-flash",
"test-mest",
"privacy.php",
"/Mod_Rewrite_Shop/",
"/hpp/",
]

if not os.path.exists('experiments-file.txt'):
    os.mknod('experiments-file.txt')

with open('experiments-file.txt', 'r') as file:
    data = file.read().splitlines()

with open('experiments-file.txt', 'a') as file:
    for url in urls:
        if url not in data:
            print(url)
            file.write(url + "\n")

