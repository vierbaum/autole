import socketserver
import socket
import chess
import chess.engine

from gpiozero import AngularServo, PWMLED
from time import sleep
import RPi.GPIO as GPIO

class ChessRobot:
    def __init__(self, servo_pin, motor_pin_forward, motor_pin_backward):
        """
        Initialize the ChessRobot object
        :param servo_pin: pin number for the servo
        :param motor_pin_forward: pin number for the forward motor
        :param motor_pin_backward: pin number for the backward motor
        """
        self.servo = AngularServo(servo_pin)
        self.motor = PWMLED(4)
        self.motor_pin_forward = motor_pin_forward
        self.motor_pin_backward = motor_pin_backward
        self.sf = chess.engine.SimpleEngine.popen_uci(r"./Stockfish/src/stockfish")
        self.board = chess.Board()

    def steer(self, angle):
        """
        Steer the robot to the given angle
        :param angle: angle to steer the robot to
        """
        self.servo.angle = -angle

    def drive(self, direction):
        """
        Drive the robot in the given direction
        :param direction: 1 for forward, 0 for backward
        """
        if direction == 1:
            GPIO.output(self.motor_pin_forward, GPIO.HIGH)
            GPIO.output(self.motor_pin_backward, GPIO.LOW)
        else:
            GPIO.output(self.motor_pin_forward, GPIO.LOW)
            GPIO.output(self.motor_pin_backward, GPIO.HIGH)
        self.motor.value = 0.9

    def stop(self):
        """
        Stop the robot's movement
        """
        self.motor.value = 0

    def play_chess(self, move):
        """
        Play a chess move using the Stockfish engine
        :param move: the move to play in UCI format
        :return: the move played by the engine in UCI format
        """
        self.board.push(chess.Move.from_uci(move))
        result = self.sf.play(self.board, chess.engine.Limit(time=0.5))
        self.board.push(result.move)
        return result.move.uci()

class ChessRobotTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).strip()
        if data[0] == 67:
            try:
                move = robot.play_chess(data[1:].decode())
                self.request.sendall(move.encode())
            except ValueError as e:
                print(f"Invalid move received: {e}")
                self.request.sendall("INVALID MOVE".encode())
        else:
            if data[0] == 102:
                robot.drive(1)
                self.request.sendall("DRIVING FORWARD".encode())
            elif data[0] == 98:
                robot.drive(0)
                self.request.sendall("DRIVING BACKWARD".encode())
            elif data[0] == 115:
                robot.stop()
                self.request.sendall("STOPPING".encode())
            try:
                angle = int(data[2:])
                print(angle)
                robot.steer(angle)
            except ValueError as e:
                print(f"Invalid steering angle received: {e}")

def run_server(host, port, robot):
    """
    Run the TCP server for the ChessRobot
    :param host: host IP address
    :param port: host port number
    :param robot: instance of the ChessRobot class
    """
    server = socketserver.TCPServer((host, port), ChessRobotTCPHandler)
    server.robot = robot
    server.serve_forever()

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    GPIO.setmode(GPIO.BCM)
    servo_pin = 18
    motor_pin_forward = 2
    motor_pin_backward = 3
    robot = ChessRobot(servo_pin, motor_pin_forward, motor_pin_backward)
    GPIO.setup(motor_pin_forward, GPIO.OUT)
    GPIO.setup(motor_pin_backward, GPIO.OUT)
    host, port = socket.gethostbyname("autole"), 9999

    run_server(host, port, robot)
