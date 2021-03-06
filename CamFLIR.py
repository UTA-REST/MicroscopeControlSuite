

import matplotlib.pyplot as plt
import os
import PySpin
import sys
import numpy as np
import time


from camera import Camera


class CamFLIR(Camera):

    cam=None
    nodemap=None
    nodemap_tldevice=None

    def __acquire_images(self,N=1):

        ToReturn=[]
        #print('*** IMAGE ACQUISITION ***\n')
        try:
            result = True

            # Set acquisition mode to continuous
            #
            #  *** NOTES ***
            #  Because the example acquires and saves 10 images, setting acquisition
            #  mode to continuous lets the example finish. If set to single frame
            #  or multiframe (at a lower number of images), the example would just
            #  hang. This would happen because the example has been written to
            #  acquire 10 images while the camera would have been programmed to
            #  retrieve less than that.
            #
            #  Setting the value of an enumeration node is slightly more complicated
            #  than other node types. Two nodes must be retrieved: first, the
            #  enumeration node is retrieved from the nodemap; and second, the entry
            #  node is retrieved from the enumeration node. The integer value of the
            #  entry node is then set as the new value of the enumeration node.
            #
            #  Notice that both the enumeration and the entry nodes are checked for
            #  availability and readability/writability. Enumeration nodes are
            #  generally readable and writable whereas their entry nodes are only
            #  ever readable.
            #
            #  Retrieve enumeration node from nodemap

            # In order to access the node entries, they have to be casted to a pointer type (CEnumerationPtr here)
            node_acquisition_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('AcquisitionMode'))
            if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
                print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...')
                return False

            # Retrieve entry node from enumeration node
            #node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
            node_acquisition_mode_single = node_acquisition_mode.GetEntryByName('SingleFrame')

            if not PySpin.IsAvailable(node_acquisition_mode_single) or not PySpin.IsReadable(node_acquisition_mode_single):
                print('Unable to set acquisition mode to single (entry retrieval). Aborting...')
                return False

            # Retrieve integer value from entry node
            acquisition_mode_single = node_acquisition_mode_single.GetValue()

            # Set integer value from entry node as new value of enumeration node
            node_acquisition_mode.SetIntValue(acquisition_mode_single)

            #print('Acquisition mode set to single...')

            #  Begin
            #
            #  *** NOTES ***
            #  What happens when the camera begins acquiring images depends on the
            #  acquisition mode. Single frame captures only a single image, multi
            #  frame catures a set number of images, and continuous captures a
            #  continuous stream of images. Because the example calls for the
            #  retrieval of 10 images, continuous mode has been set.
            #
            #  *** LATER ***
            #  Image acquisition must be ended when no more images are needed.
            self.cam.BeginAcquisition()

            ##print('Acquiring images...')

            #  Retrieve device serial number for filename
            #
            #  *** NOTES ***
            #  The device serial number is retrieved in order to keep cameras from
            #  overwriting one another. Grabbing image IDs could also accomplish
            #  this.
            #device_serial_number = ''
            #node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
            #if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
            #    device_serial_number = node_device_serial_number.GetValue()
            #    print('Device serial number retrieved as %s...' % device_serial_number)

            # Retrieve, convert, and save images
            for i in range(N):
                try:

                    #  Retrieve next received image
                    #
                    #  *** NOTES ***
                    #  Capturing an image houses images on the camera buffer. Trying
                    #  to capture an image that does not exist will hang the camera.
                    #
                    #  *** LATER ***
                    #  Once an image from the buffer is saved and/or no longer
                    #  needed, the image must be released in order to keep the
                    #  buffer from filling up.
                    image_result = self.cam.GetNextImage(1000)

                    #  Ensure image completion
                    #
                    #  *** NOTES ***
                    #  Images can easily be checked for completion. This should be
                    #  done whenever a complete image is expected or required.
                    #  Further, check image status for a little more insight into
                    #  why an image is incomplete.
                    if image_result.IsIncomplete():
                        print('Image incomplete with image status %d ...' % image_result.GetImageStatus())

                    else:

                        #  Print image information; height and width recorded in pixels
                        #
                        #  *** NOTES ***
                        #  Images have quite a bit of available metadata including
                        #  things such as CRC, image status, and offset values, to
                        #  name a few.
                        width = image_result.GetWidth()
                        height = image_result.GetHeight()
                        print('Grabbed Image %d, width = %d, height = %d' % (i, width, height))

                        #  Convert image to mono 8
                        #
                        #  *** NOTES ***
                        #  Images can be converted between pixel formats by using
                        #  the appropriate enumeration value. Unlike the original
                        #  image, the converted one does not need to be released as
                        #  it does not affect the camera buffer.
                        #
                        #  When converting images, color processing algorithm is an
                        #  optional parameter.
                        image_converted = image_result.Convert(PySpin.PixelFormat_Mono8, PySpin.HQ_LINEAR)

                        r=image_converted.GetData().reshape(int(height),int(width))
                        ToReturn.append(r)

                        image_result.Release()

                except PySpin.SpinnakerException as ex:
                    print('Error: %s' % ex)
                    return False

            #  End acquisition
            #
            #  *** NOTES ***
            #  Ending acquisition appropriately helps ensure that devices clean up
            #  properly and do not need to be power-cycled to maintain integrity.
            self.cam.EndAcquisition()

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False

        return ToReturn





    def Snap(self, N):
        result = True
        try:

            # Initialize camera
            self.cam.Init()
            self.nodemap_tldevice = self.cam.GetTLDeviceNodeMap()
            #result &= print_device_info(nodemap_tldevice)

            # Retrieve GenICam nodemap
            self.nodemap = self.cam.GetNodeMap()
            exposure=PySpin.CFloatPtr(self.nodemap.GetNode("ExposureTime"))
            exposure.SetValue(self.exposure*1e6)
            # Acquire images
            ReturnVec= self.__acquire_images(N)
            time.sleep(self.exposure*2)
            # Deinitialize camera
            self.cam.DeInit()
        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False
        return ReturnVec


    def __del__(self):

        # The usage of del is preferred to assigning the variable to None.
        del self.cam

        # Clear camera list before releasing system
        self.cam_list.Clear()

        # Release system instance
        self.system.ReleaseInstance()


    def __init__(self, exposure=0.5):
        self.exposure=exposure


        # Retrieve singleton reference to system object
        self.system = PySpin.System.GetInstance()

        # Get current library version
        version = self.system.GetLibraryVersion()
        #print('Library version: %d.%d.%d.%d' % (version.major, version.minor, version.type, version.build))

        # Retrieve list of cameras from the system
        self.cam_list = self.system.GetCameras()

        num_cameras = self.cam_list.GetSize()

        # print('Number of cameras detected: %d' % num_cameras)

        # Finish if there are no cameras
        if num_cameras == 0:

            # Clear camera list before releasing system
            self.cam_list.Clear()

            # Release system instance
            self.system.ReleaseInstance()

            return False

        # Run example on each camera
        self.cam=self.cam_list[0]
