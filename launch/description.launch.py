import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, RegisterEventHandler, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command, LaunchConfiguration, FindExecutable
from launch.event_handlers import OnProcessStart
from launch.descriptions import Executable

def generate_launch_description():

  use_sim_time = LaunchConfiguration('use_sim_time', default='false')

  pkg_share = FindPackageShare(package='rx1_arm_description').find('rx1_arm_description')
  default_model_path = os.path.join(pkg_share, 'xacro/model.xacro')

  robot_state_publisher_node = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': Command(['xacro ', default_model_path])}]
            )

  joint_state_publisher_exec = ExecuteProcess(
        cmd=[[
            FindExecutable(name='ros2'),
            ' run ',
            ' joint_state_publisher_gui ',
            ' joint_state_publisher_gui'
        ]],
        shell=True
    )

  return LaunchDescription([

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),

        robot_state_publisher_node,
        RegisterEventHandler(
            OnProcessStart(
                target_action=robot_state_publisher_node,
                on_start=[
                    LogInfo(msg='robot_state_publsiher started, start joint state publisher'),
                    joint_state_publisher_exec
                ]
            )
        )

  ]

  )
