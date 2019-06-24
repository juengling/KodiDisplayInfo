#!/usr/bin/python
# KodiDisplayInfo v20190619-pre
# Autor: Bjoern Reichert <opendisplaycase[at]gmx.net>
# License: GNU General Public License (GNU GPLv3)
#
# Modified by Daniel Siegmanski <webmaster[at]dsiggi.de>
#
# v4.0      Converted to python3
# v4.1      Neue Anzeigemethode für Musik hinzugefügt "musicthumb"
# v20190330  Zu neuer Versionsnummerrierung gewechselt, CHANGELOG nun in eigenständiger Datei

import os
import sys
import datetime
import pygame
import configparser
from classes.Helper import Helper
from classes.DrawToDisplay_Default import DrawToDisplay_Default
from classes.KODI_WEBSERVER import KODI_WEBSERVER
#from classes.DrawToDisplay_MusicThumbnail import DrawToDisplay_MusicThumbnail

basedirpath = os.path.dirname(os.path.realpath(__file__)) + os.sep

_ConfigDefault = {
    "basedirpath":              basedirpath,

    "mesg.error":                 31,
    "mesg.warning":               33,
    "mesg.info":                  36,

    "KODI.webserver.host":            "localhost",
    "KODI.webserver.port":            "8080",
    "KODI.webserver.user":            "",
    "KODI.webserver.pass":            "",
    
    "display.resolution":       "320x240",   
    
    "config.screenmodus_music":       "thumbnail",

    "color.black":              [0, 0, 0],
    "color.white":              [255, 255, 255],
    "color.red":                [255, 0, 0],
    "color.orange":             [255, 153, 0],
    "color.green":              [102, 255, 0]
    }

helper = Helper(_ConfigDefault)

# init config
helper.print_info("Parse Config")
configParser = configparser.RawConfigParser()
configFilePath = r''+basedirpath+'config.txt'
configParser.read(configFilePath)

#<editor-fold desc="CONFIG">
# check config
if configParser.has_option('CONFIG', 'SCREENMODUS_MUSIC'):
    temp = configParser.get('CONFIG', 'SCREENMODUS_MUSIC')
    if temp == "thumbnail":
        _ConfigDefault['config.screenmodus_music'] = temp
    else:
        helper.print_warning("[CONFIG] SCREENMODUS_MUSIC not set correctly - default ist active!")

if configParser.has_option('DISPLAY', 'RESOLUTION'):
    temp = configParser.get('DISPLAY', 'RESOLUTION')
    xposition = temp.find("x")
    width = round(int(temp[:xposition]))
    height = round(int(temp[xposition + 1:]))
    _ConfigDefault['display.resolution_height'] = height
    _ConfigDefault['display.resolution_width'] = width
    _ConfigDefault['display.resolution'] = width, height

if configParser.has_option('KODI_WEBSERVER', 'HOST'):
    _ConfigDefault['KODI.webserver.host'] = configParser.get('KODI_WEBSERVER', 'HOST')
if configParser.has_option('KODI_WEBSERVER', 'PORT'):
    _ConfigDefault['KODI.webserver.port'] = configParser.get('KODI_WEBSERVER', 'PORT')
if configParser.has_option('KODI_WEBSERVER', 'USER'):
    _ConfigDefault['KODI.webserver.user'] = configParser.get('KODI_WEBSERVER', 'USER')
if configParser.has_option('KODI_WEBSERVER', 'PASS'):
    _ConfigDefault['KODI.webserver.pass'] = configParser.get('KODI_WEBSERVER', 'PASS')

if configParser.has_option('COLOR', 'BLACK'):
    _ConfigDefault['color.black'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'BLACK'))
if configParser.has_option('COLOR', 'WHITE'):
    _ConfigDefault['color.white'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'WHITE'))
if configParser.has_option('COLOR', 'RED'):
    _ConfigDefault['color.red'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'RED'))
if configParser.has_option('COLOR', 'GREEN'):
    _ConfigDefault['color.green'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'GREEN'))
if configParser.has_option('COLOR', 'ORANGE'):
    _ConfigDefault['color.orange'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'ORANGE'))

# Display FB
if configParser.get('DISPLAY', 'FBDEV') != "":
    os.environ["SDL_FBDEV"] = configParser.get('DISPLAY', 'FBDEV')
#</editor-fold>

def main_exit():
    pygame.quit()
    sys.exit()

def main():
    time_now = 0
    media_title = ""
    old_album = ""
    thumbnail = ""

    helper.print_info("Start: KodiDisplayInfo")
    helper.print_info("Resolution is: " + str(_ConfigDefault['display.resolution']))

    pygame.init()
    screen = pygame.display.set_mode(_ConfigDefault['display.resolution'], 0, 32)
    pygame.display.set_caption('KodiDisplayInfo')
    pygame.mouse.set_visible(1)
    clock = pygame.time.Clock()
    
    RELOAD_SPEED = 750
    
    # create a bunch of events
    reloaded_event = pygame.USEREVENT + 1
    
    # set timer for the event
    pygame.time.set_timer(reloaded_event, RELOAD_SPEED)

    draw_default.setPygameScreen(pygame, screen)
    # if _ConfigDefault['config.screenmodus_music'] == "thumbnail":
        # draw_musicthumbnail.setPygameScreen(pygame, screen, draw_default)
        # draw_musicthumbnail.setPositions()

    running = True
    # run the game loop
    try:        
        while running:
            clock.tick(4) # 4 x in one seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            time_now = datetime.datetime.now()
            # start draw
            screen.fill(_ConfigDefault['color.black']) #reset
            
            playerid, playertype = KODI_WEBSERVER.KODI_GetActivePlayers()
            if playertype == "audio1" and int(playerid) >= 0:
                # Artist, Album und Titel herausfinden
                media_artist, media_album, media_title = KODI_WEBSERVER.KODI_GetItem(playerid, playertype)
                speed, media_time, media_totaltime = KODI_WEBSERVER.KODI_GetProperties(playerid)
                # Anzeigemodus "Thumbnail" ist gewählt
                if _ConfigDefault['config.screenmodus_music'] == "thumbnail":
                    # Neues Cover nur anfordern wenn sich das Album geändert hat
                    if not media_album == old_album and media_album != "#error":
                        # Die URL für das Cover herausfinden
                        url = KODI_WEBSERVER.KODI_GetCoverURL(playerid)
                        # Das Cover nur herunterladen wenn es es auch gibt
                        if not url == "":
                            thumbnail = KODI_WEBSERVER.KODI_DownloadCover(url)
                            helper.print_info("Found thumbnail for: " + str(media_album))
                        else:
                            helper.print_warning("Can't find a thumbnail for: " + str(media_album))
                            thumbnail = "#empty"

                        if media_album != "#error":
                            old_album = media_album

                    else:
                        if media_album == "":
                            thumbnail = "#empty"

                    # Das Cover auf's Display bringen
                    # draw_musicthumbnail.DrawMusicInfo(thumbnail, media_artist, media_album, media_title)
            else:
                # API has nothing
                media_title = ""
                draw_default.drawLogoStartScreen(time_now)
            

            pygame.display.flip()


        helper.print_info("[end] bye ...")
        main_exit()
    except SystemExit:
        main_exit()
    except KeyboardInterrupt:
        main_exit()

if __name__ == "__main__":
    draw_default = DrawToDisplay_Default(helper, _ConfigDefault)
    
    # if _ConfigDefault['config.screenmodus_music'] == "thumbnail":
        # draw_musicthumbnail = DrawToDisplay_MusicThumbnail(helper, _ConfigDefault)
    
    KODI_WEBSERVER = KODI_WEBSERVER(helper, _ConfigDefault, draw_default)
    main()
