from flask import Flask, jsonify, Response
from flask_cors import CORS
import cv2
import numpy as np
import requests
import cv2 as cv;
import mediapipe as mp
import numpy as np;

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)
mp_drawing = mp.solutions.drawing_utils

# Dummy variable for counting arm curls - replace with your actual logic
counter_la = 0
counter_ra=0

squats_counter=0
OPENAI_API_KEY='openai api key'

@app.route('/exercises/<exercise_type>', methods=['GET'])
def get_exercises(exercise_type):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = { 
        'model': 'gpt-4',
        'messages': [
            {
              'role': "system",
              'content': f'Generate a fitness exercise plan for {exercise_type} You are a fitness trainer app i want the output as json data where input takes the type of fatloss or goal they want to reach after ceratin excersice the output data should cantain (joint_key :[max_angle,min_angle]) so joint_key is 0-left elbow from 1-33 nose, left_eye_inner, left_eye, left_eye_outer, right_eye_inner, right_eye, right_eye_outer, left_ear, right_ear, mouth_left, mouth_right, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_wrist, left_pinky, right_pinky, left_index, right_index, left_thumb, right_thumb, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle, left_heel, right_heel, left_foot_index, right_foot_index respectively and the max angle is the completing angle of the excersice and the min-angle is starting angle of the joint part while doing an excersice so the output json data should contain a particular excersice data and no content other than json should be written if description is needed then add the description into json with desciption as key but give everything in json only'
            }],
        'temperature': 0.5,
        'max_tokens': 1024,
        'top_p': 1.0, 
        'frequency_penalty': 0.0,
        'presence_penalty': 0.0
    }
    print('sending sending.....') 
    response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
    if response.status_code != 200:
        # Log the error message from OpenAI API
        print(f"OpenAI API Error: {response.text}")
        return jsonify({'error': 'Failed to fetch exercises from OpenAI.', 'details': response.text}), response.status_code
    else:
        print(response.json()['choices'][0]) 
    return jsonify(response.json()['choices'][0]) 

def calculate_angle2(left,middle,right):
    a=np.array(left)
    b=np.array(middle)
    c=np.array(right)
    
    radians=np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(radians*180.0/np.pi)
    if angle>180:
        angle=360-angle;
    return angle;

def calculate_angle(landmarks,type="l_arm"):
    left,middle,right=None,None,None;
    if type=="l_arm":
        left=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        middle=[landmarks[14].x,landmarks[14].y]
        right=[landmarks[16].x,landmarks[16].y]
        return calculate_angle2(left,middle,right)
    
    elif type=="r_arm":
        left=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        middle=[landmarks[13].x,landmarks[13].y]
        right=[landmarks[15].x,landmarks[15].y]
        return calculate_angle2(left,middle,right)
        
    elif type=="squat":
        left1=[landmarks[24].x,landmarks[24].y]
        middle1=[landmarks[26].x,landmarks[26].y]
        right1=[landmarks[28].x,landmarks[28].y]
        left2=[landmarks[23].x,landmarks[23].y]
        middle2=[landmarks[25].x,landmarks[25].y]
        right2=[landmarks[27].x,landmarks[27].y]
        left_side=calculate_angle2(left1,middle1,right1)
        right_side=calculate_angle2(left2,middle2,right2)
        
        return [left_side,right_side]
        
        
        
        

    a=np.array(left)
    b=np.array(middle)
    c=np.array(right)
    
    radians=np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(radians*180.0/np.pi)
    if angle>180:
        angle=360-angle;
    return angle;

def arm(stage,counter,angle):
    if angle>130:
        stage="UP"
    elif angle<60 and stage=="UP":
        stage="DOWN"
        counter+=1;
    return [counter,stage]

def squat(stage, counter, left_angle, right_angle):
    squat_down_threshold = 120  # Angle for considering as a squat down position
    squat_up_threshold = 150  # Angle for considering as standing up (relatively straight legs)
    
    # Check both knees' angles to ensure a proper squat
    if left_angle > squat_up_threshold and right_angle > squat_up_threshold:
        if stage == "DOWN":  # Only change stage to "UP" if previously "DOWN"
            stage = "UP"
    elif left_angle < squat_down_threshold and right_angle < squat_down_threshold and stage == "UP":
        stage = "DOWN"
        counter += 1  # Increment counter when returning to "UP" position

    return [counter, stage]

@app.route('/send_data')
def send_data():
    return jsonify({"arms":{"count_la":counter_ra,"count_ra":counter_la},"legs":squats_counter})

def generate_frames():
    global counter_la,counter_ra,squats_counter
    global stage_la,stage_ra,squat_stage
    cap = cv2.VideoCapture(0)
    stage_la=None;
    stage_ra=None;
    squat_stage=None;
    counter_la=0   
    counter_ra=0
    squats_counter=0;
    while cap.isOpened():  
        print('started')
        ret, frame = cap.read()
        # counter=0
        if not ret:
            break
        width,height,z=frame.shape;
        # Convert the image from BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        
        # Process the image and detect the pose
        results = pose.process(image)
        
        # for arm curler logic
        try:
            landmarks=results.pose_landmarks.landmark
            #* arm curler logic by taking shoulder,wrist
            
            # *left arm
            angle_la=calculate_angle(landmarks=landmarks,type="l_arm")
            #^ for arm angle displaying on elbow
            # ^cv.putText(image,str(angle),tuple(np.multiply(elbow,[width,height]).astype(int)),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)    
            
            arm_curler=arm(stage=stage_la,counter=counter_la,angle=angle_la)
            counter_la,stage_la=arm_curler[0],arm_curler[1]
            cv.putText(image, 'RIGHT', (15,12), 
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
            cv.putText(image, str(counter_la), 
                        (10,60), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (250,40,255), 2, cv.LINE_AA)
            
            # Stage data
            cv.putText(image, 'STAGE', (65,12), 
                        cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
            cv.putText(image, stage_la, 
                        (80,60), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (250,40,255), 2, cv.LINE_AA)
            
            # Right Arm
            angle_ra=calculate_angle(landmarks=landmarks,type="r_arm")
            arm_curler=arm(stage=stage_ra,counter=counter_ra,angle=angle_ra)
            counter_ra,stage_ra=arm_curler[0],arm_curler[1]
            cv.putText(image, 'LEFT', (15,90),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
            cv.putText(image, str(counter_ra), 
                        (10,133), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (250,40,255), 2, cv.LINE_AA)
            
            # Stage data
            cv.putText(image, 'STAGE', (65,90),
                        cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
            cv.putText(image, stage_ra, 
                        (80,130), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (250,40,255), 2, cv.LINE_AA)
            
            
            # Leg curler
            
            squat_angles=calculate_angle(landmarks,type="squat");
            squat_value=(squat(squat_stage,squats_counter,squat_angles[0],squat_angles[1]))
            squats_counter,squat_stage=squat_value[0],squat_value[1];
            
            cv.putText(image, 'SQUATS', (15,140),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
            cv.putText(image, str(squats_counter), 
                        (10,173), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (250,40,255), 2, cv.LINE_AA)
            
            # Stage data
            cv.putText(image, 'STAGE', (65,140),
                        cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
            cv.putText(image, squat_stage,  
                        (80,170), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, (250,40,255), 2, cv.LINE_AA)
            elbow=[landmarks[25].x,landmarks[25].y] 
            cv.putText(image,str(squat_angles[0]),tuple(np.multiply(elbow,[width,height]).astype(int)),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)    
            
            
        except:
        #   counter=0;
          print('eroor')
        
        # Draw the pose annotation on the image
        
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Logic for counting arm curls can go here
        # Increment counter for the sake of example
        

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', image)
        if not ret:
            continue
        
        # Convert to byte array and yield the frame in the multipart/x-mixed-replace content-type
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    else:
        print('no camera found') 
@app.route('/video_feed')
def video_feed():
    # print('sending')
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/arm_counter')
def arm_counter():
    return jsonify({'RIGHT HAND': counter_la,'LEFT HAND':counter_ra}) 

@app.route('/leg_counter')
def leg_counter():
    return jsonify({'squats':squats_counter})
if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask
# from flask_socketio import SocketIO
# import base64
# import cv2
# import numpy as np
# import mediapipe as mp

# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")

# mp_pose = mp.solutions.pose
# pose = mp_pose.Pose()

# def process_frame(img):
#     try:
#         img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = pose.process(img_rgb)
#         landmarks = []
#         if results.pose_landmarks:
#             for landmark in results.pose_landmarks.landmark:
#                 landmarks.append({
#                     'x': landmark.x,
#                     'y': landmark.y,
#                     'visibility': landmark.visibility if hasattr(landmark, 'visibility') else None,
#                 })
#         return landmarks
#     except Exception as e:
#         print(f"Error in process_frame: {e}")
#         return []

# @socketio.on('connect')
# def test_connect():
#     print('Client connected')

# @socketio.on('frame')
# def handle_frame(data):
#     print('Received frame')
#     img_data = base64.b64decode(data.split(',')[1])
#     img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
#     # Process the image with your logic here
#     print('Image processed')  # Update this with actual processing logic
#     # After processing, emit back the results
#     socketio.emit('pose_landmarks', {'landmarks': 'Your processed data here'})

# if __name__ == '__main__':
#     socketio.run(app, debug=True)
