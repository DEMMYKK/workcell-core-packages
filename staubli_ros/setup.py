from setuptools import find_packages, setup

package_name = 'staubli_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools','transforms3d'],
    zip_safe=True,
    maintainer='staubli-1',
    maintainer_email='staubli-1@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'staubli_publisher = staubli_ros.stubli_publisher:main',
            'open_grip = staubli_ros.open_gripper:main'
        ],
    },
)
