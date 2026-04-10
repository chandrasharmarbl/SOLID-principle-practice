class SmartDevice:
    def turn_on(self): pass
    def play_music(self): pass


class SmartLight(SmartDevice):
    def turn_on(self):
        print("Light on")

    def play_music(self):
        raise Exception("Not supported")


if __name__ == '__main__':
    light = SmartLight()
    light.turn_on()
    
    try:
        light.play_music()
    except Exception as e:
        print(f"Error: {e}")