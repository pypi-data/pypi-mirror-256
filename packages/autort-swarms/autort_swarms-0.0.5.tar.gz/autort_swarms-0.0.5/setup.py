# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autort']

package_data = \
{'': ['*']}

install_requires = \
['einops',
 'swarms',
 'torch>=1.9.0,<2.0.0',
 'torchvision>=0.10.0,<0.11.0',
 'zetascale']

setup_kwargs = {
    'name': 'autort-swarms',
    'version': '0.0.5',
    'description': 'AutoRT - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# AutoRT\n![AutoRTImage](autort.png)\nImplementation of AutoRT: "AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents". This repo will implement the multi agent system that transforms a scene into a list of ranked and priortized tasks for an robotic action model to execute. This is an very effective setup that I personally believe is the future for swarming robotic foundation models!\n\nThis project will be implemented using Swarms, for the various llms and use the official RT-1 as the robotic action model.\n\n[PAPER LINK](https://auto-rt.github.io/static/pdf/AutoRT.pdf)\n\n## Install\n`$ pip3 install autort-swarms`\n\n\n## Usage\n\n\n### AutoRTAgent\nA single AutoRT agent that: analyzes a scene using visual COT -> generate tasks -> filter tasks -> execute it with a robotic transformer.\n```python\n# Import necessary modules\nimport os\nfrom autort import AutoRTSwarm, AutoRTAgent\n\n# Set the OpenAI API key\nopenai_api_key = os.getenv("OPENAI_API_KEY")\n\n# Define a list of AutoRTAgent instances\nagents = [\n    AutoRTAgent(openai_api_key, max_tokens=1000),\n    AutoRTAgent(openai_api_key, max_tokens=1000),\n]\n\n# Create an instance of AutoRTSwarm with the agents and datastore\nautort_swarm = AutoRTSwarm(agents)\n\n# Run the AutoRTSwarm with the given inputs\nautort_swarm.run(\n    "There is a bottle on the table.",\n    "https://i.imgur.com/2qY9f8U.png",\n)\n```\n\n\n### AutoRTSwarm\nA team of AutoRT agents where you can plug in and play any number of `AutoRTAgents` with customization. First, the task will be routed to each agent and then all of their outputs will be saved.\n```python\n# Import necessary modules\nimport os\nfrom autort import AutoRTSwarm, AutoRTAgent\n\n# Set the OpenAI API key\nopenai_api_key = os.getenv("OPENAI_API_KEY")\n\n# Define a list of AutoRTAgent instances\nagents = [\n    AutoRTAgent(openai_api_key, max_tokens=1000),\n    AutoRTAgent(openai_api_key, max_tokens=1000),\n]\n\n# Create an instance of AutoRTSwarm with the agents and datastore\nautort_swarm = AutoRTSwarm(agents)\n\n# Run the AutoRTSwarm with the given inputs\nautort_swarm.run(\n    "There is a bottle on the table.",\n    "https://i.imgur.com/2qY9f8U.png",\n)\n```\n\n## Citation\n```bibtex\n@inproceedings{\n    anonymous2023autort,\n    title={Auto{RT}: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents},\n    author={Anonymous},\n    booktitle={Submitted to The Twelfth International Conference on Learning Representations},\n    year={2023},\n    url={https://openreview.net/forum?id=xVlcbh0poD},\n    note={under review}\n}\n\n```\n\n\n# License\nMIT\n\n\n\n# Todo\n- [ ] Implement a run method into `AutoRTSwarm` that runs all the agents with APIs.\n- [ ] Make it able to send commands to a certain agent using the swarm network.\n- [ ] Send a task to all agents in the swarm network\n- [ ] ',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/AutoRT',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
