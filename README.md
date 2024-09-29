# Metagame

Metagame is a JSON-based language for defining text-based games. It provides a framework for creating and running games based on JSON files that define game concepts and actions.

## Getting Started

To get started with Metagame, you need to set up your environment. Add the Metagame directory to your PYTHONPATH by modifying your bashrc file:

export METAGAME_PYTHON_PATH=/path/to/metagame/python/

export PYTHONPATH=$METAGAME_PYTHON_PATH:$PYTHONPATH

You can also use the provided bashrc.sh script to set up your environment.

## Running a Game

To run a game, use the following command:

python3 -m metagame path/to/game.json

Replace path/to/game.json with the path to your game file.

## How to run "Simple Dialog generation" sample

python3 -m metagame samples/00_textgeneration/sample_0003_dragon_description

## Game Files

Game files are JSON files that define game concepts and actions. The Metagame engine loads these files, parses the data, and runs the game loop.

Here is an example of a simple game file:

```json
{
  "concept1": {
    "attribute1": "value1",
    "attribute2": "value2"
  },
  "concept2": {
    "attribute1": "value1",
    "attribute2": "value2"
  }
}
```

## Contributing

Feel free to submit PRs. I will do my best to review and merge them if I consider them essential.

## License

Metagame is licensed under the MIT License. See the LICENSE file for more information.