from setuptools import setup

setup(
    name="pricing_gym",
    version="0.0.1",
    author="Joakim B. Andersen",
    install_requires=["gym==0.26.2", "scipy==1.11.1"],
    description="A Gym Environment for Dynamic Pricing"    
)