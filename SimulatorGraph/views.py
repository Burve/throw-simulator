import base64
import io
import urllib.parse
import datetime

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.table import Table
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.transforms import Bbox
import numpy as np
from django.http import FileResponse
from django.shortcuts import render

from .forms import SimulationForm


# Create your views here.
def simulation(request):
    if request.method == 'POST':
        form = SimulationForm(request.POST)
        if form.is_valid():

            start_angle = form.cleaned_data['start_angle']
            launch_angle = form.cleaned_data['launch_angle']
            engine_position_x = form.cleaned_data['engine_position_x']
            engine_position_y = form.cleaned_data['engine_position_y']
            engine_maximum_speed = form.cleaned_data['engine_maximum_speed']
            engine_maximum_torque = form.cleaned_data['engine_maximum_torque']
            cylinder_diameter = form.cleaned_data['cylinder_diameter']
            cylinder_length = form.cleaned_data['cylinder_length']
            cylinder_arm_length = form.cleaned_data['cylinder_arm_length']
            cylinder_youngs_modulus = form.cleaned_data['cylinder_youngs_modulus']
            cylinder_material_density = form.cleaned_data['cylinder_material_density']
            ball_diameter = form.cleaned_data['ball_diameter']
            # ball_youngs_modulus = form.cleaned_data['ball_youngs_modulus']
            ball_material_density = form.cleaned_data['ball_material_density']
            environment_gravity = form.cleaned_data['environment_gravity']

            # Simulation calculation:

            # Phase 0. Calculate helping parameters for the simulation.

            # ball radius
            ball_radius = ball_diameter / 2

            # calculating mass of the rod and the ball
            m_rod = cylinder_material_density * np.pi * (cylinder_diameter / 2) ** 2 * cylinder_length
            m_ball = ball_material_density * np.pi * ball_radius ** 3 * (4 / 3)

            # calculating distance from the motor to the center of the ball in normal position
            distance_to_ball_center = np.sqrt(
                (cylinder_arm_length - ball_radius) ** 2 + ((cylinder_diameter / 2) + ball_radius) ** 2)

            # calculations for the motor movement arc
            movement_start_angle = np.degrees(start_angle)
            movement_end_angle = np.degrees(launch_angle)

            # Phase 1. Calculate the speed of the engine that was achieved during provided motion.

            # calculating moment of inertia of the rod and the ball
            I_total = (1 / 3) * m_rod * cylinder_length ** 2 + (
                    (2 / 5) * m_ball * ball_radius ** 2 + m_ball * distance_to_ball_center ** 2)

            # calculating total gravitational torque at the end angle
            T_gravity = m_rod * environment_gravity * (
                    cylinder_arm_length / 2 + (cylinder_length - cylinder_arm_length)) * np.sin(
                launch_angle) + m_ball * environment_gravity * distance_to_ball_center * np.sin(launch_angle)

            # calculating total torque at the end angle
            T_total = engine_maximum_torque - T_gravity

            # calculating angular acceleration
            alpha = T_total / I_total

            # calculating angular speed
            omega = np.sqrt(2 * alpha * (launch_angle - start_angle))

            # capping angular speed to the maximum speed of the engine
            omega = min(omega, engine_maximum_speed)

            # Phase 2. Calculate actual angle at what ball was thrown.

            # calculating centrifugal force
            F_centrifugal = m_ball * distance_to_ball_center * omega ** 2

            # calculate rod deformation
            rod_deformation = F_centrifugal * cylinder_length ** 3 / (3 * cylinder_youngs_modulus * I_total)

            # calculating angle at which the ball was thrown
            actual_launch_angle = launch_angle - np.arctan(rod_deformation / distance_to_ball_center)

            # Phase 3. Calculate the trajectory of the ball.

            # calculate ball position in the world space
            ball_position_x = engine_position_x + distance_to_ball_center * np.cos(actual_launch_angle)
            ball_position_y = engine_position_y + distance_to_ball_center * np.sin(actual_launch_angle)

            # calculating initial velocity of the ball
            v_0 = distance_to_ball_center * omega

            # Calculate the angle of the initial velocity vector
            release_angle = actual_launch_angle + np.pi / 2

            # Calculate the x and y components of the initial velocity
            v_0x = v_0 * np.cos(release_angle)
            v_0y = v_0 * np.sin(release_angle)

            # calculating time of flight
            t_flight = (v_0y + np.sqrt(v_0y ** 2 + 2 * environment_gravity * ball_position_y)) / environment_gravity

            # preparing time array for plotting
            t_values = np.linspace(0, t_flight, 500)

            # calculating trajectory equations
            x_values = ball_position_x + v_0x * t_values
            y_values = ball_position_y + v_0y * t_values - 0.5 * environment_gravity * t_values ** 2

            # calculating travel distance by x axes
            travel_distance = abs(x_values[-1] - x_values[0])

            # creating arc
            html_arc = patches.Arc((engine_position_x, engine_position_y), 2 * distance_to_ball_center,
                                   2 * distance_to_ball_center,
                                   angle=0, theta1=movement_start_angle, theta2=np.degrees(actual_launch_angle),
                                   color='blue', label='Engine movement arc')

            # Creating dummy artists for the legend
            trajectory_patch = plt.Line2D([0], [0], color='red', label='Simulated trajectory')
            arc_patch = plt.Line2D([0], [0], color='blue', label='Launch Arc')

            # Create the plot for HTML display
            plt.figure(figsize=(6, 4))  # Adjust the figure size as needed
            plt.plot(x_values, y_values, label='Simulated trajectory', color='red')
            plt.gca().add_patch(html_arc)
            plt.axis('equal')
            plt.legend(handles=[trajectory_patch, arc_patch])
            plt.title('Ball trajectory simulation')
            plt.xlabel('Horizontal distance measured in meters')
            plt.ylabel('Vertical distance measured in meters')

            # Save the plot for HTML display to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            plt.close()

            # Create an A4-sized PDF with the plot and parameters
            pdf_file = "plot_with_metadata.pdf"
            with PdfPages(pdf_file) as pdf:
                # Create a new figure for the PDF plot
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.27, 11.69), gridspec_kw={'height_ratios': [1, 1]})

                # Create the arc patch for PDF plot
                pdf_arc = patches.Arc((engine_position_x, engine_position_y), 2 * distance_to_ball_center,
                                      2 * distance_to_ball_center,
                                      angle=0, theta1=movement_start_angle, theta2=np.degrees(actual_launch_angle),
                                      color='blue', label='Engine movement arc')

                # Plot the trajectory and arc in the upper subplot
                ax1.plot(x_values, y_values, label='Simulated trajectory', color='red')
                ax1.add_patch(pdf_arc)
                ax1.axis('equal')
                ax1.legend(handles=[trajectory_patch, arc_patch])
                ax1.set_title('Ball trajectory simulation')
                ax1.set_xlabel('Horizontal distance measured in meters')
                ax1.set_ylabel('Vertical distance measured in meters')

                # Create a table for the parameters
                table_data = [
                    ['Engine Position', f'({engine_position_x}, {engine_position_y})', 'meters'],
                    ['Cylinder Arm Length', f'{cylinder_arm_length}', 'meters'],
                    ['Cylinder Length', f'{cylinder_length}', 'meters'],
                    ['Cylinder Diameter', f'{cylinder_diameter}', 'meters'],
                    ['Cylinder Material Young\'s Modulus', f'{cylinder_youngs_modulus}', 'Gpa'],
                    ['Cylinder Material Density', f'{cylinder_material_density}', 'Kg/m^3'],
                    ['Movement Start Angle', f'{movement_start_angle:.2f}', 'radians'],
                    ['Movement End Angle', f'{movement_end_angle:.2f}', 'radians'],
                    ['Engine Torque', f'{engine_maximum_torque}', 'Nm'],
                    ['Engine Max Speed', f'{engine_maximum_speed}', 'radians/second'],
                    ['Ball Diameter', f'{ball_diameter}', 'meters'],
                    # ['Ball Material Young\'s Modulus', f'{ball_youngs_modulus}', 'Gpa'],
                    ['Ball Material Density', f'{ball_material_density}', 'Kg/m^3'],
                    ['Environment Gravity', f'{environment_gravity}', 'meters/second^2'],
                    ['Omega', f'{omega:.3f}', 'radians/second'],
                    ['Travel Distance', f'{travel_distance:.3f}', 'meters']
                ]

                # Create the table and add it to the lower subplot
                table = ax2.table(cellText=table_data, cellLoc='left', loc='center', colWidths=[0.5, 0.2, 0.3])
                table.auto_set_font_size(False)
                table.set_fontsize(12)
                table.scale(1, 1.5)  # Adjust the height of the table

                ax2.axis('off')

                # Adjust the spacing between subplots
                plt.tight_layout()

                # Save the plot and parameters to the PDF
                pdf.savefig(fig)

                # Add metadata to the PDF
                d = pdf.infodict()
                d['Title'] = 'Ball throw simulation results'
                d['Author'] = 'Ball trajectory simulator'
                d['Subject'] = 'Plot with additional data'
                d['Keywords'] = 'matplotlib, plot, arc, metadata'
                d['CreationDate'] = datetime.datetime.today()
                d['ModDate'] = datetime.datetime.today()

            graph_generated = True

            return render(request, 'simulation.html', {'form': form, 'plot': uri, 'travel_distance': travel_distance,
                                                       'graph_generated': graph_generated})
    else:
        form = SimulationForm()

    return render(request, 'simulation.html', {'form': form})


def download_plot(request):
    pdf_file = "plot_with_metadata.pdf"
    return FileResponse(open(pdf_file, 'rb'), as_attachment=True, filename='plot_with_metadata.pdf')
