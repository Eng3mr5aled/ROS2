import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

COMMANDS = ['triangle', 'star', 'hexagon', 'pause', 'resume', 'reset']


class ShapeClient(Node):

    def __init__(self):
        super().__init__('shape_client')
        # One client per service name (matches the server's service names).
        self.service_clients = {name: self.create_client(Trigger, name) for name in COMMANDS}

    def send(self, command):
        client = self.service_clients.get(command)
        if client is None:
            print(f"Unknown command '{command}'.")
            return
        if not client.wait_for_service(timeout_sec=2.0):
            print('shape_server is not running.')
            return
        future = client.call_async(Trigger.Request())
        rclpy.spin_until_future_complete(self, future)
        print('->', future.result().message)


def main():
    rclpy.init()
    node = ShapeClient()

    print('Type a command: triangle | star | hexagon | pause | resume | reset | quit')
    while True:
        command = input('shape_client> ').strip().lower()
        if command in ('quit', 'exit'):
            break
        if command:
            node.send(command)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()