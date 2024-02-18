from setuptools import setup


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='lexi-craft',
    version='0.2.4',
    author='PurpleFta',
    author_email='helloworldfirstfta@gmail.com',
    description='Корректирует текст согласно грамматическим нормам',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/purple-fta/lexi_craft',
    packages=["lexi_craft"],
    install_requires=["python-dotenv", "openai"],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='text correction grammar',
    project_urls={
        'GitHub': 'https://github.com/purple-fta/lexi_craft'
    },
    python_requires='>=3.6'
)

