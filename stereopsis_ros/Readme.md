# stereopsis-ros

Another aspect of project stereopsis, drivers and such.

## Notes to for setup

### Dependencies
For a clean install of ros-base and ubuntu20
>~~~
>sudo apt install build-essential ros-noetic-vision-opencv ros-noetic-image-common python3-catkin-tools ros-noetic-usb-cam ros-noetic-image-pipeline
>~~~

- Create your catkin-ws.
- Clone this repo as a package to the src/ .
- Clone [pico-flexx-driver repo](https://github.com/code-iai/pico_flexx_driver)  to the src/ directory as another package. (A symlink would work)
- Follow the instructions on the aforementioned repository, it would ask you to place the royale sdk (that is for your system) to pico_flexx_driver/royale/ directory.
- Build your packages. (I use catkin-tools package instead of catkin_make)

After this you should be able to run the command to grab images from the pico flexx
~~~
roslaunch pico_flexx_driver pico_flexx_driver.launch
~~~
Launch rviz to check them out! Or use launcher files under ./launch/ to view them through image-view package.
