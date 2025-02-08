# pixel_kpi/components/firework.py
from ..displays.base_display import BaseDisplay
import numpy as np
from typing import Tuple
import random

class Firework:
    def __init__(self, display: BaseDisplay, position: Tuple[int, int] = (0, 0), max_height: int = 55, min_heigt: int = 30, num_rockets = 10):
        self.timestep = 0  # Initialize the internal timestep
        self.display = display
        self.position = (position[0], min(64, max(0, position[1] + random.randint(-5, 5))))  # Randomize the initial position
        self.height = random.randint(min_heigt, max_height)  # Randomize the height of the firework
        self.num_rockets = num_rockets
        self.explosion_steps = random.randint(5, 10)  # Randomize the number of explosion steps
        self.spark_positions = []  # To store the position of each spark
        self.spark_colors = []  # To store the colors of each spark
        self.rocket_color = [(random.randint(200, 255), random.randint(100, 255), random.randint(50, 255)) for i in range(num_rockets)]  # Random bright colors
        self.fired_rockets = 0

        self._initialize_sparks()


    def draw(self) -> None:
        """
        Draws an enhanced firework animation with color transitions, randomized directions, and fade effects.
        """
        # Increase timestep for the next frame
        self.timestep += 1

        if self.timestep < self.height:
            self._draw_fire_spark()
        else:
            self._draw_explosion()

        if self.fired_rockets == self.num_rockets:
            self.fired_rockets = 0
            self._initialize_sparks()

    def _draw_explosion(self) -> None:
        """
        Draws the explosion effect of the firework.
        """

        # Draw each spark and update its position
        spark_pos = self.spark_positions[self.fired_rockets]
        spark_color = self.spark_colors[self.fired_rockets]


        # Draw each spark and update its position
        for i, (spark_pos, spark_color) in enumerate(zip(self.spark_positions, self.spark_colors)):
            x, y = spark_pos
            color = spark_color

            # Move each spark outward and draw it
            self.spark_positions[i] = (x + random.randint(-1, 1), y + random.randint(-1, 1))  # Random movement
            self._draw_pixel(self.spark_positions[i], color)

        # Apply a fade effect by gradually reducing the brightness
        self._apply_fade()

        # Clear the screen periodically to refresh the explosion
        if self.timestep > self.height + self.explosion_steps:
            #self.display.clear()  # Assuming BaseDisplay has a clear method
            self._initialize_sparks()  # Reinitialize sparks for the next explosion
            self.fired_rockets += 1
            self.timestep = 0
            self.explosion_steps = random.randint(6, 9)  # Randomize the number of explosion steps
            

    def _draw_fire_spark(self) -> None:
        """
        Draws a vertical line of sparks (2-3 pixels) that moves upward at the specified position.
        """
        
        x, y = self.position
        x = x - self.timestep  # Update the vertical position based on the timestep
         
        # Draw a vertical line of sparks (2-3 pixels long)
        for i in range(2, 4):  # Adjust this range for 2 or 3 pixels
            if 0 <= y - i < self.display.height:  # Ensure we don't go out of bounds
                try:
                    self.display.screen[x - i, y] = self.rocket_color[self.fired_rockets]
                    self.display.screen[x - i, y + 1] = self.display.background_color
                except IndexError:
                    pass

 
    def _initialize_sparks(self) -> None:
        """
        Initialize the positions and colors of the sparks for the explosion.
        """
        self.spark_positions = []
        self.spark_colors = []

        for _ in range(self.num_rockets):  # Create a random number of sparks
            angle = random.uniform(0, 2 * np.pi)  # Randomize angle
            distance = random.uniform(2, 8)  # Randomize distance from the center

            x_offset = int(np.cos(angle) * distance) - self.height 
            y_offset = int(np.sin(angle) * distance) 

            spark_pos = (self.position[0] + x_offset, self.position[1] + y_offset)
            spark_color = (random.randint(200, 255), random.randint(100, 255), random.randint(50, 255))  # Random bright colors

            self.spark_positions.append(spark_pos)
            self.spark_colors.append(spark_color)

    def _draw_pixel(self, position: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """
        Draw a single pixel at a given position.
        """
        x, y = position
        if 0 <= x < self.display.width and 0 <= y < self.display.height:
            self.display.screen[x, y] = color

    def _apply_fade(self) -> None:
        """
        Gradually fades the firework sparks to simulate the fading of an explosion.
        """
        fade_factor = 0.9  # Adjust this factor for faster/slower fade
        for x in range(self.display.width):
            for y in range(self.display.height):
                current_color = self.display.screen[x, y]
                faded_color = tuple([int(c * fade_factor) for c in current_color])
                self.display.screen[x, y] = faded_color
