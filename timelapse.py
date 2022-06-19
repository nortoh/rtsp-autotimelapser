from camera import Camera
from config import Config
from frame import Frame
from log import Log
import glob
import cv2
import os

class Timelapse(object):

    SIMILARITY_MAX = 0.465

    def __init__(self, camera: Camera):
        self.frames = []
        self.camera = camera
        self.size = None

    # Load frames
    def load_frames(self):
        files = glob.glob('{path}/{datestamp}/*.png'.format(path=self.camera.images_folder, datestamp=self.camera.datestamp))
        files.sort()

        for filename in files:
            timestamp = int(filename.split('/')[-1].split('.')[0])
            image = cv2.imread(filename)
            if image is None:
                continue
            frame = Frame(camera=self.camera, image=image, timestamp=timestamp)
            height, width, _ = image.shape
            self.size = (width, height)
            self.frames.append(frame)

    # Save timelapse
    def save(self):
        if (len(self.frames) == 0):
            raise Exception('No frames found for timelapse obj')

        Log.logger().info('Saving video')
        out = cv2.VideoWriter('{path}/{name}.mp4'.format(path=self.camera.camera_folder, name=self.camera.datestamp),cv2.VideoWriter_fourcc(*'mp4v'), 15, self.size)

        previous_frame: Frame = self.frames[0]
        bad_frames = 0
        for i in range(len(self.frames)):
            current_frame: Frame = self.frames[i]
            (bad_frame, _) = self.is_bad_frame(current_frame=current_frame, previous_frame=previous_frame)

            if bad_frame:
                bad_frames += 1
                previous_frame = current_frame
                continue

            out.write(current_frame.image)
            previous_frame = current_frame

        out.release()
        Log.logger().info('Saved video. Tossed {bad_frames} bad frames'.format(
            bad_frames=bad_frames
        ))

    # Does this frame make me look bad?
    def is_bad_frame(self, current_frame: Frame, previous_frame: Frame):
        frame_matrix_a: cv2.Mat = None
        frame_matrix_b: cv2.Mat = None

        frame_matrix_a = cv2.cvtColor(src=current_frame.image, code=cv2.COLOR_BGR2GRAY)
        frame_matrix_b = cv2.cvtColor(src=previous_frame.image, code=cv2.COLOR_BGR2GRAY)

        kernal_size = (2, 2)
        frame_matrix_a = cv2.blur(frame_matrix_a, kernal_size)
        frame_matrix_b = cv2.blur(frame_matrix_b, kernal_size)
        frame_matrix_diff: cv2.Mat = cv2.subtract(src1=frame_matrix_b, src2=frame_matrix_a)

        height, width, _ = current_frame.image.shape
        similarity = cv2.countNonZero(src=frame_matrix_diff) / (width * height)

        #Log.logger().info('frame: {frame} - {similarity}'.format(frame=current_frame.timestamp, similarity=similarity))

        return (similarity > Timelapse.SIMILARITY_MAX, similarity)
