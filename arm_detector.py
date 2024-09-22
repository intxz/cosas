import cv2
import mediapipe as mp
import math

# Initialize drawing utility and pose detection from Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


# Function to calculate the angle between three points (for elbow angle calculation)
def calculate_angle(a, b, c):
    # Extract coordinates
    a = [a.x, a.y]
    b = [b.x, b.y]
    c = [c.x, c.y]

    # Vector between points a and b, and between b and c
    ba = [a[0] - b[0], a[1] - b[1]]
    bc = [c[0] - b[0], c[1] - b[1]]

    # Calculate the cosine of the angle using the dot product and magnitudes of the vectors
    cosine_angle = (ba[0] * bc[0] + ba[1] * bc[1]) / (
        math.sqrt(ba[0] ** 2 + ba[1] ** 2) * math.sqrt(bc[0] ** 2 + bc[1] ** 2) + 1e-6
    )

    # Convert the cosine value to an angle in degrees
    angle = math.degrees(math.acos(cosine_angle))

    return angle


# Initialize the video capture from the webcam
cap = cv2.VideoCapture(0)

# Use the Pose model from Mediapipe
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Cannot access the camera")
            break

        # Flip the image horizontally (mirror effect)
        frame = cv2.flip(frame, 1)

        # Convert the image to RGB for Mediapipe processing
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = (
            False  # Optimize processing by making the image non-writeable
        )

        # Process the image to detect poses
        results = pose.process(image)

        # Convert the image back to BGR for OpenCV display
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # If pose landmarks are detected
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get the coordinates of the shoulders to determine the body orientation
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

            # Determine the orientation of the body (left or right profile)
            if left_shoulder.y > right_shoulder.y:
                orientation = "Perfil Izquierdo"  # Left profile
                # Use the right arm landmarks (since it's visible in the left profile)
                shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                color = (0, 0, 255)  # Blue for the right arm
            elif right_shoulder.y > left_shoulder.y:
                orientation = "Perfil Derecho"  # Right profile
                # Use the left arm landmarks (since it's visible in the right profile)
                shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
                wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
                color = (0, 255, 0)  # Green for the left arm
            else:
                orientation = "Vista Frontal"  # Frontal view
                color = (255, 255, 255)  # White for frontal view
                shoulder = elbow = wrist = None  # No arm detection in frontal view

            # Display the detected body orientation
            cv2.putText(
                image,
                f"Orientation: {orientation}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2,
                cv2.LINE_AA,
            )

            # If the body is in profile, detect the arm and calculate the elbow angle
            if "Perfil" in orientation and shoulder and elbow and wrist:
                # Draw lines connecting the shoulder, elbow, and wrist
                cv2.line(
                    image,
                    (
                        int(shoulder.x * frame.shape[1]),
                        int(shoulder.y * frame.shape[0]),
                    ),
                    (int(elbow.x * frame.shape[1]), int(elbow.y * frame.shape[0])),
                    color,
                    3,
                )

                cv2.line(
                    image,
                    (int(elbow.x * frame.shape[1]), int(elbow.y * frame.shape[0])),
                    (int(wrist.x * frame.shape[1]), int(wrist.y * frame.shape[0])),
                    color,
                    3,
                )

                # Calculate the angle of the elbow
                angle = calculate_angle(shoulder, elbow, wrist)
                # Display the calculated elbow angle
                cv2.putText(
                    image,
                    f"Elbow Angle: {int(angle)}",
                    (
                        int(elbow.x * frame.shape[1]) - 50,
                        int(elbow.y * frame.shape[0]) - 20,
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2,
                    cv2.LINE_AA,
                )

            # Draw all pose landmarks with the color corresponding to the side of the body
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2),
            )

        # Display the image with the drawn landmarks and text
        cv2.imshow("Arm Detector", image)

        # Exit if 'q' is pressed
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
