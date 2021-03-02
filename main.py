#coding=utf-8
import pandas as pd
import xlsxwriter
import sys
import openpyxl
from openpyxl.styles.builtins import output

import Leap


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
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        #
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        print "Connected"

        def on_disconnect(self, controller):
            print("Motion Sensor Disconnected!")

        def on_exit(self, controller):
            print("Exited")


    def on_frame(self, controller):
        frame = controller.frame()
       #
        """print "Frame ID: " + str(frame.id) \
                     + " Timestamps: " + str(frame.timestamp) \
                     + " # of Hands: " + str(len(frame.hands)) \
                     + " # of Fingers: " + str(len(frame.fingers)) \
                     + " # of Tools: " + str(len(frame.tools)) \
                     + " # of Gestures: " + str(len(frame.gestures()))"""
        #

        for hand in frame.hands:
            handType ="Left Hand" if hand.is_left else "Right Hand"
            print handType + "Hand ID" + str(hand.id) + "Palm Position" + str(hand.palm_position)
            normal = hand.palm_normal
            direction = hand.direction
            print "pitch: " + str(direction.pitch * Leap.RAD_TO_DEG) + " Roll: " + str(normal.roll * Leap.RAD_TO_DEG) + " Yaw: " + str(direction.yaw * Leap.RAD_TO_DEG)

       # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" \
         #     % ( frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))



def main():

    # Create listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Add listener event to controller
    controller.add_listener(listener)

    # Remove listener at the end
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()


