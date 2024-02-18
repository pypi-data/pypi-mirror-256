from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()


setup(
    name="futurevision", 
    version="0.1.5",  
    description="Library that combines Robotics Hardware, iPhone and AI for Everyone",  
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/AliEdis/futurevision",
    author="Ali Edis",  
    author_email="aliedis34@gmail.com",  
    keywords = [
    'iPhone',
    'Raspberry Pi',
    'Arduino',
    'Computer Vision',
    'Artificial Intelligence',
    'Image Processing',
    'Robotics Hardware',
    'Face Recognition',
    'Sound Intensity Measurement',
    'Eye Blink Detection',
    'Sign Language',
    'Color Recognition',
    'Raspberry Pi Sense Hat',
    'Emotion Detection',
    'Face Counter',
    'Body Detection and Analysis',
    'Object Recognition',
    'Keyboard Control',
    'iPhone Hardware',
    ],
    
    package_dir={'futurevision': 'futurevision'},

    package_data={
        'futurevision': ['*.dat', '*.caffemodel', '*.txt','*.md'],
    },
    
    
    install_requires=[
        'opencv-python',
        'mediapipe',
        'numpy',
        'pyserial',
        'scipy',
        'pyautogui',
        'pygame',
        'flask',
        'dlib',
        'gtts',
    ],
    license="MIT",
    project_urls={
        "Bug Reports": "https://github.com/AliEdis/futurevision/issues",
        "Funding": "https://donate.pypi.org",
        "Source": "https://github.com/AliEdis/futurevision",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Natural Language :: English',
        ],

)
