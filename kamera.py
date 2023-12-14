import time
import picamera
import requests
import schedule

def capture_and_send_image():
    try:
        # Start using the camera
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            # Wait for 2 seconds to let the camera become ready
            time.sleep(2)

            # Save the captured image
            image_path = '/home/pi/captured_image.jpg'
            camera.capture(image_path)
            print('Image captured and saved:', image_path)

            # Send the image via HTTP request
            upload_url = 'UPLOAD-SERVER-ADDRESS'
            files = {'image': open(image_path, 'rb')}
            response = requests.post(upload_url, files=files)

            # Check server response
            if response.status_code == 200:
                print('Image successfully sent to the server.')
            else:
                print('Error sending the image to the server. Status code:', response.status_code)

    except Exception as e:
        # Send error message
        error_message = f'Error capturing and sending the image: {str(e)}'
        print(error_message)
        # Display the error message to the user or save it to a file or perform any other desired operation

def send_sensor_data():
    # Data to send
    data_to_send = {
        'sensor_id': 1,
        'value': 25.5,
    }

    # Modem or server URL
    modem_url = 'MODEM-OR-SERVER-ADDRESS'

    # Send a POST request to the modem
    response = requests.post(modem_url, json=data_to_send)

    # Check the success of the send
    if response.status_code == 200:
        print('Data sent successfully.')
    else:
        print(f'Error sending data. Status code: {response.status_code}')

# Schedule to capture an image every three hours
schedule.every(3).hours.do(capture_and_send_image)

# Schedule to send sensor data every hour
schedule.every().hour.do(send_sensor_data)

if __name__ == "__main__":
    # Run the program
    while True:
        schedule.run_pending()
        time.sleep(1)
