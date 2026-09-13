# my_turtle_pkg

A ROS 2 (`ament_python`) package built on top of `turtlesim` that demonstrates:

- **Reactive control** of the turtle (boundary-avoidance driving + pen-color switching based on position), and
- **Service-driven shape drawing** (triangle, hexagon, star) with pause/resume/reset controls, exposed as a small interactive CLI client.

A demo recording of the package in action is included as `ros2_task.mp4`.

## Package layout

```
my_turtle_pkg/
├── my_turtle_pkg/
│   ├── __init__.py
│   ├── turtle_control.py   # TurtleController node
│   ├── shape_server.py     # ShapeServer node
│   └── shape_client.py     # ShapeClient node (interactive CLI)
├── resource/my_turtle_pkg
├── test/                   # ament copyright / flake8 / pep257 tests
├── package.xml
├── setup.py
└── setup.cfg
```

## Nodes

### `turtle_control` — `TurtleController`
Subscribes to `/turtle1/pose` and publishes `/turtle1/cmd_vel` to drive the turtle continuously:

- Near the edges of the sim (x/y outside the `[2.0, 9.0]` range), it slows down and turns sharply to steer back toward the center.
- Otherwise, it drives straight at higher speed.
- Whenever the turtle crosses `x = 5.5`, it calls the `/turtle1/set_pen` service to switch the trail color — **red** when crossing above 5.5, **green** when crossing back below.

### `shape_server` — `ShapeServer`
Publishes `/turtle1/cmd_vel` and exposes plain `std_srvs/Trigger` services (no custom `.srv` files needed):

| Service     | Effect |
|-------------|--------|
| `/triangle` | Drives the turtle in a 3-sided polygon |
| `/hexagon`  | Drives the turtle in a 6-sided polygon |
| `/star`     | Drives the turtle in a 5-pointed star pattern |
| `/pause`    | Freezes the current shape mid-drawing |
| `/resume`   | Continues a paused shape |
| `/reset`    | Stops, teleports the turtle back to the center via `/turtle1/teleport_absolute`, and clears the canvas via `/clear` |

Shapes are generated as timed `(duration, linear_speed, angular_speed)` steps and executed on a 20 Hz timer.

### `shape_client` — `ShapeClient`
A simple interactive command-line node. It creates one `Trigger` client per command and sends requests to `shape_server` based on typed input:

```
Type a command: triangle | star | hexagon | pause | resume | reset | quit
shape_client>
```

## Requirements

- ROS 2 (built against Python 3.10 — e.g. Humble)
- `turtlesim`, `rclpy`, `geometry_msgs`, `std_srvs`

## Build

From the root of your colcon workspace:

```bash
colcon build --packages-select my_turtle_pkg
source install/setup.bash
```

## Run

Start the simulator first (needed by both demos):

```bash
ros2 run turtlesim turtlesim_node
```

**Option A — reactive boundary control + pen switching:**

```bash
ros2 run my_turtle_pkg turtle_control
```

**Option B — shape-drawing demo:**

```bash
# Terminal 1
ros2 run my_turtle_pkg shape_server

# Terminal 2
ros2 run my_turtle_pkg shape_client
```

Then type any of `triangle`, `hexagon`, `star`, `pause`, `resume`, `reset`, or `quit` at the `shape_client>` prompt.

> Note: `turtle_control` and `shape_server` both publish to `/turtle1/cmd_vel`, so they are two independent demos — run one at a time against a fresh `turtlesim_node`, not both together.

## Author

Amr Khaled Sedik _Compputer Engineer_Ain Shams University _ARL(Racing team task)
