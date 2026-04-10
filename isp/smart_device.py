class Switchable:
    def turn_on(self):
        pass


class MusicPlayer:
    def play_music(self):
        pass


class SmartLight(Switchable):
    def turn_on(self):
        print("Light on")


class SmartSpeaker(Switchable, MusicPlayer):
    def turn_on(self):
        print("Speaker on")

    def play_music(self):
        print("Playing music")


if __name__ == '__main__':
    light = SmartLight()
    light.turn_on()

    speaker = SmartSpeaker()
    speaker.turn_on()
    speaker.play_music()