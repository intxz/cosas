import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence = 0.3, min_tracking_confidence = 0.3) as hands:
    while cap.isOpened():
        ret, frame = cap.read()

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

        # Detect hands

        res = hands.process(img)  

        finger_count = 0

        # Draw landmarks

        if res.multi_hand_landmarks:
            for hand_landmarks in res.multi_hand_landmarks:

                mp_drawing.draw_landmarks( frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=3))
                
                if len(hand_landmarks.landmark) == 21:
                    # Define landmarks for finger tips and bases

                    thumb_tip = hand_landmarks.landmark[5]
                    thumb_base = hand_landmarks.landmark[4]

                    index_tip = hand_landmarks.landmark[8]
                    index_base = hand_landmarks.landmark[6]

                    middle_tip = hand_landmarks.landmark[12]
                    middle_base = hand_landmarks.landmark[10]

                    ring_tip = hand_landmarks.landmark[16]
                    ring_base = hand_landmarks.landmark[14]

                    pinky_tip = hand_landmarks.landmark[20]
                    pinky_base = hand_landmarks.landmark[18]

                    # Check if fingers are up

                    thumb_up = thumb_tip.y < thumb_base.y
                    index_up = index_tip.y < index_base.y
                    middle_up = middle_tip.y < middle_base.y
                    ring_up = ring_tip.y < ring_base.y
                    pinky_up = pinky_tip.y < pinky_base.y

                    # Count fingers that are up

                    finger_count = sum([thumb_up, index_up, middle_up, ring_up, pinky_up])

            
            if finger_count== 4:
                cv2.putText(frame, f"FINGERS: {finger_count}", (10, 30), cv2.FONT_HERSHEY_COMPLEX,1 , (0,255, 0), 2)   
            else:
                cv2.putText(frame, f"FINGERS: {finger_count}", (10, 30), cv2.FONT_HERSHEY_COMPLEX,1 , (255,255, 255), 2)   
        
        # Show the res

        cv2.imshow('HAND DETECTOR', frame)


        if cv2.waitKey(10) & 0xFF == ord('p'):
           break
           
cap.release()
cv2.destroyAllWindows()
