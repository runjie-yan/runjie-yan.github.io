from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips, ImageClip
import moviepy.video.fx.all as vfx
import numpy as np

# Load the three videos
video1 = VideoFileClip("./assets/videos/variable/noisy.mp4") # 512 * 512
video2 = VideoFileClip("./assets/videos/variable/ground_truth.mp4") # 512 * 512
video3 = VideoFileClip("./assets/videos/variable/clean.mp4") # 512 * 512

# Create empty space between videos
space_height = 50  # Height of empty space
space_width = 50  # Width of empty space
final_video_duration = max(video1.duration, video2.duration, video3.duration) + 2.5

# Function to extract 10 frames from a video at equal intervals
def extract_frames(video, num_frames=6):
    duration = video.duration
    intervals = np.linspace(0, duration, num_frames + 1)[:-1]  # Create intervals excluding the first and last
    frames = [np.array(video.get_frame(t)) for t in intervals]
    frames = np.concatenate(frames, axis=1)
    return frames

# Extract 10 frames from each video
frames1 = extract_frames(video1)
frames2 = extract_frames(video2)
frames3 = extract_frames(video3)

# Convert frames to clips and concatenate them vertically
frame_clips1 = ImageClip(np.array(frames1)).set_duration(final_video_duration).set_position((0, space_height))
frame_clips2 = ImageClip(np.array(frames2)).set_duration(final_video_duration).set_position((0, video1.h + space_height*3))
frame_clips3 = ImageClip(np.array(frames3)).set_duration(final_video_duration).set_position((0, video1.h + video2.h + space_height*5))
video1 = video1.set_duration(final_video_duration).set_position((frame_clips1.w + space_width*2, space_height))
video2 = video2.set_duration(final_video_duration).set_position((frame_clips1.w + space_width*2, video1.h + space_height*3))
video3 = video3.set_duration(final_video_duration).set_position((frame_clips1.w + space_width*2, video1.h + video2.h + space_height*5))

# Get the final video size
final_video_width = frame_clips1.w + space_width*2 + video1.w
final_video_height = video1.h + video2.h + video2.h + space_height*6

# Create the combined video with the frame strip on the left
combined_video = CompositeVideoClip(
    [
        frame_clips1,
        frame_clips2,
        frame_clips3,
        video1,
        video2,
        video3,
    ], 
    size=(final_video_width, final_video_height),
    # bg_color=(245,245,245)
    bg_color=(255,255,255)
)

# Set the duration of the combined video to the longest individual video duration
combined_video = combined_video.set_duration(final_video_duration)

# Write the final video to a file
combined_video.write_videofile("./assets/videos/variable/variable.mp4", codec="libx264", fps=24)
