from setuptools import find_packages, setup

import os
import subprocess
import time

def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content

def get_git_hash():

    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH', 'HOME']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        sha = out.strip().decode('ascii')
    except OSError:
        sha = 'unknown'

    return sha


def get_hash():
    if os.path.exists('.git'):
        sha = get_git_hash()[:7]
    else:
        sha = 'unknown'

    return sha

def get_requirements(filename='requirements.txt'):
    here = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(here, filename), 'r') as f:
        requires = [line.replace('\n', '') for line in f.readlines()]
    return requires

if __name__ == '__main__':
    setup(
        name='HyperRez',
        version="1.0",
        description='Sharpen Blurry Memories: Supercharge Your Images with HyperRez',
        long_description=readme(),
        long_description_content_type='text/markdown',
        author='Rauhan Ahmed Siddiqui',
        author_email='rauhaan.siddiqui@gamil.com',
        keywords='computer vision, pytorch, image restoration, super-resolution, esrgan, real-esrgan, gfpgan, gradio, image enhancer, image quality enhancement, image upscaler, image quality upscaler',
        url='https://github.com/RauhanAhmed/HyperRez',
        include_package_data=True,
        packages=find_packages(exclude=('options', 'datasets', 'experiments', 'results', 'tb_logger', 'wandb')),
        license='MIT',
        setup_requires=['cython', 'numpy'],
        install_requires=get_requirements(),
        zip_safe=False)
