import numpy as np

NEW_POSITION = 0

def disable_shield_left(self):
    '''
    disable_shield_left: Disables the left shield.
    '''
    shield_status_left = self.get_ram()[43:52]
    for i in range(len(shield_status_left)):
        shield_status_left[i] = 0
        self.set_ram(i+43,shield_status_left[i])

def disable_shield_middle(self):
    '''
    disable_shield_middle: Disables the middle shield.
    '''
    shield_status_middle = self.get_ram()[52:61]
    for i in range(len(shield_status_middle)):
        shield_status_middle[i] = 0
        self.set_ram(i+52, shield_status_middle[i])

def disable_shield_right(self):
    '''
    disable_shield_right: Disables the right shield.
    '''
    shield_status_right = self.get_ram()[61:71]
    for i in range(len(shield_status_right)):
        shield_status_right[i] = 0
        self.set_ram(i+61, shield_status_right[i])

def relocate_shields(self):
    '''
    relocate_shields: Allows for the relocation of the shields via an offset.
    '''
    shield_pos_new = NEW_POSITION
    if shield_pos_new < 53 and shield_pos_new >= 35:
        self.set_ram(27, shield_pos_new)

def curved_shots(self):
    '''
    curved_shots: Makes the shots travel on a curved path.
    '''
    curr_laser_pos = self.get_ram()[87]
    # Manipulate the value in RAM cell 87 as long as the upper and the lower threshold
    # are not reached.
    if 40 < curr_laser_pos < 122:
        laser_displacement = calculate_x_displacement(curr_laser_pos)
        self.set_ram(87, laser_displacement)

# calculates the x coordinate displacement based on a parabolic function
def calculate_x_displacement(current_x):
    '''
    calculate_x_displacement: calculates the displacement value based on a parabolic function
    and the current x position.
    '''
    if current_x < 81:
        x_out = -0.01 * current_x + current_x
    else:
        x_out = 0.01 * current_x + current_x
    x_out = int(np.round(x_out))
    return int(x_out)

def modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "disable_shield_left":
            step_modifs.append(disable_shield_left)
        elif mod == "disable_shield_middle":
            step_modifs.append(disable_shield_middle)
        elif mod == "disable_shield_right":
            step_modifs.append(disable_shield_right)
        elif mod == "disable_shields":
            step_modifs.append(disable_shield_left)
            step_modifs.append(disable_shield_middle)
            step_modifs.append(disable_shield_right)
        elif mod == "curved":
            step_modifs.append(curved_shots) 
        elif mod.startswith('relocate'):
            mod_n = int(mod[-2:])
            if mod_n < 35 or mod_n > 53:
                raise ValueError("Invalid position for shields")
            global NEW_POSITION
            NEW_POSITION = mod_n
            reset_modifs.append(relocate_shields)        
    return step_modifs, reset_modifs