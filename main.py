from sheep import Sheep
from wolf import Wolf

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
    sheep_list = [Sheep(), Sheep(), Sheep()]
    wolf = Wolf()
    for sheep in sheep_list:
        print(sheep)
    print(wolf)

    for sheep in sheep_list:
        sheep.move()
    killed_sheep = wolf.move(sheep_list)

    for sheep in sheep_list:
        print(sheep)
    print(wolf)
    if killed_sheep is not None:
        print(f"Wolf killed sheep {killed_sheep.id}")


if __name__ == '__main__':
    main()
