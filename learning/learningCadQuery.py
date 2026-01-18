import cadquery as cq

# 1. Definition of parameters

# Basic parameters
length = 100
width = 60
height = 40
thickness = 2

# Cable hole
cable_hole_diameter = 10
cable_hole_case_height = 20

# Cover and lip
lip_height = 3 # How far the lid sticks into the actual enclosure
tolerance = 0.2 # Crucial! Makes the lid slightly smaller so it actually fits

# 2. Building the box and cover
# BASE ENCLOSURE: Start on the XY plane, draw a rectangle, then extrude it
enclosure = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(height)
)

# 3. Hollow it out
# Select the top face (">Z") and "shell" it
# A negative thickness shells towards the inside
enclosure = enclosure.faces(">Z").shell(-thickness)

# 4. Add a hole for a cable on the sidee
# We select the front face (">Y"), draw a circle, and cut through
enclosure = (
    enclosure.faces(">X")
    .workplane()
    .center(0, cable_hole_case_height)
    .circle(cable_hole_diameter / 2)
    .cutBlind(-thickness)
)

#5. Build the cover

# COVER: Start on the XY plane, draw a rectangle, then extrude it
cover = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(thickness)
)

# Select the top face (">Z") and create a new workplane there
cover = cover.faces("<Z").workplane()

# Draw the lip
# The box walls are 'thickness' wide (default 2mm)
# So the inside of the box is (length - 2*thickness) wide.
# We subtract 'tolerance' so it isn't a "tight" friction fit.
lip_length = length - (2 * thickness) - (2 * tolerance)
lip_width = width - (2 * thickness) - (2 * tolerance)

cover = (
    cover.rect(lip_length, lip_width)
    .extrude(lip_height)
)

# 5. Export to STL
cq.exporters.export(enclosure, "learning/enclosure_learning_preview.stl")
cq.exporters.export(cover, "learning/cover_learning_preview.stl")

print("Sample enclosure with a cover generated succcessfully!")
