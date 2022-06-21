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
        self.camera = camera
        self.size = (1920, 1080)

    # Save timelapse
    def save(self):
        Log.logger().info('Saving video')

        out = cv2.VideoWriter('{path}/{datestamp}/{name}.mp4'.format(path=self.camera.images_folder, datestamp=self.camera.datestamp, name=self.camera.datestamp),cv2.VideoWriter_fourcc(*'mp4v'), 15, self.size)

        files = glob.glob('{path}/{datestamp}/*.png'.format(path=self.camera.images_folder, datestamp=self.camera.datestamp))
        files.sort()

        previous_frame: Frame = None
        bad_frames = 0
        for filename in files:
            timestamp = int(filename.split('/')[-1].split('.')[0])
            image = cv2.imread(filename)
            if image is None:
                continue

            current_frame = Frame(camera=self.camera, image=image, timestamp=timestamp)
            if previous_frame is None:
                previous_frame = current_frame

            (bad_frame, _) = self.is_bad_frame(current_frame=current_frame, previous_frame=previous_frame)
            if bad_frame and Config.get_setting('skip_bad_frames'):
                bad_frames += 1
                previous_frame = current_frame
                continue

            height, width, _ = image.shape
            self.size = (width, height)

            #self.frames.append(frame)
            out.write(current_frame.image)
            previous_frame = current_frame

        out.release()
        Log.logger().info('Saved video. Tossed {bad_frames} bad frames'.format(
            bad_frames=bad_frames
        ))
        del out

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
