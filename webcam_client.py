#!/usr/bin/env python3

import cv2
import requests
import base64
import json
import time
import argparse
from datetime import datetime

# Default configuration
DEFAULT_SERVER_URL = 'http://raspberrypi.local:3000'  # Change to your Raspberry Pi's IP/hostname
DEFAULT_CAMERA_ID = 0
DEFAULT_FPS = 5
DEFAULT_QUALITY = 70  # JPEG compression quality (0-100)
DEFAULT_RESOLUTION = (640, 480)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Stream webcam to Raspberry Pi server')
    parser.add_argument('--server', default=DEFAULT_SERVER_URL, help='Server URL')
    parser.add_argument('--camera', type=int, default=DEFAULT_CAMERA_ID, help='Camera device ID')
    parser.add_argument('--fps', type=int, default=DEFAULT_FPS, help='Frames per second')
    parser.add_argument('--quality', type=int, default=DEFAULT_QUALITY, help='JPEG quality (0-100)')
    parser.add_argument('--width', type=int, default=DEFAULT_RESOLUTION[0], help='Frame width')
    parser.add_argument('--height', type=int, default=DEFAULT_RESOLUTION[1], help='Frame height')
    return parser.parse_args()


def stream_webcam(server_url, camera_id, fps, quality, resolution):
    # Initialize webcam
    cap = cv2.VideoCapture(camera_id)

    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print(f"Streaming webcam to {server_url}/api/camera/upload")
    print(f"Resolution: {resolution[0]}x{resolution[1]}, FPS: {fps}, Quality: {quality}")

    # Calculate delay between frames
    delay = 1.0 / fps

    try:
        while True:
            start_time = time.time()

            # Capture frame
            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Convert frame to JPEG
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            _, jpeg_frame = cv2.imencode('.jpg', frame, encode_param)

            # Encode JPEG as base64
            base64_frame = base64.b64encode(jpeg_frame).decode('utf-8')

            # Prepare payload
            payload = {
                'image': base64_frame,
                'timestamp': datetime.now().isoformat(),
                'device_id': 'computer_webcam'
            }

            # Send to server
            try:
                response = requests.post(
                    f"{server_url}/api/camera/upload",
                    json=payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=1
                )

                if response.status_code == 200:
                    print(".", end='', flush=True)
                else:
                    print(f"\nError: Server returned status code {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"\nConnection error: {e}")

            # Sleep to maintain desired FPS
            elapsed = time.time() - start_time
            sleep_time = max(0, delay - elapsed)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nStreaming stopped by user.")
    finally:
        # Release resources
        cap.release()
        print("\nResources released.")


if __name__ == "__main__":
    args = parse_arguments()

    resolution = (args.width, args.height)

    stream_webcam(
        server_url=args.server,
        camera_id=args.camera,
        fps=args.fps,
        quality=args.quality,
        resolution=resolution
    )
