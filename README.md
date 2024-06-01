# throw-simulator

Perform simulation of a ball throwing

# Disclaimer

All the formulas used in this project are obtained from AI (ChatGPT and Claude) and have not been verified with appropriate sources. In theory, they all might be completely wrong; however, visually the results look correct. Nevertheless, I do not recommend blindly trusting all the calculations from this project.

This project assumes that simulations are happening in a vacuum, or air resistance is negligible, as there is no account for air or any environmental resistance during calculations.

During the simulation, possible bending of the cylinder where the ball is attached is calculated; however, any vibrations or other effects on the part of the arm positioned under the motor attachment point are not calculated and are ignored.

The end result of the simulation is provided in the form of a trajectory graph for easy comparison between different input parameters.

# Used Formulas

1. Ball radius:
   $$r_{ball} = \frac{d_{ball}}{2}$$
2. Mass of the rod:
   $$m_{rod} = \rho_{rod} \pi (\frac{d_{cylinder}}{2})^2 l_{cylinder}$$
3. Mass of the ball:
   $$m_{ball} = \rho_{ball} \pi r_{ball}^3 (\frac{4}{3})$$
4. Distance from the motor to the center of the ball in normal position:
   $$d_{ball} = \sqrt{(l_{arm} - r_{ball})^2 + (\frac{d_{cylinder}}{2} + r_{ball})^2}$$
5. Moment of inertia of the rod and the ball:
   $$I_{total} = \frac{1}{3} m_{rod} l_{cylinder}^2 + (\frac{2}{5} m_{ball} r_{ball}^2 + m_{ball} d_{ball}^2)$$
6. Total gravitational torque at the end angle:
   $$T_{gravity} = m_{rod} g (\frac{l_{arm}}{2} + (l_{cylinder} - l_{arm})) \sin(\theta_{launch}) + m_{ball} g d_{ball} \sin(\theta_{launch})$$
7. Total torque at the end angle:
   $$T_{total} = T_{max} - T_{gravity}$$
8. Angular acceleration:
   $$\alpha = \frac{T_{total}}{I_{total}}$$
9. Angular speed:
   $$\omega = \min(\sqrt{2 \alpha (\theta_{launch} - \theta_{start})}, \omega_{max})$$
10. Centrifugal force:
    $$F_{centrifugal} = m_{ball} d_{ball} \omega^2$$
11. Rod deformation:
    $$\delta_{rod} = \frac{F_{centrifugal} l_{cylinder}^3}{3 E_{rod} I_{total}}$$
12. Actual launch angle:
    $$\theta_{actual} = \theta_{launch} - \arctan(\frac{\delta_{rod}}{d_{ball}})$$
13. Ball position in world space:
    $$x_{ball} = x_{engine} + d_{ball} \cos(\theta_{actual})$$
    $$y_{ball} = y_{engine} + d_{ball} \sin(\theta_{actual})$$
14. Initial velocity of the ball:
    $$v_0 = d_{ball} \omega$$
15. Components of initial velocity:
    $$v_{0x} = v_0 \cos(\theta_{actual} + \frac{\pi}{2})$$
    $$v_{0y} = v_0 \sin(\theta_{actual} + \frac{\pi}{2})$$
16. Time of flight:
    $$t_{flight} = \frac{v_{0y} + \sqrt{v_{0y}^2 + 2 g y_{ball}}}{g}$$
17. Trajectory equations:
    $$x(t) = x_{ball} + v_{0x} t$$
    $$y(t) = y_{ball} + v_{0y} t - \frac{1}{2} g t^2$$
18. Travel distance:
    $$d_{travel} = |x(t_{flight}) - x(0)|$$

# Project details

Project is implemented using python and django framework.

Project comes with Docker file and docker-compose.yml file. In order to run the project use docker-compose.yml file.

`docker-compose build`

`docker-compose up`

You can then access project at `localhost:8010`
