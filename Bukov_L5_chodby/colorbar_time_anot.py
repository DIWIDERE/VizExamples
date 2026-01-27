from paraview.simple import *

def start_cue(self):
    pass

def tick(self):
    # Get the animation time
    animationTime = self.GetClockTime()  # Use cue's own clock time
    renderView1 = GetActiveViewOrCreate("RenderView")

    display_colorbar(animationTime, renderView1)
    display_colorbar_boreholes(animationTime, renderView1)

    move_bill_01(animationTime, renderView1)  # ZK5-1S
    move_bill_02(animationTime, renderView1)  # ZK5-1J
    Render()  # Important in scripted animation to force update

def display_colorbar(t, view):
    # Get the source and view
    pressure_clip = FindSource("pressure_clip")
    view = GetActiveViewOrCreate("RenderView")

    # Set up display properties and color mapping
    rep = GetDisplayProperties(pressure_clip, view=view)
    ColorBy(rep, ("CELLS", "pressure_p0"))

    # Get LUT and scalar bar
    lut = GetColorTransferFunction("pressure_p0")
    scalarBar = GetScalarBar(lut, view)

    # Force color scale to fixed range
    lut.RescaleTransferFunction(-50, 150)

    t0 = 59250
    t1 = 82000
    # Opacity fade-in and fade-out (1 sec = 1000 ms)
    fade_dt = 500
    fade_in_start = t0
    fade_in_end = t0 + fade_dt
    fade_out_start = t1 - fade_dt
    fade_out_end = t1
    opacity = interpolate_opacity(t, fade_in_start, fade_in_end, fade_out_start, fade_out_end)

    # Toggle visibility based on animation time
    if opacity > 0:
        scalarBar.Visibility = 1
        rep.SetScalarBarVisibility(view, True)
    else:
        scalarBar.Visibility = 0
        rep.SetScalarBarVisibility(view, False)

    # Apply fading components
    # BarOpacity is missing in current API !
    scalarBar.TitleOpacity = 1
    scalarBar.LabelOpacity = 1
    # scalarBar.TitleOpacity = opacity
    # scalarBar.LabelOpacity = opacity
    # scalarBar.BarOpacity = opacity

    scalarBar.Modified()
  
def display_colorbar_boreholes(t, view):
    # Get the source and view
    boreholes = FindSource("boreholes_opt_cfg_1.vtk")
    view = GetActiveViewOrCreate("RenderView")

    # Set up display properties and color mapping
    rep = GetDisplayProperties(boreholes, view=view)
    ColorBy(rep, ("POINTS", "index"))

    # Get LUT and scalar bar
    lut = GetColorTransferFunction("index")
    scalarBar = GetScalarBar(lut, view)

    # Force color scale to fixed range
    # lut.RescaleTransferFunction(-50, 150)

    t0 = 32000
    t1 = 45000
    # Opacity fade-in and fade-out (1 sec = 1000 ms)
    fade_dt = 500
    fade_in_start = t0
    fade_in_end = t0 + fade_dt
    fade_out_start = t1 - fade_dt
    fade_out_end = t1
    opacity = interpolate_opacity(t, fade_in_start, fade_in_end, fade_out_start, fade_out_end)

    # Toggle visibility based on animation time
    if opacity > 0:
        scalarBar.Visibility = 1
        rep.SetScalarBarVisibility(view, True)
    else:
        scalarBar.Visibility = 0
        rep.SetScalarBarVisibility(view, False)

    # Apply fading components
    # BarOpacity is missing in current API !
    scalarBar.TitleOpacity = 1
    scalarBar.LabelOpacity = 1
    # scalarBar.TitleOpacity = opacity
    # scalarBar.LabelOpacity = opacity
    # scalarBar.BarOpacity = opacity

    scalarBar.Modified()

def move_bill_01(t, view):
    p0 = [-5, 19, 2.0]
    p1 = [-9.0, 22.6, 2.0]
    t0 = 60000
    t1 = 85000 # 70400 #66933

    pos = interpolate_position(p0, p1, t, t0, t1)

    # Opacity fade-in and fade-out (1 sec = 1000 ms)
    fade_dt = 1000
    fade_in_start = t0 -fade_dt
    fade_in_end = t0
    fade_out_start = t1 - 3*fade_dt
    fade_out_end = t1
    opacity = interpolate_opacity(t, fade_in_start, fade_in_end, fade_out_start, fade_out_end)

    print("ZK5-1S", opacity, pos)
    billboard = FindSource("ZK5-1S")
    rep = GetDisplayProperties(billboard, view=view)
    rep.BillboardPosition = pos
    rep.Opacity = opacity

def move_bill_02(t, view):
    p0 = [15, 4.0, 2.0]
    p1 = [18, 14, 2.0]
    t0 = 70400
    t1 = 85000

    pos = interpolate_position(p0, p1, t, t0, t1)

    # Opacity fade-in and fade-out (1 sec = 1000 ms)
    fade_dt = 1000
    fade_in_start = t0 - fade_dt
    fade_in_end = t0
    fade_out_start = t1 - 3*fade_dt
    fade_out_end = t1
    opacity = interpolate_opacity(t, fade_in_start, fade_in_end, fade_out_start, fade_out_end)

    print("ZK5-1J", opacity, pos)
    billboard = FindSource("ZK5-1J")
    rep = GetDisplayProperties(billboard, view=view)
    rep.BillboardPosition = pos
    rep.Opacity = opacity

def interpolate_position(p0, p1, t, t0, t1):
    """
    Linearly interpolates between two 3D points p0 and p1 over time [t0, t1].

    Parameters:
        p0 (list of float): Start position [x0, y0, z0]
        p1 (list of float): End position [x1, y1, z1]
        t (float): Current time
        t0 (float): Start time
        t1 (float): End time

    Returns:
        list of float: Interpolated position at time t
    """
    if t <= t0:
        return p0
    elif t >= t1:
        return p1
    else:
        f = (t - t0) / (t1 - t0)
        return [p0[i] + f * (p1[i] - p0[i]) for i in range(3)]

def interpolate_opacity(t, fade_in_start, fade_in_end, fade_out_start, fade_out_end):
    """
    Returns opacity value based on fade-in and fade-out time windows.

    - Returns 0 before fade-in start and after fade-out end.
    - Linearly fades in from 0 to 1 between fade_in_start and fade_in_end.
    - Linearly fades out from 1 to 0 between fade_out_start and fade_out_end.
    - Full opacity (1.0) in between.

    Parameters:
        t (float): Current time
        fade_in_start, fade_in_end (float): Fade-in time range
        fade_out_start, fade_out_end (float): Fade-out time range
    """
    if t < fade_in_start:
        return 0.0
    elif fade_in_start <= t <= fade_in_end:
        return (t - fade_in_start) / (fade_in_end - fade_in_start)
    elif fade_out_start <= t <= fade_out_end:
        return 1.0 - (t - fade_out_start) / (fade_out_end - fade_out_start)
    elif t > fade_out_end:
        return 0.0
    else:
        return 1.0

def end_cue(self):
    pass
