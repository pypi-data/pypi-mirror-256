from setuptools import setup
setup(
    name='Rubik_Vault',
    version='5.5',
    description='¡Bienvenido a Rubik Vault, tu lugar para explorar y coleccionar imágenes de cubos Rubik!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  #Obligatorio especificar el tipo de archivo que es el README.md
    author='Michael Esquivel',
    author_email='michaelesquivel100@gmail.com',
    url='https://github.com/Michael-Esquivel/Rubik-Vault',
    license_files=['LICENSE'],

    packages=['codex','codex.res'],
    scripts=[],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
    ],
)