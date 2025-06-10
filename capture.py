import cv2
import time
import os

def snip(name):
    # Check if directory exists and if not, create it
    dir_path=os.path.abspath(__file__)
    dir_path=os.path.dirname(dir_path)
    dir_path=os.path.join(dir_path,"Face_detect/Faces/"+name).replace("\\","/")
    #dir_path = 'C:/leo/Encryption Using Face/Face_detect/Faces/{}'.format(name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if not cap.isOpened(): 
        print("Unable to read camera feed")
        return

    frame_id = 0
    start_time = time.time()  # Start time for capturing
    try:
        while True:
            ret, frame = cap.read()
            if ret:
                # Save frame as JPG file every 2 seconds
                if time.time() - start_time >= 2:
                    cv2.imwrite('{}/frame_{:d}.jpg'.format(dir_path, frame_id), frame)
                    frame_id += 1
                    start_time = time.time()  # Reset the start time
            else:
                break
            # Display the resulting frame    
            cv2.imshow('frame', frame)
            # Introduce delay for GUI window to update
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' key to break
                break
            # Stop recording after 5 frames (10 seconds)
            if frame_id == 5:
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # When everything done, release the video capture and video write objects
        cap.release()

        # Closes all the frames
        cv2.destroyAllWindows() 
