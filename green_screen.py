import cv2

# open the video
video = cv2.VideoCapture('resources/video.mp4')

_, frame = video.read()
h,w = frame.shape[0:2]

background = cv2.imread('resources/bg.jpg')
background = cv2.resize(background,(w,h),None,None,None,cv2.INTER_LANCZOS4)

# Exit on error
if not video.isOpened():
    print('Error reading the video')
    exit()

while True:
    ok, frame = video.read()
    # Exit when there are not frames to read, or on error
    if not ok:
        print('End of video')
        exit()

    # split the the B, G and R channels
    b, g, r = cv2.split(frame)

    # Since the video is a green screen makes sense to use the green channel as the one to threshold for the mask
    _, th = cv2.threshold(g, 200, 255, cv2.THRESH_BINARY_INV)

    # make a new copy of the background resized image
    bg = background.copy()

    # if the pixel on threshold is background then make it white
    frame[th == 0]  = 255

    # if the pixel on threshold is not background then make it black
    bg[th !=0] = 255

    # combine both images into frame
    frame = cv2.bitwise_and(bg,frame)

    # show frames
    cv2.imshow('b',b)
    cv2.imshow('g',g)
    cv2.imshow('r',r)
    cv2.imshow('threshold',th)
    cv2.imshow('frame', frame)


    # Wait 30 miliseconds per frame to display the video with normal speed
    k = cv2.waitKey(30)

# Destroy all windows and release video capture instance
cv2.destroyAllWindows()
cv2.waitKey(1)
video.release()