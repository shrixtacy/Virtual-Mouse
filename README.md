# Virtual Mouse Hand Tracking

This project allows you to control your computer mouse using hand gestures detected via your webcam. It leverages computer vision techniques to track your hand and map its movements to mouse actions, providing a touchless way to interact with your computer.

## Features

- Real-time hand tracking using your webcam
- Move the mouse cursor with your hand
- Perform mouse clicks with specific gestures
- No additional hardware required

## Requirements

- Python 3.x
- Webcam
- The dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/shrixtacy/Virtual-Mouse.git
   cd Virtual-Mouse
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Connect your webcam.**
2. **Run the main script:**
   ```sh
   python virtual_mouse.py
   ```
3. **Follow the on-screen instructions to control your mouse with hand gestures.**

## How it Works

The script uses computer vision libraries to detect and track your hand in real-time. It maps the position of your index finger to the mouse cursor and recognizes gestures (like pinching) to perform mouse clicks.

## Troubleshooting

- Ensure your webcam is connected and accessible.
- If you encounter missing package errors, double-check that all dependencies are installed.
- For best results, use the system in a well-lit environment.

## License

This project is open source and available under the [MIT License](LICENSE).
