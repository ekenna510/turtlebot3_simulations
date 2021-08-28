#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
import launch_ros.actions 

TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']


def generate_launch_description():
    #gui1 = launch.actions.DeclareLaunchArgument( 'gui', default_value='false')
    #print(gui1)
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    #world_file_name = 'turtlebot3_houses/' + TURTLEBOT3_MODEL + '.model'
    world_file_name = 'wlroom.world'
    world = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'worlds', world_file_name)
    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
    spawn_launch_dir=os.path.join(get_package_share_directory('robot_spawner_pkg'), 'launch')
    #urdffile = os.path.join(get_package_share_directory('turtlebot_description'),''
    requestname= TURTLEBOT3_MODEL
    namespacename=''
    x='0.0'
    y='0.0'
    z='0.0'
    #doc=xacro.process_file()

    guiz= LaunchConfiguration('guic', default='false')
    gui = 'true'
    print(str(gui))
    #guic.parse
    mycmd = 'gzserver'
    if (gui == 'true'):
        mycmd = 'gazebo'
        print("full")
    else:
        print("headless")

    print("mycmd",mycmd)
    print("world",world)
    #

    return LaunchDescription([
        ExecuteProcess(
            cmd=[mycmd, '--verbose', '-s', 'libgazebo_ros_factory.so' , world],
            output='both')
        ,
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, '/robot_state_publisher.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        )
        ,
        launch_ros.actions.Node(
           package='robot_spawner_pkg', executable='spawn_turtlebot', output='both',
           arguments=[requestname,namespacename,x,y,z]
           
       ),
 #       IncludeLaunchDescription(
 #           PythonLaunchDescriptionSource([launch_file_dir, '/burger_tf_pub.launch.py']),
 #           launch_arguments={'use_sim_time': use_sim_time}.items(),
 #       )

        # launch_ros.actions.Node(
        #     package='gazebo_ros', node_executable='spawn_model', node_name='spawn_urdf',
        #     arguments='-urdf -model turtlebot3_$(arg model) -x $(arg x_pos) -y $(arg y_pos) -z $(arg z_pos) -param robot_description'
        # )
 
    ])
    