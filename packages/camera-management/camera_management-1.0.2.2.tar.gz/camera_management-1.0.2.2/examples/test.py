# ensure a running CameraApplication
import cv2
from camera_management.frontends.basic_frontend import basic_Interface, manager_interface

interface = manager_interface(host='10.40.20.240', port=8090)
print(interface.get_configured_cams())

cam_if = interface.get_interface_by_port(8093)

while True:
    data = cam_if.fetch_image_data()
    cv2.imshow("Stream", data.image)
    if cv2.waitKey(20) == ord("q"):
        break
