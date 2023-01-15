import setuptools

setuptools.setup(
    name='restaurant_schedule',
    description='API for restaurant schedule',
    author='Tamirlan Omarov',
    author_email='omarovt96@gmail.com',
    packages=setuptools.find_namespace_packages(include=['api.*']),
    python_requires='>=3.8, <4',
    install_requires=[
        'fastapi==0.88.0',
        'uvicorn[standard]==0.20.0',
    ],
    extras_require={
        'dev': [
            'flake8-bugbear==22.12.6',
            'flake8-commas==2.1.0',
            'flake8-quotes==3.3.1',
            'flake8==5.0.4',
            'pep8-naming==0.12.1',
        ],
        'test': [
            'httpx==0.23.1',
            'pytest==7.2.0',
        ],
    },
)
