from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.descriptions import ParameterValue


def generate_launch_description():
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "xela_sensor",
            description="Model of xela sensor.",
            choices=["1x6", "4x4", "4x6", "aftc", "aftf", "allegro_hand_right", "taxel", "xela"],
        )
    )
    # Initialize Arguments
    xela_sensor            = LaunchConfiguration("xela_sensor")
    rviz_config_file        = LaunchConfiguration("rviz_config_file")

    description_file = PathJoinSubstitution([
        FindPackageShare("xela_models"),
        "urdf",
        PythonExpression(["'", xela_sensor, ".xacro'"])
    ])
    declared_arguments.append(
        DeclareLaunchArgument(
            "description_file",
            default_value=description_file,
            description="URDF/XACRO description file (absolute path) with the robot.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "rviz_config_file",
            default_value=PathJoinSubstitution(
                [FindPackageShare("xela_models"), "rviz", "urdf.rviz"]
            ),
            description="RViz config file (absolute path) to use when launching rviz.",
        )
    )
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            description_file,
        ]
    )
    robot_description = {"robot_description": ParameterValue( 
                            robot_description_content, value_type=str)}

    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )
    nodes_to_start = [
        joint_state_publisher_node,
        robot_state_publisher_node,
        rviz_node,
    ]
    return LaunchDescription(declared_arguments + nodes_to_start)