import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty, Trigger
from turtlesim.srv import TeleportAbsolute

CENTER_X = 5.544445
CENTER_Y = 5.544445


def polygon(sides, turn_deg, side_time=1.5, speed=2.0, turn_speed=1.2):
    """Build a shape as a list of (time, linear_speed, angular_speed) steps."""
    turn_time = math.radians(turn_deg) / turn_speed
    steps = []
    for _ in range(sides):
        steps.append((side_time, speed, 0.0))       # go straight
        steps.append((turn_time, 0.0, turn_speed))  # turn
    return steps


SHAPES = {
    'triangle': lambda: polygon(sides=3, turn_deg=120),
    'hexagon': lambda: polygon(sides=6, turn_deg=60, side_time=1.2),
    'star': lambda: polygon(sides=5, turn_deg=144, side_time=2.0, turn_speed=1.5),
}


class ShapeServer(Node):

    def __init__(self):
        super().__init__('shape_server')

        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.teleport_client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.clear_client = self.create_client(Empty, '/clear')

        # One plain std_srvs/Trigger service per command - no custom .srv needed.
        self.create_service(Trigger, 'triangle', self.make_shape_cb('triangle'))
        self.create_service(Trigger, 'star', self.make_shape_cb('star'))
        self.create_service(Trigger, 'hexagon', self.make_shape_cb('hexagon'))
        self.create_service(Trigger, 'pause', self.pause_cb)
        self.create_service(Trigger, 'resume', self.resume_cb)
        self.create_service(Trigger, 'reset', self.reset_cb)

        self.steps = []       # steps left to run for the current shape
        self.time_left = 0.0
        self.paused = False

        self.create_timer(0.05, self.tick)  # 20 times per second

        self.get_logger().info(
            'Ready. Services: /triangle /star /hexagon /pause /resume /reset')

    def tick(self):
        if self.paused or not self.steps:
            self.cmd_pub.publish(Twist())  # stop
            return

        duration, linear, angular = self.steps[0]
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.cmd_pub.publish(msg)

        self.time_left -= 0.05
        if self.time_left <= 0:
            self.steps.pop(0)
            if self.steps:
                self.time_left = self.steps[0][0]
            else:
                self.get_logger().info('Shape finished.')

    def make_shape_cb(self, name):
        def callback(request, response):
            self.steps = SHAPES[name]()
            self.time_left = self.steps[0][0]
            self.paused = False
            response.success = True
            response.message = f'Drawing {name}.'
            return response
        return callback

    def pause_cb(self, request, response):
        self.paused = True
        response.success = True
        response.message = 'Paused.'
        return response

    def resume_cb(self, request, response):
        self.paused = False
        response.success = True
        response.message = 'Resumed.'
        return response

    def reset_cb(self, request, response):
        self.steps = []
        self.paused = False
        self.cmd_pub.publish(Twist())
        self.reset_turtle()
        response.success = True
        response.message = 'Turtle reset to the center.'
        return response

    def reset_turtle(self):
        if self.teleport_client.wait_for_service(timeout_sec=2.0):
            req = TeleportAbsolute.Request()
            req.x = CENTER_X
            req.y = CENTER_Y
            req.theta = 0.0
            self.teleport_client.call_async(req)
        if self.clear_client.wait_for_service(timeout_sec=1.0):
            self.clear_client.call_async(Empty.Request())


def main():
    rclpy.init()
    node = ShapeServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()