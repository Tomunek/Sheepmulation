from sheep import Sheep

WELCOME_STRING = r"""
 ____   _                                           _         _    _               
/ ___| | |__    ___   ___  _ __   _ __ ___   _   _ | |  __ _ | |_ (_)  ___   _ __  
\___ \ | '_ \  / _ \ / _ \| '_ \ | '_ ` _ \ | | | || | / _` || __|| | / _ \ | '_ \ 
 ___) || | | ||  __/|  __/| |_) || | | | | || |_| || || (_| || |_ | || (_) || | | |
|____/ |_| |_| \___| \___|| .__/ |_| |_| |_| \__,_||_| \__,_| \__||_| \___/ |_| |_|
                          |_|                                                      
By Tomasz Kowalczyk & Jakub Kalinowski
"""


def main():
    print(WELCOME_STRING)
    sheep = Sheep()
    print(sheep)
    sheep.move()
    print(sheep)


if __name__ == '__main__':
    main()
