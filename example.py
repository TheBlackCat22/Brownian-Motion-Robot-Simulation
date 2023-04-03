from Brownian_Robot import Simulation

BACKGROUND_COLOUR = (0,0,0)
ROBOT_RADIUS = 30
ROBOT_COLOUR = (255, 255, 255)
ROBOT_TRANSLATIONAL_VELOCITY = 3
ROBOT_ROTATIONAL_VELOCITY = 1

sim = Simulation(
    bg_color = BACKGROUND_COLOUR,
    robot_radius = ROBOT_RADIUS,
    robot_colour = ROBOT_COLOUR,
    robot_translational_velocity = ROBOT_TRANSLATIONAL_VELOCITY,
    robot_rotational_velocity = ROBOT_ROTATIONAL_VELOCITY
    )

sim.run()