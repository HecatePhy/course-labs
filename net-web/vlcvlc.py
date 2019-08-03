import vlc
import cv2
import ctypes

VIDEO_WIDTH = 1024
VIDEO_HEIGHT = 578
videobuf = []
def lock(data, p_pixels):
    p_pixels = videobuf

def display(data, id):
    img = cv2.CreateImage((VIDEO_WIDTH, VIDEO_HEIGHT), IPL_DEPTH_8U, 4)
    img.imageData = videobuf
    cv2.ShowImage(vlc.libvlc_get_version(), img)
    cv2.WaitKey(10)
    cv2.ReleaseImage(img)

def unlock(data, id, p_pixels):
    assert id == None


if __name__ == '__main__':
    vlc_args = ["-I","dummy","--ignore-config"]
    arguments = [bytes(a,"utf-8") for a in vlc_args]
    #videobuf = (char*)malloc((VIDEO_WIDTH * VIDEO_HEIGHT) << 2);
    #memset(videobuf, 0, (VIDEO_WIDTH * VIDEO_HEIGHT) << 2);
    
    instance = vlc.libvlc_new(len(arguments),(ctypes.c_char_p * len(arguments))(*arguments))
    
    media = vlc.libvlc_media_new_location(instance, "rtsp://192.168.200.20:8554/test")
    mediaPlayer = vlc.libvlc_media_player_new_from_media(media)
    vlc.libvlc_media_release(media)
    
     #libvlc_media_player_set_media(mediaPlayer, media)
    vlc.libvlc_video_set_callbacks(mediaPlayer, lock, unlock, display, None)
    vlc.libvlc_video_set_format(mediaPlayer, "RV32", VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_WIDTH<<2)
    vlc.libvlc_media_player_play(mediaPlayer)

