from django import forms


class SimulationForm(forms.Form):
    start_angle = forms.FloatField(initial=0, label='Engine Start Angle', help_text='rad',
                                   widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))  # rad
    launch_angle = forms.FloatField(initial=0.785398, label='Engine launch angle', help_text='rad',
                                    widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))  # rad
    engine_position_x = forms.FloatField(initial=0, label='Engine position x in 2D space', help_text='m',
                                         widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))  # mm
    engine_position_y = forms.FloatField(initial=0.300, label='Engine position y in 2D space', help_text='m',
                                         widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))  # mm
    engine_maximum_speed = forms.FloatField(initial=20, label='Engine maximum speed', help_text='rad/s',
                                            widget=forms.NumberInput(
                                                attrs={'class': 'form-control', 'step': 'any'}))  # rad/s
    engine_maximum_torque = forms.FloatField(initial=2, label='Engine Torque', help_text='Nm', widget=forms.NumberInput(
        attrs={'class': 'form-control', 'step': 'any'}))  # Nm
    cylinder_diameter = forms.FloatField(initial=0.015, label='Cylinder diameter', help_text='m',
                                         widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))  # mm
    cylinder_length = forms.FloatField(initial=0.200, label='Cylinder length', help_text='m',
                                       widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))  # mm
    cylinder_arm_length = forms.FloatField(initial=0.170, label='Cylinder arm length (above contact point with engine)',
                                           help_text='m', widget=forms.NumberInput(
            attrs={'class': 'form-control', 'step': 'any'}))  # mm
    cylinder_youngs_modulus = forms.FloatField(initial=69, label="Cylinder material Young's modus",
                                               help_text='Gpa', widget=forms.NumberInput(
            attrs={'class': 'form-control', 'step': 'any'}))  # Gpa
    cylinder_material_density = forms.FloatField(initial=2720, label='Cylinder material density',
                                                 help_text='Kg/m^3', widget=forms.NumberInput(
            attrs={'class': 'form-control', 'step': 'any'}))  # g/cm^3
    ball_diameter = forms.FloatField(initial=0.015, label='Ball diameter', help_text='m',
                                     widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))  # mm
    # Currently not used in the calculations
    # ball_youngs_modulus = forms.FloatField(initial=78, label="Ball material Young's modus", help_text='Gpa',
    #                                        widget=forms.NumberInput(
    #                                            attrs={'class': 'form-control', 'step': 'any'}))  # Gpa
    ball_material_density = forms.FloatField(initial=7870, label='Ball material density',
                                             help_text='Kg/m^3', widget=forms.NumberInput(
            attrs={'class': 'form-control', 'step': 'any'}))  # g/cm^3
    environment_gravity = forms.FloatField(initial=9.80665, label='Environment gravity', help_text='m/s^2',
                                           widget=forms.NumberInput(
                                               attrs={'class': 'form-control', 'step': 'any'}))  # m/s^2
