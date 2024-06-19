import cv2
import os
import numpy as np
import imageio
# Function to process a single frame
def process_frame(frame):
    # Example: Convert the frame to grayscale
    frame_rgb = frame[:,:512]
    frame_noise = frame[:,512*3:512*4]
    processed_frame = np.concatenate((frame_rgb, frame_noise), axis=1)
    return processed_frame


# Function to read video, process frames, and write the output video
def edit_video(input_video_path, output_video_path):
    # Read the input video
    reader = imageio.get_reader(input_video_path, 'ffmpeg')
    fps = reader.get_meta_data()['fps']

    # List to store processed frames
    processed_frames = []

    for frame in reader:
        # Process the frame
        processed_frame = process_frame(frame)

        # Append the processed frame to the list
        processed_frames.append(processed_frame)

    # Close the reader
    reader.close()

    # Save the processed frames as a new video
    imageio.mimsave(output_video_path, processed_frames, fps=fps)
    
# Example usage
for i in range(4):
    input_video_path = f'./assets/videos/noise_map/{i}.mp4'
    output_video_path = input_video_path[:-4]+'_noise.mp4'
    edit_video(input_video_path, output_video_path)
