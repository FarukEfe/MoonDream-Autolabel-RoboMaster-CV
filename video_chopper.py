import cv2
import os


def chop_video(video_path: str, output_dir: str, step: int = 20):
    # Create destination directory if the specified doesn't exist
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    video_capture = cv2.VideoCapture(video_path)

    if not video_capture.isOpened():
        print("Error: Unable to open video.")
        exit()

    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in the video: {frame_count}")

    # Read and save frames
    frame_idx = 0
    saves = 0
    while True:
        # Get next frame
        ret, frame = video_capture.read()
        # If in-between steps, ignore
        if frame_idx % step != 0:
            frame_idx += 1
            continue
        # All frames are read
        if not ret: break
        # Save current frame as image
        frame_filename = os.path.join(output_dir, f"frame{frame_idx:05d}.jpg")
        cv2.imwrite(frame_filename, frame)
        # Increment index of frame
        frame_idx += 1
        saves += 1
    
    print(f"Saved {saves} frames in '{output_dir}'")

    video_capture.release()

chop_video('./videos/macu_vs_uofa.mp4', './frames')

