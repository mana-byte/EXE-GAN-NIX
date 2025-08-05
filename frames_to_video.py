import cv2
import os


def frames_to_video(frames, output_path, fps=30):
    if not frames:
        raise ValueError("The list of frames is empty.")

    height, width, layers = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        video_writer.write(frame)

    video_writer.release()
    print(f"Video saved to {output_path}")


def read_frames_in_current_folder():
    frames = []
    for filename in sorted(os.listdir(".")):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            frame = cv2.imread(filename)
            if frame is not None:
                frames.append(frame)
    return frames


if __name__ == "__main__":
    output_video_path = "output_video.mp4"
    frames = read_frames_in_current_folder()
    if frames:
        frames_to_video(frames, output_video_path, fps=30)
    else:
        print("No frames found in the current folder.")
