from datetime import timedelta
from PIL import Image
from io import BytesIO


class DrawToDisplay_MusicThumbnail:

    # default for 320x240
    _drawSetting = {}
    _drawSetting['musicinfo.artist.fontsize'] = 30
    _drawSetting['musicinfo.album.fontsize'] = 15
    _drawSetting['musicinfo.song.fontsize'] = 20

    # settings for the thumbnail
    _drawSetting['musicinfo.thumbnail.size'] = 150, 150

    # in seconds
    time = 0
    totaltime = 0
    old_thumbnail = ''

    def __init__(self, helper, _ConfigDefault):
        self.helper = helper
        self._ConfigDefault = _ConfigDefault

    def setPygameScreen(self, pygame, screen, draw_default):
        self.pygame = pygame
        self.screen = screen
        self.draw_default = draw_default

        getattr(self, 'SetupDrawSetting'+self._ConfigDefault['display.resolution'])()

    def SetupDrawSetting320x240(self):
        self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_320x240.png')

    def SetupDrawSetting480x272(self):
        self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_480x272.png')

        self._drawSetting['musicinfo.artist.fontsize'] = 30
        self._drawSetting['musicinfo.album.fontsize'] = 20
        self._drawSetting['musicinfo.song.fontsize'] = 20
        self._drawSetting['musicinfo.thumbnail.size'] = 150, 150

    def SetupDrawSetting480x320(self):
        self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_480x320.png')

        self._drawSetting['musicinfo.artist.fontsize'] = 40
        self._drawSetting['musicinfo.album.fontsize'] = 15
        self._drawSetting['musicinfo.song.fontsize'] = 25
        self._drawSetting['musicinfo.thumbnail.size'] = 200, 200

    def displaytext(self, text, size, x, y, floating, color):
        #font = self.pygame.font.Font(self._ConfigDefault['basedirpath']+"fonts/MC360.ttf", size
        font = self.pygame.font.SysFont("Arial", size, bold=True)
        text = font.render(text, 1, color)
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

    # Diese Funktion zeichnet das Coverart auf das Display.
    # Wird kein Cover für das Album gefunden, wird ein Platzhalter angezeigt.
    def DrawThumbnail(self, thumbnail):
        # Thumbnail nur anpassen wenn es auch ein neues ist
        if not self.old_thumbnail == thumbnail:
            self.old_thumbnail = thumbnail
            # Wenn ein Thumbnail gefunden wurde, wird es verwendet
            if not thumbnail == "#empty":
                try:
                    self.thumbnail = Image.open(BytesIO(thumbnail))
                except ValueError:
                    self.helper.printout("[warning]    ", self._ConfigDefault['mesg.yellow'])
                    print('ValueError - DrawThumbnail')
                    # Sollte bei der Veraebeitung des gefundenen Covers was schief gehen, nutzen wie das
                    # DefaultAlbumCover
                    self.thumbnail = Image.open(self._ConfigDefault['basedirpath'] + 'img/DefaultAlbumCover.png')
            else:
                self.thumbnail = Image.open(self._ConfigDefault['basedirpath']+'img/DefaultAlbumCover.png')

            # Die Größe des Bildes anpassen
            self.thumbnail = self.thumbnail.resize(self._drawSetting['musicinfo.thumbnail.size'], Image.ANTIALIAS)
            # Das Bild an pygame senden
            self.thumbnail = self.pygame.image.fromstring(self.thumbnail.tobytes(), self.thumbnail.size,
                                                          self.thumbnail.mode)

        # Das Cover mittig im Dispaly positionieren
        x = (self.screen.get_width()/2) - ((self._drawSetting['musicinfo.thumbnail.size'][0])/2)
        y = (self.screen.get_height()/2) - ((self._drawSetting['musicinfo.thumbnail.size'][1])/2)

        # Nun das ganze aufs Display bringen
        self.screen.blit(self.thumbnail, (x, y))

    def DrawMusicInfo(self, thumbnail, artist, album, title):
        # Das Thumbnail im Dispaly platzieren
        self.DrawThumbnail(thumbnail)

        # Künstlername anzeigen
        # Der Künstelername wird mittig in der Breite und in der Höge genau zwischen oberen Displayrand
        # und oberen Coverrand angezeigt
        self.displaytext(artist, self._drawSetting['musicinfo.artist.fontsize'], (self.screen.get_width()/2),
                         ((self.screen.get_height() - (self._drawSetting['musicinfo.thumbnail.size'][1])) / 2)/2,
                         'none', self._ConfigDefault['color.white'])

        # Albumtitel anzeigen
        # Der Albumtitel wird mittig in der Breite und genau an der unteren Kante des Covers angezeigt
        self.displaytext(album, self._drawSetting['musicinfo.album.fontsize'], (self.screen.get_width()/2),
                         self.screen.get_height() -
                         ((self.screen.get_height() - (self._drawSetting['musicinfo.thumbnail.size'][1])) / 2)
                         + self._drawSetting['musicinfo.album.fontsize']/2 + 5, 'none', self._ConfigDefault['color.white'])

        #Songtitel anzeigen
        # Der Songtitel wird bündig an der unteren Kante des Displays angezeigt
        self.displaytext(title, self._drawSetting['musicinfo.song.fontsize'], (self.screen.get_width()/2),
                         self.screen.get_height() - self._drawSetting['musicinfo.song.fontsize']/2 - 5,
                         'none', self._ConfigDefault['color.white'])
