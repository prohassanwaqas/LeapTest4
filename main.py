#coding=utf-8
import pandas

import numpy as np

################################################################
'%matplotlib inline'

# import numpy as np

# import pandas as pd

import Leap, ctypes, os, sys


# from leap_data_helper import *     ########un comment this when figured out what where this goes and to do with it

# import matplotlib.pyplot as plt
################################################################
class SampleListener(Leap.Listener):
    #
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    #
    def on_init(self, controller):
        print("Initialized")

    def on_connect(self,
                   controller):
        print("Motion Sensor Connected!")
        #
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        #
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        print
        "Connected"

        def on_disconnect(self, controller):
            print("Motion Sensor Disconnected!")

        def on_exit(self, controller):
            print("Exited")

    def on_frame(self, controller):

        global finger
        frame = controller.frame()

        for hand in frame.hands:
            for finger in hand.fingers:    '''print "Type: " + self.fingers_names[finger.type()]'''
            print
            " type: " + self.finger_names[finger.type] + "ID: " + str(finger.id) + "Length (mm): " + str(
                finger.length) + " width(mm)" + str(finger.width)

        for b in range(0, 4):
            bone = finger.bone(b)
            print
            "Bone: " + self.bone_names[bone.type] + "Start: " + str(bone.prev_joint) + "End: " + str(
                bone.next_joint) + "Direction: " + str(bone.direction)


''' for hand in frame.hands:
            handType ="Left Hand" if hand.is_left else "Right Hand"
            print handType + "Hand ID" + str(hand.id) + "Palm Position" + str(hand.palm_position)
            normal = hand.palm_normal
            direction = hand.direction
            print "pitch: " + str(direction.pitch * Leap.RAD_TO_DEG) + " Roll: " + str(normal.roll * Leap.RAD_TO_DEG) + " Yaw: " + str(direction.yaw * Leap.RAD_TO_DEG)
'''


def main():
    # Create listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Add listener event to controller
    controller.add_listener(listener)

    # Remove listener at the end
    print
    "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()

    '''   print "Frame ID: " + str(frame.id) \
                     + " Timestamps: " + str(frame.timestamp) \
                     + " # of Hands: " + str(len(frame.hands)) \
                     + " # of Fingers: " + str(len(frame.fingers)) \
                     + " # of Tools: " + str(len(frame.tools)) \
                     + " # of Gestures: " + str(len(frame.gestures())) '''


    ###################################################################################################################################
    def cal_2vec_angle(v1, v2):
        # return the value of cos(angle)
        return np.dot(v1, v2) / np.linalg.norm(v1) / np.linalg.norm(v2)


    def get_frame(filename):

        frame = Leap.Frame()
        # filename = 'cali_1495553181022000.data'
        with open(os.path.realpath(filename), 'rb') as data_file:
            data = data_file.read()

        leap_byte_array = Leap.byte_array(len(data))
        address = leap_byte_array.cast().__long__()
        ctypes.memmove(address, data, len(data))

        frame.deserialize((leap_byte_array, len(data)))

        return frame


    # Let's have a quick validation of the frame data
    def get_joints(frame):
        joints = []
        for hand in frame.hands:
            for finger in hand.fingers:
                for b in range(0, 4):
                    bone = finger.bone(b)
                    joint_pos = bone.next_joint.to_float_array()
                    joints.append(joint_pos)

        return np.array(joints)


    def get_angles(frame):

        angles = []
        # palm position
        J0 = np.array(frame.hands[0].palm_position.to_float_array())
        # thumb
        J1 = np.array(frame.hands[0].fingers[0].bone(1).next_joint.to_float_array())
        J2 = np.array(frame.hands[0].fingers[0].bone(2).next_joint.to_float_array())
        J3 = np.array(frame.hands[0].fingers[0].bone(3).next_joint.to_float_array())
        # index
        J4 = np.array(frame.hands[0].fingers[1].bone(0).next_joint.to_float_array())
        J5 = np.array(frame.hands[0].fingers[1].bone(1).next_joint.to_float_array())
        J6 = np.array(frame.hands[0].fingers[1].bone(2).next_joint.to_float_array())
        J7 = np.array(frame.hands[0].fingers[1].bone(3).next_joint.to_float_array())
        # middle
        J8 = np.array(frame.hands[0].fingers[2].bone(0).next_joint.to_float_array())
        J9 = np.array(frame.hands[0].fingers[2].bone(1).next_joint.to_float_array())
        J10 = np.array(frame.hands[0].fingers[2].bone(2).next_joint.to_float_array())
        J11 = np.array(frame.hands[0].fingers[2].bone(3).next_joint.to_float_array())
        # ring
        J12 = np.array(frame.hands[0].fingers[3].bone(0).next_joint.to_float_array())
        J13 = np.array(frame.hands[0].fingers[3].bone(1).next_joint.to_float_array())
        J14 = np.array(frame.hands[0].fingers[3].bone(2).next_joint.to_float_array())
        J15 = np.array(frame.hands[0].fingers[3].bone(3).next_joint.to_float_array())
        # pinky
        J16 = np.array(frame.hands[0].fingers[4].bone(0).next_joint.to_float_array())
        J17 = np.array(frame.hands[0].fingers[4].bone(1).next_joint.to_float_array())
        J18 = np.array(frame.hands[0].fingers[4].bone(2).next_joint.to_float_array())
        J19 = np.array(frame.hands[0].fingers[4].bone(3).next_joint.to_float_array())

        # A1-4
        A = cal_2vec_angle((J1 - J0), (J4 - J0))
        angles.append(A)
        A = cal_2vec_angle((J4 - J0), (J8 - J0))
        angles.append(A)
        A = cal_2vec_angle((J8 - J0), (J12 - J0))
        angles.append(A)
        A = cal_2vec_angle((J12 - J0), (J16 - J0))
        angles.append(A)

        # A5,6 on thumb
        A = cal_2vec_angle((J2 - J1), (J1 - J0))
        angles.append(A)
        A = cal_2vec_angle((J3 - J2), (J2 - J1))
        angles.append(A)

        # A7-9 on index
        A = cal_2vec_angle((J5 - J4), (J4 - J0))
        angles.append(A)
        A = cal_2vec_angle((J6 - J5), (J5 - J4))
        angles.append(A)
        A = cal_2vec_angle((J7 - J6), (J6 - J5))
        angles.append(A)

        # A10-12 on middle
        A = cal_2vec_angle((J9 - J8), (J8 - J0))
        angles.append(A)
        A = cal_2vec_angle((J10 - J9), (J9 - J8))
        angles.append(A)
        A = cal_2vec_angle((J11 - J10), (J10 - J9))
        angles.append(A)

        # A13-15 on ring
        A = cal_2vec_angle((J13 - J12), (J12 - J0))
        angles.append(A)
        A = cal_2vec_angle((J14 - J13), (J13 - J12))
        angles.append(A)
        A = cal_2vec_angle((J15 - J14), (J14 - J13))
        angles.append(A)

        # A16-18 on pinky
        A = cal_2vec_angle((J17 - J16), (J16 - J0))
        angles.append(A)
        A = cal_2vec_angle((J18 - J17), (J17 - J16))
        angles.append(A)
        A = cal_2vec_angle((J19 - J18), (J18 - J17))
        angles.append(A)

        # A19-22 between adjacent finger tips
        A = cal_2vec_angle((J3 - J2), (J7 - J6))
        angles.append(A)
        A = cal_2vec_angle((J7 - J6), (J11 - J10))
        angles.append(A)
        A = cal_2vec_angle((J11 - J10), (J15 - J14))
        angles.append(A)
        A = cal_2vec_angle((J15 - J14), (J19 - J18))
        angles.append(A)

        return np.array(angles)
