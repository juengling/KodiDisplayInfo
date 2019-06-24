from datetime import timedelta
from PIL import Image
from io import BytesIO


class DrawToDisplay_Default:

    default_info_text = ""
    default_info_color = ""
    
    def __init__(self, helper, _ConfigDefault):
        self.helper = helper
        self._ConfigDefault = _ConfigDefault

    def setVars(self):
        self._drawSetting = {}
        self._drawSetting['startscreen.logo'] = self._ConfigDefault['basedirpath'] + 'img/kodi_logo.png'

        self._drawSetting['startscreen.logo.size.prozent'] = 60
        self._drawSetting['startscreen.logo.size.pixel'] = \
            self.helper.PercentToPixel(self._drawSetting['startscreen.logo.size.prozent'])

        # Anpassen der Größe des Logos
        self.logo = Image.open(self._drawSetting['startscreen.logo'])
        self.logo = self.logo.resize([self._drawSetting['startscreen.logo.size.pixel'],
                                      self._drawSetting['startscreen.logo.size.pixel']], Image.ANTIALIAS)
        self.logo = self.pygame.image.fromstring(self.logo.tobytes(), self.logo.size, self.logo.mode)


        # Position der Uhrzeit
        # Die Uhrzeit soll mittig zwischen unterem Logorand und unterem Bildrand angezeigt werden
        # Berechnen des zu verfügung stehenden Platzes

        free_space_time = ( self.screen.get_height() - self._drawSetting['startscreen.logo.size.pixel']) / 2
        # Schriftgröße der Uhr ist 75% des zur verfügung stehenden Platzes
        self._drawSetting['startscreen.clock.fontsize'] = round(free_space_time * 0.75)
        # Position der Uhrzeit
        self._drawSetting['startscreen.clock.y'] = round(self.screen.get_height() - free_space_time / 2)

        # Position und Größe des Infotextes
        # Der Infotext wird mittig zwischen oberen Rand und oberen Logorand angezeit
        # Schriftgröße des Infotextes ist 60% der zur verfügung stehenden Höhe
        self._drawSetting['startscreen.info.fontsize'] = round(free_space_time * 0.6)
        # Position des Infotextes
        self._drawSetting['startscreen.info.y'] = round(free_space_time / 2)

    def setPygameScreen(self, pygame, screen):
        self.pygame = pygame
        self.screen = screen

        # DIe Konfiguration für die Anzeige initialisieren
        self.setVars()


    def setInfoText(self, text, color):
        self.default_info_text = text
        self.default_info_color = color
    
    def infoTextKODI(self, text, color):
        self.displaytext(text, self._drawSetting['startscreen.info.fontsize'], (self.screen.get_width()/2),
                         self._drawSetting['startscreen.info.y'], 'none', "false", color)
    
    def displaytext(self, text, size, x, y, floating, bold, color):
        # font = self.pygame.font.SysFont("monospace", size, bold=bold)
        font = self.pygame.font.Font(self._ConfigDefault['basedirpath'] + "fonts/MC360.ttf", size)
        if bold == "true":
            font.set_bold(1)

        text = font.render(text, 1, color, (200, 200, 200))
        if floating == 'right':
            x = x - text.get_rect().width
            y = y - text.get_rect().height
        elif floating == 'left':
            x = x
            y = y - text.get_rect().height
        else:
            x = x - (text.get_rect().width/2)
            y = y - (text.get_rect().height/2)

        self.screen.blit(text, [x, y])
    
    def drawLogoStartScreen(self, time_now):
        if self.default_info_text != '':
            self.infoTextKODI(self.default_info_text, self.default_info_color)
        else:
            self.infoTextKODI("KodiDisplayInfo", self._ConfigDefault['color.white'])
        
        x = (self.screen.get_width()/2) - (self._drawSetting['startscreen.logo.size.pixel']/2)
        y = (self.screen.get_height()/2) - (self._drawSetting['startscreen.logo.size.pixel']/2)
        self.screen.blit(self.logo,(x,y-10))

        self.displaytext(time_now.strftime("%H:%M:%S"), self._drawSetting['startscreen.clock.fontsize'],
                         self.screen.get_width()/2,
                         self._drawSetting['startscreen.clock.y'],'none', "true", self._ConfigDefault['color.white'])