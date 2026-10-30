Home renders in Blender (Cycles)

1. Install Blender 4.2 LTS (free): https://www.blender.org/download/lts/4-2/  or  winget install BlenderFoundation.Blender.LTS.4.2
2. In this folder, run:
   "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe" -b -P render_house.py -- --shots front,corner,back,firepit,falls,porch,aerial --res 3840 --samples 1024 --save
3. Renders land in renders\ ; house.blend is saved for opening in Blender.

Options: --hour 16.5 (sun time, 7 to 19.5), --exposure -1.2, --res 1920 for quick tests, --cpu to skip the GPU.
