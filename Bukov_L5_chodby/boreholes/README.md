# Boreholes and labels

Setup to create a ParaView scene that reads from a VTM/VTP file the borehole geometry and field data that is used to create labels.

1. Open ParaView menu Tools->Manage Plugins, select "Load New..." and choose "pvDataLabelRepresentation.xml". This creates a new representation "Labels". Maybe the restart of ParaView application will be necessary.
2. Open menu View->Python Shell, select "Run Script" and choose "boreholes_paraview_annotation.py". The script loads the VTK multiblock data and creates a source for borehole labels.