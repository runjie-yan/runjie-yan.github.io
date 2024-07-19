import cv2
import os
import numpy as np
import imageio
from PIL import Image
# Function to process a single frame
def process_frame(frame):
    # Example: Convert the frame to grayscale
    frame_rgb = frame[:,:1024]
    frame_noise = frame[:,1024:1024*2]
    processed_frame = np.concatenate((frame_rgb, frame_noise), axis=1)
    return processed_frame

def process_frame_composite(frame):
    # Example: Convert the frame to grayscale
    frame_rgb = frame[:,:1024]
    frame_noise = frame[:,1024:1024*2]
    
    # Convert frame_noise to a Pillow Image
    noise_img = Image.fromarray(frame_noise)

    # Resize noise frame to 0.25 of its original size
    new_size = (noise_img.width // 4, noise_img.height // 4)
    resized_noise_img = noise_img.resize(new_size, Image.ANTIALIAS)

    # Convert the resized noise image back to a NumPy array
    resized_frame_noise = np.array(resized_noise_img)
        
    # put noise frame on right bottom
    frame_rgb[:resized_frame_noise.shape[0], -resized_frame_noise.shape[1]:] = resized_frame_noise
    return frame_rgb


# Function to read video, process frames, and write the output video
def edit_video(input_video_path, output_video_path):
    # Read the input video
    reader = imageio.get_reader(input_video_path, 'ffmpeg')
    fps = reader.get_meta_data()['fps']

    # List to store processed frames
    processed_frames = []

    for frame in reader:
        # Process the frame
        processed_frame = process_frame_composite(frame)

        # Append the processed frame to the list
        processed_frames.append(processed_frame)

    # Close the reader
    reader.close()

    # Save the processed frames as a new video
    imageio.mimsave(output_video_path, processed_frames, fps=fps)

def composite_edit_video(input_video_path, input_video_path_noise, output_video_path):
    # Read the input video
    rgb_reader = imageio.get_reader(input_video_path, 'ffmpeg')
    noise_reader = imageio.get_reader(input_video_path_noise, 'ffmpeg')
    fps = rgb_reader.get_meta_data()['fps']

    # List to store processed frames
    processed_frames = []

    for i in range(5):
        f = 0
        for rgb, noise in zip(rgb_reader, noise_reader):
            rgb, noise = rgb[:,:1024], noise[:,1024:2048]
            percentage = f/120
            f += 1
            if i < 2:
                processed_frames.append(rgb)
            elif i==2:
                processed_frames.append(cv2.addWeighted(rgb, 1 - percentage, noise, percentage, 0))
            elif i==3:
                processed_frames.append(noise)
            elif i==4:
                processed_frames.append(cv2.addWeighted(noise, 1 - percentage, rgb, percentage, 0))
        
        
    # close the reader
    rgb_reader.close()
    noise_reader.close()
    
    # Save the processed frames as a new video
    imageio.mimsave(output_video_path, processed_frames, fps=fps)
        
    
# Example usage
input_teaser = './assets/videos/teaser'
output_teaser = './assets/videos/head_teasern'
os.makedirs(output_teaser, exist_ok=True)
for video_name in sorted(os.listdir(input_teaser)):
    if video_name.endswith('noise.mp4'):
        continue
    else:
        video_name_noise = video_name.replace('.mp4', '_noise.mp4')
        input_video_path = os.path.join(input_teaser, video_name)
        input_video_path_noise = os.path.join(input_teaser, video_name_noise)
        output_video_path = os.path.join(output_teaser, video_name)
        composite_edit_video(input_video_path, input_video_path_noise, output_video_path)
        if os.path.exists(output_video_path):
            continue
