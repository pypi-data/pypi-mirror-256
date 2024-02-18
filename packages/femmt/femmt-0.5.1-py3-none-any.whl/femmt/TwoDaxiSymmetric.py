# Python standard libraries
from logging import warning
import numpy as np
from typing import List

# Local libraries
from femmt.enumerations import *
from femmt.data import MeshData
from femmt.model import Core, VirtualWindingWindow, AirGaps, StrayPath, Insulation

class TwoDaxiSymmetric:
    """
    This class creates the model of the magnetic component. This is done by creating lists of points which
    will be later added to the gmsh file.

    :return:

    """

    core: Core
    virtual_winding_windows: List[VirtualWindingWindow]
    air_gaps: AirGaps
    stray_path: StrayPath
    insulation: Insulation
    component_type: ComponentType
    mesh_data: MeshData
    number_of_windings: int

    # List of points which represent the model
    # Every List is a List of 4 Points: x, y, z, mesh_factor
    p_outer: List[List[float]]
    p_region_bound: List[List[float]] 
    p_window: List[List[float]] 
    p_air_gaps: List[List[float]]
    p_conductor: List[List[float]]
    p_iso_core: List[List[float]]
    p_iso_pri_sec: List[List[float]]

    def __init__(self, core: Core, mesh_data: MeshData, air_gaps: AirGaps, virtual_winding_windows: List[VirtualWindingWindow], 
                stray_path: StrayPath, insulation: Insulation, component_type: ComponentType, number_of_windings: int):
        self.core = core
        self.mesh_data = mesh_data
        self.virtual_winding_windows = virtual_winding_windows
        self.air_gaps = air_gaps
        self.component_type = component_type
        self.stray_path = stray_path
        self.insulation = insulation
        self.number_of_windings = number_of_windings

        # -- Arrays for geometry data -- 
        # TODO Is the zero initialization necessary?
        self.p_outer = np.zeros((4, 4))
        self.p_region_bound = np.zeros((4, 4))
        self.p_window = np.zeros((4 * core.number_core_windows, 4))
        self.p_air_gaps = np.zeros((4 * air_gaps.number, 4)) 
        self.p_conductor = []
        self.p_iso_core = []
        self.p_iso_pri_sec = []

        for i in range(number_of_windings):
            self.p_conductor.insert(i, [])

        self.r_inner = core.r_inner
        self.r_outer = core.r_outer

    def draw_outer(self):
        """
        Draws the outer points

        :return:
        """
        # Outer Core
        # (A_zyl=2pi*r*h => h=0.5r=0.25core_w <=> ensure A_zyl=A_core on the tiniest point)
        self.p_outer[0][:] = [-self.r_outer,
                            -self.core.core_h/2,
                            0,
                            self.mesh_data.c_core]

        self.p_outer[1][:] = [self.r_outer,
                            -self.core.core_h/2,
                            0,
                            self.mesh_data.c_core]

        self.p_outer[2][:] = [-self.r_outer,
                            self.core.core_h/2,
                            0,
                            self.mesh_data.c_core]

        self.p_outer[3][:] = [self.r_outer,
                            self.core.core_h/2,
                            0,
                            self.mesh_data.c_core]

    def draw_window(self):
        # Window
        # At this point both windows (in a cut) are modeled
        # print(f"win: c_window: {self.component.mesh.c_window}")
        self.p_window[0] = [-self.r_inner,
                            -self.core.window_h / 2,
                            0,
                            self.mesh_data.c_window]

        self.p_window[1] = [-self.core.core_inner_diameter / 2,
                            -self.core.window_h / 2,
                            0,
                            self.mesh_data.c_window]

        self.p_window[2] = [-self.r_inner,
                            self.core.window_h / 2,
                            0,
                            self.mesh_data.c_window]

        self.p_window[3] = [-self.core.core_inner_diameter / 2,
                            self.core.window_h / 2,
                            0,
                            self.mesh_data.c_window]

        self.p_window[4] = [self.core.core_inner_diameter / 2,
                            -self.core.window_h / 2,
                            0,
                            self.mesh_data.c_window]

        self.p_window[5] = [self.r_inner,
                            -self.core.window_h / 2,
                            0,
                            self.mesh_data.c_window]

        self.p_window[6] = [self.core.core_inner_diameter / 2,
                            self.core.window_h / 2,
                            0,
                            self.mesh_data.c_window]

        self.p_window[7] = [self.r_inner,
                            self.core.window_h / 2,
                            0,
                            self.mesh_data.c_window]

    def draw_air_gaps(self):
        # Air gaps
        # "air_gaps" is a list with [position_tag, air_gap_position, air_gap_h, c_air_gap]
        #   - position_tag: specifies the gapped "leg"
        #   - air_gap_position: specifies the coordinate of the air gap's center point along the specified leg
        #   - air_gap_h: height/length of the air gap
        #   - c_air_gap: mesh accuracy factor
        # at this point the 4 corner points of each air gap are generated out of "air_gaps"

        mesh_accuracy = self.core.window_w / 20 * self.mesh_data.global_accuracy

        for i in range(0, self.air_gaps.number):

            # # Left leg (-1)
            # if self.component.air_gaps.midpoints[i][0] == -1:
            #     self.p_air_gaps[i * 4] = [-(self.component.core.core_w + self.component.core.window_w),
            #                               self.component.air_gaps.midpoints[i][1] -
            #     self.component.air_gaps.midpoints[i][2] / 2, 0, self.component.air_gaps.midpoints[i][3]]
            #     self.p_air_gaps[i * 4 + 1] = [-(self.component.core.core_w / 2 + self.component.core.window_w),
            #                                   self.component.air_gaps.midpoints[i][1] -
            #     self.component.air_gaps.midpoints[i][2] / 2, 0, self.component.air_gaps.midpoints[i][3]]
            #     self.p_air_gaps[i * 4 + 2] = [-(self.component.core.core_w + self.component.core.window_w),
            #                                   self.component.air_gaps.midpoints[i][1] +
            #     self.component.air_gaps.midpoints[i][2] / 2, 0, self.component.air_gaps.midpoints[i][3]]
            #     self.p_air_gaps[i * 4 + 3] = [-(self.component.core.core_w / 2 + self.component.core.window_w),
            #                                   self.component.air_gaps.midpoints[i][1] +
            #     self.component.air_gaps.midpoints[i][2] / 2, 0, self.component.air_gaps.midpoints[i][3]]
            #
            # # Right leg (+1)
            # if self.component.air_gaps.midpoints[i][0] == 1:
            #     self.p_air_gaps[i * 4] = [self.component.core.core_w / 2 + self.component.core.window_w,
            #                               self.component.air_gaps.midpoints[i][1] -
            #     self.component.air_gaps.midpoints[i][2] / 2, 0, self.component.air_gaps.midpoints[i][3]]
            #     self.p_air_gaps[i * 4 + 1] = [self.component.core.core_w + self.component.core.window_w,
            #                                   self.component.air_gaps.midpoints[i][1] -
            #     self.component.air_gaps.midpoints[i][2] / 2, 0, self.component.air_gaps.midpoints[i][3]]
            #     self.p_air_gaps[i * 4 + 2] = [self.component.core.core_w / 2 + self.component.core.window_w,
            #                                   self.component.air_gaps.midpoints[i][1] +
            #     self.component.air_gaps.midpoints[i][2] / 2, 0, self.component.air_gaps.midpoints[i][3]]
            #     self.p_air_gaps[i * 4 + 3] = [self.component.core.core_w + self.component.core.window_w,
            #                                   self.component.air_gaps.midpoints[i][1] +
            #     self.component.air_gaps.midpoints[i][2] / 2, 0, self.component.air_gaps.midpoints[i][3]]

            # Center leg (0)
            if self.air_gaps.midpoints[i][0] == 0:
                # The center points are transformed each into 4 corner points

                air_gap_y_position = self.air_gaps.midpoints[i][1]
                air_gap_height = self.air_gaps.midpoints[i][2]
                air_gap_length_top = self.core.core_inner_diameter / 2
                air_gap_length_bot = self.core.core_inner_diameter / 2

                # Check for stray_paths in integrated transformers
                if self.component_type == ComponentType.IntegratedTransformer:
                    if self.stray_path.start_index == i:
                        # Stray path is above current air_gap
                        air_gap_length_top = self.stray_path.stray_path_radius
                    elif self.stray_path.start_index + 1 == i:
                        # Stray path is below current air_gap
                        air_gap_length_bot = self.stray_path.stray_path_radius

                # Bottom left
                self.p_air_gaps[i * 4 + 0] = [0,
                                                air_gap_y_position -
                                                air_gap_height / 2,
                                                0,
                                                self.mesh_data.c_core]

                # Bottom right
                self.p_air_gaps[i * 4 + 1] = [air_gap_length_bot,
                                                air_gap_y_position -
                                                air_gap_height / 2,
                                                0,
                                                mesh_accuracy]

                # Top left
                self.p_air_gaps[i * 4 + 2] = [0,
                                                air_gap_y_position +
                                                air_gap_height / 2,
                                                0,
                                                self.mesh_data.c_core]

                # Top right
                self.p_air_gaps[i * 4 + 3] = [air_gap_length_top,
                                                air_gap_y_position +
                                                air_gap_height / 2,
                                                0,
                                                mesh_accuracy]

        # In order to close the air gap when a stray_path is added, additional points need to be added
        if self.component_type == ComponentType.IntegratedTransformer:
            top_point = [self.core.core_inner_diameter / 2,
                            self.air_gaps.midpoints[self.stray_path.start_index+1][1] -
                            air_gap_height / 2,
                            0,
                            mesh_accuracy]
            bot_point = [self.core.core_inner_diameter / 2,
                            self.air_gaps.midpoints[self.stray_path.start_index][1] +
                            air_gap_height / 2,
                            0,
                            mesh_accuracy]
            self.p_close_air_gaps = [top_point, bot_point]

    def draw_conductors(self, draw_top_down = True):
        # Draw every conductor type based on the virtual_winding_window bounds

        for virtual_winding_window in self.virtual_winding_windows:
            # Get bounds from virtual winding window
            bot_bound = virtual_winding_window.bot_bound
            top_bound = virtual_winding_window.top_bound
            left_bound = virtual_winding_window.left_bound
            right_bound = virtual_winding_window.right_bound

            # Check the possible WindingTypes and draw accordingly
            if virtual_winding_window.winding_type == WindingType.Interleaved:
                # Two windings in the virtual winding window
                windings = virtual_winding_window.windings
                winding0 = windings[0]
                winding1 = windings[1]

                turns = virtual_winding_window.turns
                turns0 = turns[0]
                turns1 = turns[1]

                winding_numbers = [winding0.winding_number, winding1.winding_number]

                # Now check for every winding scheme which is possible for interleaved winding type
                if virtual_winding_window.winding_scheme == InterleavedWindingScheme.Bifilar:
                    """
                    - Bifilar interleaving means a uniform winding scheme of two conductors (prim. and sec.)
                    - Can only be used for conductors of identical radius (in terms of litz radius for 
                        stranded wires)
                    - Excess windings are placed below the bifilar ones
    
                    """
                    if winding0.conductor_radius != winding1.conductor_radius:
                        print("For bifilar winding scheme both conductors must be of the same radius!")
                    else:
                        print("Bifilar winding scheme is applied")

                    raise Exception("Bifilar winding scheme is not implemented yet.")

                if virtual_winding_window.winding_scheme == InterleavedWindingScheme.VerticalAlternating:
                    """
                    - Vertical interleaving means a winding scheme where the two conductors are alternating 
                        in vertical (y-)direction
                    - This is practically uncommon
                    - If the turns ratio is != 1, the scheme always begins with the "higher-turns-number's" 
                        conductor
                    """

                    raise Exception("Vertical winding scheme is not implemented yet.")

                if virtual_winding_window.winding_scheme == InterleavedWindingScheme.HorizontalAlternating:
                    """
                    - Horizontal interleaving means a winding scheme where the two conductors are alternating in 
                    horizontal  (x-)direction (Tonnenwicklung)
                    - This is practically most common
                    - If the turns ratio is != 1, the scheme always begins with the "higher-turns-number's" 
                        conductor
                        
                    """

                    # assume 2 winding transformer and dedicated stray path:
                    if draw_top_down:
                        # This will draw from top bound down

                        # Initialize the list, that counts the already placed conductors
                        N_completed = [0, 0]

                        # Initialize the starting conductor
                        if turns0 >= turns1:
                            # Primary starts first
                            col_cond = 0
                        else:
                            # Secondary starts fist
                            col_cond = 1

                        # Get winding number of current winding
                        winding_number = winding_numbers[col_cond]

                        # Initialize the x and y coordinate
                        x = left_bound + windings[col_cond].conductor_radius
                        y = top_bound - windings[col_cond].conductor_radius
                        top_window_iso_counter = 0
                        # Continue placing as long as not all conductors have been placed
                        while (turns0 - N_completed[0] != 0) or \
                                (turns1 - N_completed[1] != 0):
                            if turns[col_cond] - N_completed[col_cond] != 0:
                                # is this winding not already finished?
                                if x < right_bound - windings[col_cond].conductor_radius:
                                    while y > bot_bound + windings[col_cond].conductor_radius and \
                                            N_completed[col_cond] < turns[col_cond]:
                                        self.p_conductor[winding_number].append([
                                            x, 
                                            y, 
                                            0, 
                                            self.mesh_data.c_center_conductor[winding_number]])

                                        self.p_conductor[winding_number].append([
                                            x - windings[col_cond].conductor_radius,
                                            y,
                                            0,
                                            self.mesh_data.c_conductor[winding_number]])

                                        self.p_conductor[winding_number].append([
                                            x,
                                            y + windings[col_cond].conductor_radius,
                                            0,
                                            self.mesh_data.c_conductor[winding_number]])

                                        self.p_conductor[winding_number].append([
                                            x + windings[col_cond].conductor_radius,
                                            y,
                                            0,
                                            self.mesh_data.c_conductor[winding_number]])

                                        self.p_conductor[winding_number].append([
                                            x,
                                            y - windings[col_cond].conductor_radius,
                                            0,
                                            self.mesh_data.c_conductor[winding_number]])

                                        N_completed[col_cond] += 1

                                        y -= windings[col_cond].conductor_radius * 2 + self.insulation.inner_winding_insulations[col_cond]  # one from bot to top

                                    x += windings[col_cond].conductor_radius + \
                                            windings[(col_cond + 1) % 2].conductor_radius + \
                                            virtual_winding_window.winding_insulation

                                    # Reset y
                                    col_cond = (col_cond + 1) % 2
                                    winding_number = winding_numbers[col_cond]
                                    y = top_bound - windings[col_cond].conductor_radius
                                    top_window_iso_counter += 1
                                else:
                                    break

                            else:
                                # is this winding already finished? - continue with the other one
                                col_cond = (col_cond + 1) % 2

                                # Correct the reset of y and correct x displacement
                                x += windings[col_cond].conductor_radius - \
                                        windings[(col_cond + 1) % 2].conductor_radius \
                                        - virtual_winding_window.winding_insulation + self.insulation.inner_winding_insulations[
                                            col_cond]

                                y = top_bound - windings[col_cond].conductor_radius
                                top_window_iso_counter -= 1
                    else:
                        # This will draw from bottom bound up.

                        # Initialize the list, that counts the already placed conductors
                        N_completed = [0, 0]

                        # Initialize the starting conductor
                        if turns0 >= turns1:
                            col_cond = 0
                        else:
                            col_cond = 1

                        # Get winding number of current winding
                        winding_number = winding_numbers[col_cond]

                        # Initialize the x and y coordinate
                        x = left_bound + windings[col_cond].conductor_radius
                        y = bot_bound + windings[col_cond].conductor_radius

                        # Continue placing as long as not all conductors have been placed
                        while (turns0 - N_completed[0] != 0) or \
                                (turns1 - N_completed[1] != 0):
                            if turns[col_cond] - N_completed[col_cond] != 0:
                                # is this winding not already finished?
                                if x < right_bound - windings[col_cond].conductor_radius:
                                    while y < top_bound - windings[col_cond].conductor_radius and \
                                            N_completed[col_cond] < turns[col_cond]:
                                        self.p_conductor[winding_number].append([
                                            x, 
                                            y, 
                                            0, 
                                            self.mesh_data.c_center_conductor[winding_number]])

                                        self.p_conductor[winding_number].append([
                                            x - windings[col_cond].conductor_radius,
                                            y,
                                            0,
                                            self.mesh_data.c_conductor[winding_number]])

                                        self.p_conductor[winding_number].append([
                                            x,
                                            y + windings[col_cond].conductor_radius,
                                            0,
                                            self.mesh_data.c_conductor[winding_number]])

                                        self.p_conductor[winding_number].append([
                                            x + windings[col_cond].conductor_radius,
                                            y,
                                            0,
                                            self.mesh_data.c_conductor[winding_number]])

                                        self.p_conductor[winding_number].append([
                                            x,
                                            y - windings[col_cond].conductor_radius,
                                            0,
                                            self.mesh_data.c_conductor[winding_number]])

                                        N_completed[col_cond] += 1

                                        y += windings[col_cond].conductor_radius * 2 + \
                                                self.insulation.inner_winding_insulations[col_cond]  # one from bot to top

                                    x += windings[col_cond].conductor_radius + \
                                            windings[(col_cond + 1) % 2].conductor_radius + \
                                            virtual_winding_window.winding_insulation

                                    # Reset y
                                    col_cond = (col_cond + 1) % 2
                                    y = bot_bound + windings[col_cond].conductor_radius

                                else:
                                    break

                            else:
                                # is this winding already finished? - continue with the other one
                                col_cond = (col_cond + 1) % 2
                                winding_number = winding_numbers[col_cond]

                                # Correct the reset of y and correct x displacement
                                x += windings[col_cond].conductor_radius - \
                                        windings[(col_cond + 1) % 2].conductor_radius \
                                        - virtual_winding_window.winding_insulation + \
                                        self.insulation.inner_winding_insulations[
                                            col_cond]

                                y = bot_bound + windings[col_cond].conductor_radius
                
                if virtual_winding_window.winding_scheme == InterleavedWindingScheme.VerticalStacked:
                    winding_number0, winding_number1 = winding_numbers
                    y = bot_bound + winding0.conductor_radius

                    # Initialization
                    x = left_bound + winding0.conductor_radius
                    i = 0

                    # First winding from bottom to top
                    if winding0.conductor_arrangement == ConductorArrangement.Square:
                        while y < top_bound - winding0.conductor_radius and \
                                i < turns0:
                            while x < right_bound - winding0.conductor_radius and \
                                    i < turns0:
                                self.p_conductor[winding_number0].append([
                                    x, 
                                    y, 
                                    0, 
                                    self.mesh_data.c_center_conductor[winding_number0]])
                                self.p_conductor[winding_number0].append([
                                    x - winding0.conductor_radius, 
                                    y, 
                                    0,
                                    self.mesh_data.c_conductor[winding_number0]])
                                self.p_conductor[winding_number0].append([
                                    x,
                                    y + winding0.conductor_radius,
                                    0,
                                    self.mesh_data.c_conductor[winding_number0]])
                                self.p_conductor[winding_number0].append([
                                    x + winding0.conductor_radius, 
                                    y, 
                                    0,
                                    self.mesh_data.c_conductor[winding_number0]])
                                self.p_conductor[winding_number0].append([
                                    x, 
                                    y - winding0.conductor_radius, 
                                    0,
                                    self.mesh_data.c_conductor[winding_number0]])
                                i += 1
                                x += winding0.conductor_radius * 2 + \
                                        self.insulation.inner_winding_insulations[
                                            winding_number0]  # from left to right
                            y += winding0.conductor_radius * 2 + \
                                    self.insulation.inner_winding_insulations[
                                        winding_number0]  # one step from bot to top
                            x = left_bound + winding0.conductor_radius  # always the same
                    elif winding0.conductor_arrangement == ConductorArrangement.Hexagonal:
                            base_line = True

                            while y < top_bound - winding0.conductor_radius and \
                                    i < turns0:
                                while x < right_bound - winding0.conductor_radius and \
                                        i < turns0:
                                    self.p_conductor[winding_number0].append([
                                        x, 
                                        y, 
                                        0, 
                                        self.mesh_data.c_center_conductor[winding_number0]])
                                    self.p_conductor[winding_number0].append([
                                        x - winding0.conductor_radius, 
                                        y, 
                                        0,
                                        self.mesh_data.c_conductor[winding_number0]])
                                    self.p_conductor[winding_number0].append([
                                        x, 
                                        y + winding0.conductor_radius, 
                                        0,
                                        self.mesh_data.c_conductor[winding_number0]])
                                    self.p_conductor[winding_number0].append([
                                        x + winding0.conductor_radius, 
                                        y, 
                                        0,
                                        self.mesh_data.c_conductor[winding_number0]])
                                    self.p_conductor[winding_number0].append([
                                        x, 
                                        y - winding0.conductor_radius, 
                                        0,
                                        self.mesh_data.c_conductor[winding_number0]])
                                    i += 1

                                    x += 2 * np.cos(np.pi / 6) * (
                                            winding0.conductor_radius +
                                            self.insulation.inner_winding_insulations[winding_number0] / 2)

                                    # depending on what line, hexa scheme starts shifted
                                    # reset y to "new" bottom
                                    base_line = (not base_line)
                                    if base_line:
                                        y -= (winding0.conductor_radius +
                                                self.insulation.inner_winding_insulations[winding_number0] / 2)
                                    else:
                                        y += (winding0.conductor_radius +
                                                self.insulation.inner_winding_insulations[winding_number0] / 2)

                                # Undo last base_line reset
                                if base_line:
                                    y += (winding0.conductor_radius +
                                            self.insulation.inner_winding_insulations[winding_number0] / 2)
                                else:
                                    y -= (winding0.conductor_radius +
                                            self.insulation.inner_winding_insulations[winding_number0] / 2)

                                base_line = True
                                x = left_bound + winding0.conductor_radius
                                y += winding0.conductor_radius * 2 + \
                                        self.insulation.inner_winding_insulations[winding_number0]
                    elif winding0.conductor_arrangement == ConductorArrangement.SquareFullWidth:
                        # TODO Implement?
                        raise Exception("ConductorArrangement SquareFullWidth is not implemented for interleaved and vertical stacked")
                    else:
                        raise Exception(f"Unknown conductor_arrangement {winding0.conductor_arrangement}")

                    # Second winding from top to bottom
                    
                    y = top_bound - winding1.conductor_radius
                    i = 0

                    if winding1.conductor_arrangement == ConductorArrangement.Square:
                        while y > bot_bound + winding1.conductor_radius and i < \
                                turns1:
                            while x < right_bound - winding1.conductor_radius and i < \
                                    turns1:
                                self.p_conductor[winding_number1].append([
                                    x, 
                                    y, 
                                    0, 
                                    self.mesh_data.c_center_conductor[winding_number1]])
                                self.p_conductor[winding_number1].append([
                                    x - winding1.conductor_radius, 
                                    y, 
                                    0,
                                    self.mesh_data.c_conductor[winding_number1]])
                                self.p_conductor[winding_number1].append([
                                    x, 
                                    y + winding1.conductor_radius, 
                                    0,
                                    self.mesh_data.c_conductor[winding_number1]])
                                self.p_conductor[winding_number1].append([
                                    x + winding1.conductor_radius, 
                                    y, 
                                    0,
                                    self.mesh_data.c_conductor[winding_number1]])
                                self.p_conductor[winding_number1].append([
                                    x, 
                                    y - winding1.conductor_radius, 
                                    0,
                                    self.mesh_data.c_conductor[winding_number1]])
                                i += 1

                                x += winding1.conductor_radius * 2 + \
                                        self.insulation.inner_winding_insulations[
                                            winding_number1]  # from left to right
                            y += -(winding1.conductor_radius * 2) - \
                                    self.insulation.inner_winding_insulations[
                                        winding_number1]  # one step from bot to top
                            x = left_bound + winding1.conductor_radius  # always the same
                    elif winding1.conductor_arrangement == ConductorArrangement.Hexagonal:
                        base_line = True

                        while y > bot_bound + winding1.conductor_radius and \
                                i < turns1:
                            while x < right_bound - winding1.conductor_radius and \
                                    i < turns1:

                                self.p_conductor[winding_number1].append([
                                    x, 
                                    y, 
                                    0, 
                                    self.mesh_data.c_center_conductor[winding_number1]])
                                self.p_conductor[winding_number1].append([
                                    x - winding1.conductor_radius, 
                                    y, 
                                    0,
                                    self.mesh_data.c_conductor[winding_number1]])
                                self.p_conductor[winding_number1].append([
                                    x, 
                                    y + winding1.conductor_radius, 
                                    0,
                                    self.mesh_data.c_conductor[winding_number1]])
                                self.p_conductor[winding_number1].append([
                                    x + winding1.conductor_radius, 
                                    y, 
                                    0,
                                    self.mesh_data.c_conductor[winding_number1]])
                                self.p_conductor[winding_number1].append([
                                    x, 
                                    y - winding1.conductor_radius, 
                                    0,
                                    self.mesh_data.c_conductor[winding_number1]])

                                i += 1
                                x += 2 * np.cos(np.pi / 6) * (
                                        winding1.conductor_radius +
                                        self.insulation.inner_winding_insulations[winding_number1] / 2)

                                # depending on what line, hexa scheme starts shifted
                                # reset y to "new" bottom
                                base_line = (not base_line)
                                if base_line:
                                    y += (winding1.conductor_radius +
                                            self.insulation.inner_winding_insulations[winding_number1])
                                else:
                                    y -= (winding1.conductor_radius +
                                            self.insulation.inner_winding_insulations[winding_number1])

                            # Undo last base_line reset
                            if base_line:
                                y -= (winding1.conductor_radius +
                                        self.insulation.inner_winding_insulations[winding_number1])
                            else:
                                y += (winding1.conductor_radius +
                                        self.insulation.inner_winding_insulations[winding_number1])

                            base_line = True
                            x = left_bound + winding1.conductor_radius
                            # from top to bottom
                            y += -(winding1.conductor_radius * 2) - \
                                    self.insulation.inner_winding_insulations[
                                        winding_number1]
                    else:
                        raise Exception(f"Unknown conductor_arrangement {winding1.conductor_arrangement.name}")
            elif virtual_winding_window.winding_type == WindingType.Single:
                # One winding in the virtual winding window
                winding = virtual_winding_window.windings[0]
                turns = virtual_winding_window.turns[0]
                conductor_type = winding.conductor_type
                winding_scheme = virtual_winding_window.winding_scheme

                num = winding.winding_number

                # Check if the coil is round or rectangular
                if conductor_type == ConductorType.RectangularSolid:    
                    # Now check for each possible winding scheme 
                    if winding_scheme == WindingScheme.Full:
                        # Full window conductor
                        self.p_conductor[num].append([
                            left_bound, 
                            bot_bound, 
                            0, 
                            self.mesh_data.c_conductor[num]])
                        self.p_conductor[num].append([
                            right_bound, 
                            bot_bound, 
                            0, 
                            self.mesh_data.c_conductor[num]])
                        self.p_conductor[num].append([
                            left_bound, 
                            top_bound, 
                            0, 
                            self.mesh_data.c_conductor[num]])
                        self.p_conductor[num].append([
                            right_bound, 
                            top_bound, 
                            0, 
                            self.mesh_data.c_conductor[num]])
                    elif winding_scheme == WindingScheme.FoilVertical:
                        # TODO Add check if turns do not fit in winding window
                        # Foil conductors where each conductor is very high and the conductors are expanding in the x-direction
                        if virtual_winding_window.wrap_para == WrapParaType.FixedThickness:
                            # Wrap defined number of turns and chosen thickness
                            for i in range(turns):
                                # CHECK if right bound is reached
                                if (left_bound + (i + 1) * winding.thickness +
                                    i * self.insulation.inner_winding_insulations[num]) <= right_bound:
                                    # Foils
                                    self.p_conductor[num].append([
                                        left_bound + i * winding.thickness + i * self.insulation.inner_winding_insulations[num],
                                        bot_bound, 
                                        0, 
                                        self.mesh_data.c_conductor[num]])
                                    self.p_conductor[num].append([
                                        left_bound + (i + 1) * winding.thickness + i * self.insulation.inner_winding_insulations[num], 
                                        bot_bound, 
                                        0,
                                        self.mesh_data.c_conductor[num]])
                                    self.p_conductor[num].append([
                                        left_bound + i * winding.thickness + i * self.insulation.inner_winding_insulations[num],
                                        top_bound, 
                                        0, 
                                        self.mesh_data.c_conductor[num]])
                                    self.p_conductor[num].append([
                                        left_bound + (i + 1) * winding.thickness + i * self.insulation.inner_winding_insulations[num], 
                                        top_bound, 
                                        0,
                                        self.mesh_data.c_conductor[num]])
                        elif virtual_winding_window.wrap_para == WrapParaType.Interpolate:
                            # Fill the allowed space in the Winding Window with a chosen number of turns
                            x_interpol = np.linspace(left_bound, right_bound + self.insulation.inner_winding_insulations[num],
                                                        turns + 1)
                            for i in range(turns):
                                # Foils
                                self.p_conductor[num].append([
                                    x_interpol[i], 
                                    bot_bound, 
                                    0, 
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    x_interpol[i + 1] - self.insulation.inner_winding_insulations[num], 
                                    bot_bound, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    x_interpol[i],
                                    top_bound, 
                                    0, 
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    x_interpol[i + 1] - self.insulation.inner_winding_insulations[num], 
                                    top_bound, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                        else:
                            raise Exception(f"Unknown wrap para type {virtual_winding_window.wrap_para}")
                    elif winding_scheme == WindingScheme.FoilHorizontal:
                        # Foil conductors where each conductor is very long and the conductors are expanding the y-direction
                        # Stack defined number of turns and chosen thickness
                        for i in range(turns):
                            # CHECK if top bound is reached
                            if (bot_bound + (i + 1) * winding.thickness +
                                i * self.insulation.inner_winding_insulations[num]) <= top_bound:
                                # stacking from the ground
                                self.p_conductor[num].append([
                                    left_bound, 
                                    bot_bound + i * winding.thickness + i * self.insulation.inner_winding_insulations[num], 
                                    0, 
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    right_bound,
                                    bot_bound + i * winding.thickness + i * self.insulation.inner_winding_insulations[num],
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    left_bound,
                                    bot_bound + (i + 1) * winding.thickness + i * self.insulation.inner_winding_insulations[num], 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    right_bound,
                                    bot_bound + (i + 1) * winding.thickness + i * self.insulation.inner_winding_insulations[num],
                                    0,
                                    self.mesh_data.c_conductor[num]])      
                    else:
                        raise Exception(f"Winding scheme {winding_scheme.name} is not implemented.")
                elif conductor_type == ConductorType.RoundSolid or conductor_type == ConductorType.RoundLitz:
                    # Since round conductors have no winding scheme check for each conductor_arrangement
                    conductor_arrangement = winding.conductor_arrangement

                    if conductor_arrangement == ConductorArrangement.Square:
                        y = bot_bound + winding.conductor_radius
                        x = left_bound + winding.conductor_radius
                        i = 0
                        # Case n_conductors higher that "allowed" is missing
                        while x < right_bound - winding.conductor_radius and i < turns:
                            while y < top_bound - winding.conductor_radius and i < turns:
                                self.p_conductor[num].append([
                                    x, 
                                    y, 
                                    0, 
                                    self.mesh_data.c_center_conductor[num]])
                                self.p_conductor[num].append([
                                    x - winding.conductor_radius, 
                                    y, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    x, 
                                    y + winding.conductor_radius, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append(
                                    [x + winding.conductor_radius, 
                                    y, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    x, 
                                    y - winding.conductor_radius, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                i += 1
                                y += winding.conductor_radius * 2 + self.insulation.inner_winding_insulations[num]  # one step from left to right
                            x += winding.conductor_radius * 2 + self.insulation.inner_winding_insulations[num]  # from left to top
                            y = bot_bound + winding.conductor_radius
                    elif conductor_arrangement == ConductorArrangement.Hexagonal:
                        y = bot_bound + winding.conductor_radius
                        x = left_bound + winding.conductor_radius
                        i = 0
                        base_line = True
                        # Case n_conductors higher that "allowed" is missing
                        while x < right_bound - winding.conductor_radius \
                                and i < turns:
                            while y < top_bound - winding.conductor_radius and \
                                    i < turns:
                                self.p_conductor[num].append([
                                    x, 
                                    y, 
                                    0, 
                                    self.mesh_data.c_center_conductor[num]])
                                self.p_conductor[num].append([
                                    x - winding.conductor_radius, 
                                    y, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    x, 
                                    y + winding.conductor_radius, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    x + winding.conductor_radius, 
                                    y, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    x, 
                                    y - winding.conductor_radius, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                i += 1
                                y += winding.conductor_radius * 2 + \
                                        self.insulation.inner_winding_insulations[
                                            num]  # from bottom to top
                            x += 2 * np.cos(np.pi / 6) * (
                                    winding.conductor_radius +
                                    self.insulation.inner_winding_insulations[num] / 2)
                            # * np.sqrt(2 / 3 * np.pi / np.sqrt(3))  # one step from left to right
                            # depending on what line, hexa scheme starts shifted
                            # reset y to "new" bottom
                            base_line = (not base_line)
                            if base_line:
                                y = bot_bound + winding.conductor_radius
                            else:
                                y = bot_bound + 2 * winding.conductor_radius + \
                                    self.insulation.inner_winding_insulations[
                                        num] / 2
                    elif conductor_arrangement == ConductorArrangement.SquareFullWidth:
                        y = bot_bound + winding.conductor_radius
                        x = left_bound + winding.conductor_radius
                        i = 0
                        # Case n_conductors higher that "allowed" is missing
                        while y < top_bound - winding.conductor_radius \
                                and i < turns:
                            while x < right_bound - winding.conductor_radius \
                                    and i < turns:
                                self.p_conductor[num].append([
                                    x, 
                                    y, 
                                    0, 
                                    self.mesh_data.c_center_conductor[num]])
                                self.p_conductor[num].append([
                                    x - winding.conductor_radius, 
                                    y, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    x,
                                    y + winding.conductor_radius, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    x + winding.conductor_radius, 
                                    y, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                self.p_conductor[num].append([
                                    x, 
                                    y - winding.conductor_radius, 
                                    0,
                                    self.mesh_data.c_conductor[num]])
                                i += 1
                                x += winding.conductor_radius * 2 + \
                                        self.insulation.inner_winding_insulations[
                                            num]  # from left to top
                            y += winding.conductor_radius * 2 + \
                                    self.insulation.inner_winding_insulations[
                                        num]  # one step from left to right
                            x = left_bound + winding.conductor_radius  # always the same
                    else:
                        raise Exception(f"Conductor arrangement {conductor_arrangement} is not implemented.")
                else:
                    raise Exception(f"Conductor type {winding.conductor_type.name} is not implemented.")
            else:
                raise Exception(f"Unknown winding type {virtual_winding_window.winding_type.name}")

        # Checking the Conductors
        for vww in self.virtual_winding_windows:
            for index, winding in enumerate(vww.windings):
                num = winding.winding_number

                # Convert to numpy
                # Check if all Conductors could be resolved
                self.p_conductor[num] = np.asarray(self.p_conductor[num])

                # TODO:CHECKS for rect. conductors
                """ CHECK: rectangle conductors with 4 points
                if self.component.windings[num].conductor_type == "full" or 
                        self.component.windings[num].conductor_type == "stacked" or \
                        self.component.windings[num].conductor_type == "foil":
                    if int(self.p_conductor[num].shape[0]/4) < self.component.windings[num].turns:
                        warnings.warn("Too many turns that do not fit in the winding window.")
                        # self.component.windings[num].turns = int(self.p_conductor[num].shape[0]/4)
                        self.component.valid = None
                """

                # CHECK: round conductors with 5 points
                if winding.conductor_type in [ConductorType.RoundSolid, ConductorType.RoundLitz]:
                    if int(self.p_conductor[num].shape[0] / 5) < vww.turns[index]:
                        # Warning: warnings.warn("Too many turns that do not fit in the winding window.")
                        # Correct: self.component.windings[num].turns = int(self.p_conductor[num].shape[0]/5)
                        # TODO: break, but remove warning. valid bit should be set to False
                        #  Code must go to the next parameter-iteration step for geometric sweep
                        self.valid = False
                        # TODO Tell the user which winding window
                        raise Exception(f"Too many turns that do not fit in the winding window {str(vww)}")

                # Region for Boundary Condition
                self.p_region_bound[0][:] = [-self.r_outer * self.mesh_data.padding,
                                            -(self.core.window_h / 2 + self.core.core_inner_diameter / 4)
                                            * self.mesh_data.padding,
                                            0,
                                            self.mesh_data.c_core * self.mesh_data.padding]
                self.p_region_bound[1][:] = [self.r_outer * self.mesh_data.padding,
                                            -(self.core.window_h / 2 + self.core.core_inner_diameter / 4)
                                            * self.mesh_data.padding,
                                            0,
                                            self.mesh_data.c_core * self.mesh_data.padding]
                self.p_region_bound[2][:] = [-self.r_outer * self.mesh_data.padding,
                                            (self.core.window_h / 2 + self.core.core_inner_diameter / 4)
                                            * self.mesh_data.padding,
                                            0,
                                            self.mesh_data.c_core * self.mesh_data.padding]
                self.p_region_bound[3][:] = [self.r_outer * self.mesh_data.padding,
                                            (self.core.window_h / 2 + self.core.core_inner_diameter / 4)
                                            * self.mesh_data.padding,
                                            0,
                                            self.mesh_data.c_core * self.mesh_data.padding]

    def draw_insulations(self):
        """
        IMPORTANT
        Because the distance from the core to the winding is set by
        iso.core_cond, a delta, which is used in order for no overlapping lines will cause
        the "real" insulation to be slightly smaller than set by the user.
        """

        window_h = self.core.window_h
        iso = self.insulation
        mesh_data = self.mesh_data

        # Since there are many cases in which alternating conductors would lead to slightly different
        # mesh densities a simplification is made: Just use the lowest mesh density to be safe all the time.
        mesh_density_to_winding = min(mesh_data.c_conductor)

        mesh_density_to_core = mesh_data.c_window

        # Using the delta the lines and points from the insulation and the core/windings are not overlapping
        # which makes creating the mesh more simpler
        # Insulation between winding and core
        insulation_delta = self.insulation.insulation_delta

        self.p_iso_core = [] # Order: Left, Top, Right, Bot
        self.p_iso_pri_sec = []

        if self.component_type == ComponentType.IntegratedTransformer:
            # TODO implement for integrated_transformers
            # TODO Change back to warnings?
            print("Insulations are not set because they are not implemented for integrated transformers.")
        else:
            # Useful points for insulation creation
            left_x = self.core.core_inner_diameter / 2 + insulation_delta
            top_y = window_h / 2 - insulation_delta
            right_x = self.r_inner - insulation_delta
            bot_y = -window_h / 2 + insulation_delta

            # Useful lengths
            left_iso_width = iso.core_cond[2] - insulation_delta - insulation_delta
            top_iso_height = iso.core_cond[0] - insulation_delta - insulation_delta
            right_iso_width = iso.core_cond[3] - insulation_delta - insulation_delta
            bot_iso_height = iso.core_cond[1] - insulation_delta - insulation_delta

            # Core to Pri insulation
            iso_core_left = [
                [
                    left_x,
                    top_y - top_iso_height - insulation_delta,
                    0,
                    mesh_density_to_core
                ],
                [
                    left_x + left_iso_width,
                    top_y - top_iso_height - insulation_delta,
                    0,
                    mesh_density_to_winding
                ],
                [
                    left_x + left_iso_width,
                    bot_y + bot_iso_height + insulation_delta,
                    0,
                    mesh_density_to_winding
                ],
                [
                    left_x,
                    bot_y + bot_iso_height + insulation_delta,
                    0,
                    mesh_density_to_core
                ]
            ]
            iso_core_top = [
                [
                    left_x,
                    top_y,
                    0,
                    mesh_density_to_core
                ],
                [
                    right_x,
                    top_y,
                    0,
                    mesh_density_to_core
                ],
                [
                    right_x,
                    top_y - top_iso_height,
                    0,
                    mesh_density_to_winding
                ],
                [
                    left_x,
                    top_y - top_iso_height,
                    0,
                    mesh_density_to_winding
                ]
            ]
            iso_core_right = [
                [
                    right_x - right_iso_width,
                    top_y - top_iso_height - insulation_delta,
                    0,
                    mesh_density_to_winding
                ],
                [
                    right_x,
                    top_y - top_iso_height - insulation_delta,
                    0,
                    mesh_density_to_core
                ],
                [
                    right_x,
                    bot_y + bot_iso_height + insulation_delta,
                    0,
                    mesh_density_to_core
                ],
                [
                    right_x - right_iso_width,
                    bot_y + bot_iso_height + insulation_delta,
                    0,
                    mesh_density_to_winding
                ]
            ]
            iso_core_bot = [
                [
                    left_x,
                    bot_y + bot_iso_height,
                    0,
                    mesh_density_to_winding
                ],
                [
                    right_x,
                    bot_y + bot_iso_height,
                    0,
                    mesh_density_to_winding
                ],
                [
                    right_x,
                    bot_y,
                    0,
                    mesh_density_to_core
                ],
                [
                    left_x,
                    bot_y,
                    0,
                    mesh_density_to_core
                ]
            ]

            self.p_iso_core = [iso_core_left, iso_core_top, iso_core_right, iso_core_bot]

            """
            Currently there are only core to vww insulations
            # Now create insulations for interleaved windings
            self.p_iso_interleaved = []
            for vww in self.virtual_winding_windows:
                if vww.winding_type == WindingType.Interleaved:
                    if vww.winding_scheme == InterleavedWindingScheme.Bifilar:
                        print("No insulations for bifilar winding scheme")
                    elif vww.winding_scheme == InterleavedWindingScheme.HorizontalAlternating:
                        winding_0 = vww.windings[0]
                        winding_1 = vww.windings[1]
                        turns0 = vww.turns[0]
                        turns1 = vww.turns[1]
                        current_x = vww.left_bound + 2 * winding_0.conductor_radius

                        mesh_density_left_side = 0
                        mesh_density_right_side = 0
                        if turns0 > turns1:
                            mesh_density_left_side = self.mesh_data.c_conductor[0]
                            mesh_density_right_side = self.mesh_data.c_conductor[1]
                        else:
                            mesh_density_left_side = self.mesh_data.c_conductor[1]
                            mesh_density_right_side = self.mesh_data.c_conductor[0]

                        current_iso = []
                        for index in range(self.top_window_iso_counter-1):
                            current_iso.append([
                                [
                                    current_x + insulation_delta,
                                    top_y - top_iso_height - insulation_delta,
                                    0,
                                    mesh_density_left_side
                                ],
                                [
                                    current_x + iso.vww_insulation - insulation_delta,
                                    top_y - top_iso_height - insulation_delta,
                                    0,
                                    mesh_density_right_side
                                ],
                                [
                                    current_x + iso.vww_insulation - insulation_delta,
                                    bot_y + bot_iso_height + insulation_delta,
                                    0,
                                    mesh_density_right_side
                                ],
                                [
                                    current_x + insulation_delta,
                                    bot_y + bot_iso_height + insulation_delta,
                                    0,
                                    mesh_density_left_side
                                ]
                            ])
                            # The sec winding can start first when it has a higher number of turns
                            # col_cond
                            if index % 2 == self.col_cond_start:
                                current_x += iso.vww_insulation + 2 * winding_1.conductor_radius
                            else:
                                current_x += iso.vww_insulation + 2 * winding_0.conductor_radius
                    elif vww.winding_scheme == InterleavedWindingScheme.VerticalAlternating:
                        print("No insulations for vertical alternating winding scheme")
                    elif vww.winding_scheme == InterleavedWindingScheme.VerticalStacked:
                        print("No insulations for vertical stacked winding scheme")
                    else:
                        raise Exception(f"Unknown interleaved winding scheme {vww.winding_scheme.name}")
                else:
                    # TODO Own handler for warnings?
                    print("No insulations for winding type {vww.winding_type.name}")
            """

    def draw_model(self):
        self.draw_outer()
        self.draw_window()
        self.draw_air_gaps()
        self.draw_conductors()
        self.draw_insulations()
