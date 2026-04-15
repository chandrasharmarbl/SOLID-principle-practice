import pytest
from unittest.mock import MagicMock, call
from smart_device import Switchable, MusicPlayer, SmartLight, SmartSpeaker

class TestSmartLightISP:

    def test_light_only_needs_switchable(self, mocker):
        mock_light = mocker.MagicMock(spec=Switchable)

        mock_light.turn_on()

        mock_light.turn_on.assert_called_once()

    def test_light_does_not_expose_play_music(self, mocker):
        mock_light = mocker.MagicMock(spec=Switchable)

        assert not hasattr(mock_light, 'play_music') or \
               'play_music' not in dir(Switchable)

    def test_real_light_turn_on(self, capsys):
        light = SmartLight()
        light.turn_on()

        captured = capsys.readouterr()
        assert "Light on" in captured.out

    def test_real_light_has_no_play_music(self):
        light = SmartLight()

        assert not hasattr(light, 'play_music'), (
            "ISP violated: SmartLight should not implement MusicPlayer"
        )

    def test_light_turn_on_called_with_mock(self, mocker):
        mock_light = mocker.MagicMock(spec=Switchable)

        def controller(device: Switchable):
            device.turn_on()

        controller(mock_light)

        mock_light.turn_on.assert_called_once()

class TestSmartSpeakerISP:

    def test_speaker_satisfies_switchable(self, mocker):
        mock_speaker = mocker.MagicMock(spec=SmartSpeaker)

        mock_speaker.turn_on()

        mock_speaker.turn_on.assert_called_once()

    def test_speaker_satisfies_music_player(self, mocker):
        mock_speaker = mocker.MagicMock(spec=SmartSpeaker)

        mock_speaker.play_music()

        mock_speaker.play_music.assert_called_once()

    def test_speaker_switchable_and_music_are_independent(self, mocker):
        mock_speaker = mocker.MagicMock(spec=SmartSpeaker)

        mock_speaker.turn_on()

        mock_speaker.play_music.assert_not_called()

    def test_real_speaker_both_interfaces(self, capsys):
        speaker = SmartSpeaker()

        speaker.turn_on()
        speaker.play_music()

        captured = capsys.readouterr()
        assert "Speaker on" in captured.out
        assert "Playing music" in captured.out


class TestISPContractSeparation:

    def test_switchable_controller_works_for_both_devices(self, mocker):
        mock_light   = mocker.MagicMock(spec=Switchable)
        mock_speaker = mocker.MagicMock(spec=Switchable)

        def power_on_all(devices):
            for device in devices:
                device.turn_on()

        power_on_all([mock_light, mock_speaker])

        mock_light.turn_on.assert_called_once()
        mock_speaker.turn_on.assert_called_once()

    def test_music_controller_only_needs_music_player(self, mocker):
        mock_speaker = mocker.MagicMock(spec=MusicPlayer)

        def start_playlist(player: MusicPlayer):
            player.play_music()

        start_playlist(mock_speaker)

        mock_speaker.play_music.assert_called_once()
        assert not hasattr(mock_speaker, 'turn_on') or \
               mock_speaker.turn_on.call_count == 0

    def test_isp_violation_would_look_like_this(self, mocker):
       
        bad_mock_light = mocker.MagicMock(spec=MusicPlayer)

        assert hasattr(bad_mock_light, 'play_music')

        good_mock_light = mocker.MagicMock(spec=Switchable)
        assert not hasattr(good_mock_light, 'play_music') 


if __name__ == "__main__":
    pytest.main([__file__, "-v"])