from enum import IntEnum

class WindingWindowSplit(IntEnum):
    """Determines how many virtual winding windowes are created by the winding window. Used in Winding window class.
    """
    NoSplit = 1 
    """Virtual winding window same size as winding window
    """
    HorizontalSplit = 2
    """Splits winding window in two virtual winding windows which are separated by a horizontal line
    """
    VerticalSplit = 3
    """Splits winding window in two virtual winding windows which are separated by a vertical line
    """
    HorizontalAndVerticalSplit = 4
    """Splits winding window in four virtual winding windows separated by a horizontal and vertical line
    """

class ComponentType(IntEnum):
    """Sets the component type for the whole simulation. Needs to be given to the MagneticComponent on creation.
    """
    Inductor = 1
    Transformer = 2
    IntegratedTransformer = 3

class AirGapMethod(IntEnum):
    """Sets the method how the air gap position (vertical) is set.
    Used in AirGaps class.
    """
    Center = 1
    """Only valid for one air gap. This air gap will always be placed in the middle (vertically)
    """
    Percent = 2
    """A value between 0 and 100 will determine the vertical position.
    """
    Manually = 3
    """The vertical position needs to be given manually. In metres.
    """

class AirGapLegPosition(IntEnum):
    """Sets the core at which the air gap will be added. Currently only CenterLeg is supported.
    Used when adding an air gap to the model.
    """
    LeftLeg = -1
    """Air gap in left leg.
    """
    CenterLeg = 0
    """Air gap in center leg.
    """
    RightLeg = 1
    """Air gap in right leg.
    """

class WindingType(IntEnum):
    """Internally used in VirtualWindingWindow class. 
    """
    Interleaved = 1
    Single = 2

class WindingScheme(IntEnum):
    """Used when adding a single winding to the virtual winding window. Only used with an
    rectangular solid conductor.
    """
    Full = 1
    """The whole virtual winding window is filled with one conductor.
    """
    SquareFullWidth = 2
    """Not implemented. Foils are drawn along x-axis first and then along y-axis.
    """
    FoilVertical = 3
    """Foils are very tall (y-axis) and drawn along x-axis.
    """
    FoilHorizontal = 4
    """Foils are very wide (x-axis) and drawn along y-axis.
    """

class InterleavedWindingScheme(IntEnum):
    """Used when adding an interleaved winding to the virtual winding window.
    """
    Bifilar = 1
    """Not implemented.
    """
    VerticalAlternating = 2
    """Not implemented. First and second winding are interleaved vertically (rows)
    """
    HorizontalAlternating = 3
    """First and second winding are interleaved horizontally (cols)
    """
    VerticalStacked = 4
    """First winding is drawn bottom to top. Second winding is drawn top to bottom.
    """

class ConductorArrangement(IntEnum):
    """Set for round conductors when having a single conductor in the virtual winding window.
    """
    Square = 1
    """Turns are drawn in a grid (perfectly aligned). First drawn in y-direction then x-direction.
    """
    SquareFullWidth = 2
    """Turns are drawn in a grid. First drawn in x-direction then in y-direction .
    """
    Hexagonal = 3
    """Turns are drawn more compact. The turn of the next line slides in the empty space between two turns of the previous line.
    Frist drawn in y-direction then x-direction.
    """

class ConductorType(IntEnum):
    """Sets the type of the conductor.
    """
    RoundSolid = 1
    RoundLitz = 2
    RectangularSolid = 3

class WrapParaType(IntEnum):
    """Sets the wrap para type. Only necessary for a single conductor in a virtual winding window and a FoilVertical winding scheme.
    """
    FixedThickness = 1
    """The foils have a fixed thickness given when creating the conductor. The virtual winding window
    may not be fully occupied.
    """
    Interpolate = 2
    """The foils will have a dynamic thickness. The thickness is chosen in such way that the virtual winding window is fully occupied.
    The thickness parameter when creating the conductor is irrelevant.
    """

class Conductivity(IntEnum):
    """Sets the conductivity of the conductor.
    """
    Copper = 1
    Aluminium = 2

class LossApproach(IntEnum):
    """Sets the way how losses will be calculated.
    """
    Steinmetz = 1
    LossAngle = 2

class PermeabilityType(IntEnum):
    """Sets the way how permeability data is recieved.  
    """
    FixedLossAngle = 1
    RealValue = 2
    FromData = 3

class ExcitationMeshingType(IntEnum):
    """When running an excitation it is possible to not mesh at every frequency.
    """
    MeshOnlyLowestFrequency = 1
    MeshOnlyHighestFrequency = 2
    MeshEachFrequency = 3