import cv2, os, sys

def chop_video(video_path: str, output_dir: str, step: int = 20):

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

if __name__ == '__main__':
    # Handle CL Argv Errors
    if len(sys.argv) != 3:
        print("Usage: python tools.chopper <file_src_dir> <folder_dest_dir> ...")
        sys.exit(1)
    # Receive CL Arguments
    _ = sys.argv[0] # The script call (not used)
    src_path = sys.argv[1] # src file directory
    dest_path = sys.argv[2] # dest folder directory
    # Debug 
    #src_path = './videos/macu_vs_uofa.mp4'
    #dest_path = './frames/macu_vs_uofa'
    # Handle Argument Path
    absolute_src_path = os.path.abspath(src_path)
    absolute_dest_path = os.path.abspath(dest_path)
    if not os.path.exists(absolute_src_path):
        print("Source file not found in directory")
        sys.exit(1)
    if not os.path.exists(absolute_dest_path):
        print("Destination directory not found, making a new one...")
        # Create destination directory if the specified doesn't exist
        os.makedirs(absolute_dest_path)
    # Chop video and save
    chop_video(absolute_src_path, absolute_dest_path)
    
