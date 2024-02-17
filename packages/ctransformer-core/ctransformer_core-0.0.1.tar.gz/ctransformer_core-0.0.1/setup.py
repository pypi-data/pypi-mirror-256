import os

kwargs = {}
if os.environ.get("CT_WHEEL") == "1":
    from setuptools import setup
else:
    from skbuild import setup

    cmake_args = []
    for key in ["CT_INSTRUCTIONS", "CT_CUBLAS", "CT_HIPBLAS", "CT_METAL"]:
        value = os.environ.get(key)
        if value:
            cmake_args.append(f"-D{key}={value}")
    if cmake_args:
        kwargs["cmake_args"] = cmake_args

with open("README.md") as f:
    long_description = f.read()

name = "ctransformer_core"

setup(
    name=name,
    version="0.0.1",
    description="gguf connector core built on ctransformers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="calcuis",
    author_email="calculatics@gmail.com",
    license="MIT",
    packages=[name, "ctransformer_core.gptq"],
    package_data={name: ["lib/*/*.so", "lib/*/*.dll", "lib/*/*.dylib"]},
    install_requires=[
        "huggingface-hub",
        "py-cpuinfo>=9.0.0,<10.0.0",
    ],
    extras_require={
        "cuda": [
            "nvidia-cuda-runtime-cu12",
            "nvidia-cublas-cu12",
        ],
        "gptq": [
            "exllama==0.1.0",
        ],
        "tests": [
            "pytest",
        ],
    },
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="{} gguf connector transformers ai llm".format(name),
    **kwargs,
)
