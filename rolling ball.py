import pymunk
import math
import time

def run_simulation(duration=10, time_step=0.1):
    """
    Runs a text-based simulation of a ball in a rotating box.

    Args:
        duration: The duration of the simulation in seconds.
        time_step: The time step for each physics update in seconds.
    """
    # --- Pymunk Setup ---
    space = pymunk.Space()
    space.gravity = (0, 9.81)

    # Create a static square box
    box_size = 3
    box_position = (0, 0)
    box_rotation_speed = 0.2
    box_angle = 0

    box_vertices = [
        (-box_size / 2, -box_size / 2),
        (box_size / 2, -box_size / 2),
        (box_size / 2, box_size / 2),
        (-box_size / 2, box_size / 2),
    ]

    box_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    box_body.position = box_position
    box_shape = pymunk.Poly(box_body, box_vertices)
    box_shape.elasticity = 0.8
    box_shape.friction = 0.3
    space.add(box_body, box_shape)

    # Create a dynamic ball
    ball_radius = 0.1
    ball_mass = 0.1
    ball_position = (0, -1)
    ball_body = pymunk.Body(ball_mass, pymunk.moment_for_circle(ball_mass, 0, ball_radius))
    ball_body.position = ball_position
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 0.8
    ball_shape.friction = 0.3
    space.add(ball_body, ball_shape)

    # --- Simulation Loop ---
    end_time = time.time() + duration
    while time.time() < end_time:
        # Update Pymunk space
        space.step(time_step)

        # Update box rotation
        box_angle += box_rotation_speed
        box_body.angle = box_angle

        # Get ball position
        ball_x, ball_y = ball_body.position.x, ball_body.position.y

        # Get box center and corners for printing
        box_x, box_y = box_body.position.x, box_body.position.y
        half_size = box_size / 2
        
        # Calculate rotated box corners
        corners = []
        for x, y in box_vertices:
            rotated_x = x * math.cos(box_angle) - y * math.sin(box_angle)
            rotated_y = x * math.sin(box_angle) + y * math.cos(box_angle)
            corners.append((rotated_x + box_x, rotated_y + box_y))

        # Print state
        print(f"Time: {time.time() - end_time + duration:.2f}, Ball Position: ({ball_x:.2f}, {ball_y:.2f}), Box Corners: {[(c[0]-box_x, c[1]-box_y) for c in corners]}") # print relative corner positions

        # Introduce a small delay
        time.sleep(time_step)

if __name__ == "__main__":
    run_simulation()
