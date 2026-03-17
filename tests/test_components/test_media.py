from py_a2ui import AudioPlayer, Icon, IconName, Image, ImageFit, Video


def test_image_defaults():
    img = Image(id="photo", url="https://example.com/img.png")
    data = img.model_dump(by_alias=True, exclude_none=True)
    assert data["fit"] == "fill"
    assert data["variant"] == "mediumFeature"


def test_image_cover():
    img = Image(id="bg", url="https://example.com/bg.jpg", fit=ImageFit.COVER)
    assert img.fit == ImageFit.COVER


def test_icon_builtin():
    icon = Icon(id="i1", name=IconName.SEARCH)
    data = icon.model_dump(by_alias=True, exclude_none=True)
    assert data["name"] == "search"


def test_video():
    v = Video(id="v1", url="https://example.com/video.mp4")
    data = v.model_dump(by_alias=True, exclude_none=True)
    assert data["url"] == "https://example.com/video.mp4"


def test_audio_player():
    ap = AudioPlayer(id="ap1", url="https://example.com/audio.mp3", description="Song")
    data = ap.model_dump(by_alias=True, exclude_none=True)
    assert data["description"] == "Song"
