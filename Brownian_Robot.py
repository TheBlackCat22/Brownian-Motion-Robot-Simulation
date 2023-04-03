import pygame
import math
import random


class Simulation():
    """
    A class used to represent the Entire Simulation

    Parameters
    ----------
    window_size: tuple[int, int], optional
        The size of the simulation window (default is 900x500)
    fps: int, optional
        Simulation fps (default is 60)
    bg_colour: tuple[int, int, int], optional
        The RBG Background colour of the simulation environment (default is White)
    robot_raduis: int, optional
        Radius of Robot (default is 20 pixel)
    robot_colour: tuple[int, int, int], optional
        The RBG colour of the robot (default is Blue)
    robot_translational_velocity: int, optional
        The Translational velocity of the robot in Pixel/Frame (default is 1 pixel/frame)
    robot_rotational_velocity: int, optional
        The Rotatinal velocity of the robot in Degree/Frame (default is 1 degree/frame)
    max_rotation_time: int, optional
        The maximum amount of time the robot is allowed to rotate when it collides with the 
        boundarymes the robot is allowed to rotate when it collides with the boundary in seconds
        (default is 2 sec)

    Methods
    -------
    run() -> None
        Used to start the simulation and loop through every frame of the simulation
    _draw_window() -> None
        Used to draw the robot and the environment on the window.
    """

    def __init__(self,
                 window_size: tuple[int, int] = (900, 500),
                 fps: int = 60,
                 bg_color: tuple[int, int, int] = (255, 255, 255),
                 robot_radius: int = 20,
                 robot_colour: tuple[int, int, int] = (0, 0, 255),
                 robot_translational_velocity: int = 1,
                 robot_rotational_velocity: int = 1,
                 max_rotation_time: int = 2):

        self.window_size = window_size
        self.fps = fps
        self.bg_color = bg_color

        pygame.init()
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Brownian Motion in Robot")
        self.clock = pygame.time.Clock()

        self.robot = Robot(
            center=(self.window_size[0]/2,
                    self.window_size[1]/2),
            raduis=robot_radius, colour=robot_colour,
            translational_velocity=robot_translational_velocity,
            rotational_velocity=robot_rotational_velocity,
            max_rotation_frames=fps * max_rotation_time
        )

    def run(self) -> None:
        run = True
        while run:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("\n\nQuitting!!!!")
                    run = False

            if self.robot.rotation_frames == 0:
                if not self.robot.move(self.window.get_rect()):
                    self.robot.rotation_frames = random.randint(
                        1, self.robot.max_rotation_frames)
                    self.robot.moving_angle += self.robot.rotation_frames*self.robot.rotational_velocity
                    if self.robot.moving_angle > 360:
                        self.robot.moving_angle = self.robot.moving_angle % 360
                    print(
                        f"\nCollided! Rotating for {round(self.robot.rotation_frames/self.fps, 2)} Seconds")
            else:
                self.robot.rotation_frames -= 1

            self._draw_window()

        pygame.quit()

    def _draw_window(self) -> None:
        self.window.fill(self.bg_color)
        self.robot.draw_robot(self.window)
        pygame.display.update()


class Robot():
    """
    A class used to represent the Robot

    Parameters
    ----------
    center: tuple[float, float]
        The x, y coordinate of the center of robot at its starting point.
    raduis: int
        Radius of Robot
    colour: tuple[int, int, int]
        The RBG colour of the robot.
    translational_velocity: int
        The Translational velocity of the robot in Pixel/Frame
    rotational_velocity: int
        The Rotatinal velocity of the robot in Degree/Frame
    max_rotation_frames: int
        The maximum number of frames the robot is allowed to rotate when it collides with the boundary

    Methods
    -------
    draw_robot(window: pygame.display) -> None
        Draws the robot on the given window
    _check_collision(center: tuple[int, int], rect: pygame.Rect) -> bool
        Checks if the robot collides with the boundary of the window at the given center
    move(rect: pygame.Rect) -> bool
        Returns True if robot is able to move in this frame otherwise returns False
    """

    def __init__(self,
                 center: tuple[float, float],
                 raduis: int,
                 colour: tuple[int, int, int],
                 translational_velocity: int,
                 rotational_velocity: int,
                 max_rotation_frames: int):

        self.center = center
        self.radius = raduis
        self.colour = colour
        self.translational_velocity = translational_velocity
        self.rotational_velocity = rotational_velocity
        self.max_rotation_frames = max_rotation_frames

        self.moving_angle = 0
        self.rotation_frames = 0

    def draw_robot(self, window: pygame.display) -> None:
        pygame.draw.circle(window, self.colour, self.center, self.radius)

    def _check_collision(self, center: tuple[int, int], rect: pygame.Rect) -> bool:
        return (((center[0]+self.radius) > rect.right)
                or ((center[0]-self.radius) < rect.left)
                or ((center[1]+self.radius) > rect.bottom)
                or ((center[1]-self.radius) < rect.top))

    def move(self, rect: pygame.Rect) -> bool:
        x = self.center[0] + math.cos(self.moving_angle *
                                      math.pi/180)*self.translational_velocity
        y = self.center[1] + math.sin(self.moving_angle *
                                      math.pi/180)*self.translational_velocity
        if self._check_collision((x, y), rect):
            return False
        else:
            self.center = (x, y)
            return True


if __name__ == '__main__':
    env = Simulation(robot_radius=30, robot_translational_velocity=5)
    env.run()
