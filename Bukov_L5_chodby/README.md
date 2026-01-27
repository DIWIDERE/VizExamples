# Endorse experiment design clip

## Paraview Animation using Time Manager

- Animation time axis is saved as Paraview state file
- Most important note: ** When creating new animation, think twice about total time and frame rate (number of frames).**
  - At the header of the time axis, set the start time and end time of your animation time. Use locker to lock these values
    and never touch it again. If you change these (e.g. you would like to add additional time interval to you animation),
    all time properties you defined for the animated objects will be interpolated to new time scale which is most probably something you do not want.
  - Use advanced properties of `Time Manager`, in `Animations` tree you can edit `TimeKeeper`.
    Select `Variable Time`.
    Use column `Time` to create time marks in your own arbitrary time axis (here we understand it as milliseconds).
    Using column `Value` you can interpolate the data time axis onto your created time scale.
    Therefore you control when your data animation starts/ends and its "speed" in your animation time axis.
- Some objects have `opacity` parameter in Time Manager, however it does not work (`Text`, `AnnotateTime`).
- Use `Python` object in Time Manager for using python code to control stuff that cannot be controled directly.
  - File `colorbar_time_anot.py` includes code that must be inserted into `Python` editting window in Paraview
    (This window is so user unfriendly that it is necessary to edit python code outside of Paraview).
    Currently the file controls:
    - `Visibility` of colorbar (scalarbar) of the data (Unfortunately the API does not have access to opacity of all components
      of scalarbar, so it cannost be used for fade in/fade out).
    - `Opacity` of text (not 3D text).
    - Interpolation of position of text (we use Billboard type of Text objects)
    - Debugging: Use `print` and run Paraview from shell where you can see the output.
    - Debugging: When getting `'Python' module_from_string failed to load` error, beware of syntax bugs
      (it is very sensitive to white characters -- pay attention to tabs/spaces/comments -- here comes the necessity to use editor outside of Paraview!)

## TODO:
- DVC source data:
  - `fotogrametrie/PVP_Bukov_II_Model_a_data_2025.obj`
  - `fotogrametrie/PVP Bukov II k 08-2024 bez stufu, srafa.png`
  - `fotogrametrie/ZK5-1J_PTG_SJTSK.png`
  - `results/boreholes_opt_cfg_0.vtk`
  - `results/boreholes_opt_cfg_1.vtk`
  - `results/output/mechanics.pvd` + vtu's
  - `results/output/flow.pvd` + vtu's


