# LBRY_rss
This is a simple python program that allows for creating a rss feed for a video podcast generated from a LBRY channel

# How-To:
- make sure the LBRY desktop application is running, or you have a LBRY server setup
- edit the config file (config.json) to change the claimid (identifies your LBRY channel)
- edit other settings in config file to your satisfaction (Title, contact, keywords, etc)
- run as follows: 

    ./lbrss.py > show_rss.xml
    
- copy file to your webserver and make sure it has the correct permissions. For example: 

    chown www-data:www-data show_rss.xml
    
    chmod 444 show_rss.xml
    
    scp show_rss.xml youruser@webserver:/var/www/
