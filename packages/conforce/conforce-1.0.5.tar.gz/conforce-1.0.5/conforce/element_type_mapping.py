"""
This module provides mappings from element types to supported element types.

**Example**

The deformation gradient of a triangular plane stress element should be computed.
This element type CPS3 is not supported.

>>> from conforce import cf_c
>>> not_supported_element_type = "CPS3"
>>> X_at_nodes = [[
...     [0, 0],
...     [1, 0],
...     [0, 1],
... ]]
>>> U_at_nodes = [[
...     [0, 0],
...     [0.1, 0],
...     [0, 0],
... ]]

However, CPE3 can be replaced by a similar triangular plane strain element.
Of course, this is an approximation that neglects the out-of-plane strain of the CPE3 element.

>>> supported_similar_element_type = map_abaqus_element_type_to_supported_element_type[not_supported_element_type]
>>> supported_similar_element_type
'CPE3'

The deformation gradient is computed using the supported element type.

>>> cf_c.compute_F(
...     X_at_nodes=X_at_nodes,
...     U_at_nodes=U_at_nodes,
...     element_type=supported_similar_element_type
... )
array([[[[1.1, 0. ],
         [0. , 1. ]]]])

"""

map_abaqus_element_type_to_supported_element_type = dict()
"""
mapping of abaqus element types to supported element types.
The element types must have:

 - the same shape,
 - the same dimension (2D or 3D),
 - the same number of nodes at the same positions,
 - the same number of integration points at the same positions
 - the same integration weights
 
.. note::
    The mapping might make assumptions and simplifications.

    One simplification is, that the out-of-plane strain of plane stress elements is negligible,
    because Abaqus does not compute the out-of-plane strain.
    Consequently, a correct implementation for plane stress elements is not possible
    and the plane stress elements are instead treated as plane strain elements.
"""

map_abaqus_element_type_to_supported_element_type.update({
    # not compatible: "CAX3": "CPE3",
    # not compatible: "CAX3H": "CPE3",
    # not compatible: "CAX4": "CPE4",
    # not compatible: "CAX4H": "CPE4",
    # not compatible: "CAX4I": "CPE4",
    # not compatible: "CAX4IH": "CPE4",
    # not compatible: "CAX4R": "CPE4R",
    # not compatible: "CAX4RH": "CPE4R",
    # not compatible: "CAX6": "CPE6",
    # not compatible: "CAX6H": "CPE6",
    # not compatible: "CAX6M": "CPE6",
    # not compatible: "CAX6MH": "CPE6",
    # not compatible: "CAX8": "CPE8",
    # not compatible: "CAX8H": "CPE8",
    # not compatible: "CAX8R": "CPE8R",
    # not compatible: "CAX8RH": "CPE8R",
    "CPE3": "CPE3",
    "CPE3H": "CPE3",
    "CPE4": "CPE4",
    "CPE4H": "CPE4",
    "CPE4I": "CPE4",
    "CPE4IH": "CPE4",
    "CPE4R": "CPE4R",
    "CPE4RH": "CPE4R",
    "CPE6": "CPE6",
    "CPE6H": "CPE6",
    # not compatible: "CPE6M": "CPE6",
    # not compatible: "CPE6MH": "CPE6",
    "CPE8": "CPE8",
    "CPE8H": "CPE8",
    "CPE8R": "CPE8R",
    "CPE8RH": "CPE8R",
    "CPS3": "CPE3",
    "CPS4": "CPE4",
    "CPS4I": "CPE4",
    "CPS4R": "CPE4R",
    "CPS6": "CPE6",
    # not compatible: "CPS6M": "CPE6",
    "CPS8": "CPE8",
    "CPS8R": "CPE8R",
    # not compatible: "CPEG3": "CPE3",
    # not compatible: "CPEG3H": "CPE3",
    # not compatible: "CPEG4": "CPE4",
    # not compatible: "CPEG4H": "CPE4",
    # not compatible: "CPEG4I": "CPE4",
    # not compatible: "CPEG4IH": "CPE4",
    # not compatible: "CPEG4R": "CPE4R",
    # not compatible: "CPEG4RH": "CPE4R",
    # not compatible: "CPEG6": "CPE6",
    # not compatible: "CPEG6H": "CPE6",
    # not compatible: "CPEG6M": "CPE6",
    # not compatible: "CPEG6MH": "CPE6",
    # not compatible: "CPEG8": "CPE8",
    # not compatible: "CPEG8H": "CPE8",
    # not compatible: "CPEG8R": "CPE8R",
    # not compatible: "CPEG8RH": "CPE8R",
    "C3D4": "C3D4",
    "C3D4H": "C3D4",
    "C3D6": "C3D6",
    "C3D6H": "C3D6",
    "C3D8": "C3D8",
    "C3D8H": "C3D8",
    "C3D8I": "C3D8",
    "C3D8IH": "C3D8",
    "C3D8R": "C3D8R",
    "C3D8RH": "C3D8R",
    "C3D10": "C3D10",
    "C3D10H": "C3D10",
    # not compatible: "C3D10I": "C3D10",
    # not compatible: "C3D10M": "C3D10",
    # not compatible: "C3D10MH": "C3D10",
    "C3D15": "C3D15",
    "C3D15H": "C3D15",
    "C3D20": "C3D20",
    "C3D20H": "C3D20",
    "C3D20R": "C3D20R",
    "C3D20RH": "C3D20R"
})
