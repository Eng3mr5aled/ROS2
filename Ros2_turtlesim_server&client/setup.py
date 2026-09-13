from setuptools import find_packages, setup

package_name = 'my_turtle_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='amrkhaled237',
    maintainer_email='amrkhaled237@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'turtle_control = my_turtle_pkg.turtle_control:main',
            'shape_server = my_turtle_pkg.shape_server:main',
            'shape_client = my_turtle_pkg.shape_client:main',
        ],
    },
)
