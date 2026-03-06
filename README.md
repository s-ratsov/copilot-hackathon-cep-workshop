# GitHub Copilot Workshop

## Build a Rock, Paper, Scissors game from scratch with GitHub Copilot

<img width="400" alt="Rock Paper Scissors image" src="./assets/Rock Paper Scissors image.png">

In this fun workshop, you will learn how to use GitHub Copilot to build a simple game in Python, with little to no coding experience required.

Estimated time to complete: `10 to 60 minutes`

Participants will be guided to install the GitHub Copilot VS Code extension, follow a CodeTour to learn how to interact with GitHub Copilot, and then use GitHub Copilot to build a Rock, Paper, Scissors game from scratch. 

Depending on the time available, participants will be able to complete the game or just get started, from a simple version all the way to introducing additional logic to make the game more interesting complete, with unit tests and REST API endpoints.

## How To Play

This repository now includes the extended **Rock, Paper, Scissors, Lizard, Spock** version of the game.

### Play in the terminal (CLI mode)

Run:

```bash
python3 main.py
```

You will see:

```text
Choose your option:
1. Rock
2. Paper
3. Scissors
4. Lizard
5. Spock
```

You can enter either:

- A number (`1` to `5`)
- A choice name (`rock`, `paper`, `scissors`, `lizard`, or `spock`)

### Play via REST API

Start the API server:

```bash
python3 main.py --mode api --host 127.0.0.1 --port 8000
```

Send a move using JSON:

```bash
curl -X POST http://127.0.0.1:8000/play \
  -H "Content-Type: application/json" \
  -d '{"choice":"rock"}'
```

Or use path-based endpoints:

```bash
curl -X POST http://127.0.0.1:8000/rock
curl -X POST http://127.0.0.1:8000/paper
curl -X POST http://127.0.0.1:8000/scissors
curl -X POST http://127.0.0.1:8000/lizard
curl -X POST http://127.0.0.1:8000/spock
```

### Run tests

```bash
python3 -m unittest discover -s tests -v
```

### Winning logic (who beats who)

Each round compares your choice with the computer's choice.

- If both choices are the same, the result is a **tie**.
- Otherwise, each choice beats exactly two others:
  - **Rock** beats **Scissors** and **Lizard**
  - **Paper** beats **Rock** and **Spock**
  - **Scissors** beats **Paper** and **Lizard**
  - **Lizard** beats **Paper** and **Spock**
  - **Spock** beats **Rock** and **Scissors**

Result rules:

- If the computer's move is in the list your move beats, you **win**.
- If not (and it is not a tie), the computer **wins**.



## Instructions 

Inside the `.instructions` folder you will find a number of markdown files that contain the instructions for this workshop.

Filename | Description
--- | ---
[1. setup.md](</.instructions/1. setup.md>) | Instructions for installing the GitHub Copilot VS Code extension and joining the GitHub Copilot trial.
[2. core exercises.md](</.instructions/2. core exercises.md>) | Instructions for getting started with GitHub Copilot.
[3. challenge exercises.md](</.instructions/3. challenge exercises.md>) | Challenge exercises for participants to complete.
[4. additional resources.md](</.instructions/4. additional resources.md>) | Additional resources for participants to explore after the workshop.


## Running a workshop?

If you're planning to run a GitHub Copilot workshop, please review the [workshop guide](</.instructions/workshop organisers.md>) for tips and tricks to help you run a successful workshop. 


## Project Structure

In this project you will find: 

* a `main.py` file with no contents
* a devcontainer that installs CodeTour and GitHub Copilot when the Codespace is created (If you want to use Codespaces)
* an `.instructions` folder all the instructions for this workshop.
* an `assets` folder containing images used in this workshop documentation.
* a `.tours` folder that includes the CodeTour file if you wish to use it.




## FAQ 

- **How do I get a GitHub Copilot license?**
  - You can request a trial license from your GitHub Sales representative or via Copilot for Individuals or Business licenses.
- **How do I get a GitHub Codespaces license?**
    - Codespaces is included with GitHub Enterprise Cloud, GitHub Enterprise Server, and GitHub Free. You can check under your [billing settings page](https://github.com/settings/billing).
- **I am having trouble activating GitHub Copilot after I load the plugin, what should I do?**
    - This could be because you launched your Codespace before you activated GitHub Copilot or accepted the invitation to the trial org. Please try to reload your Codespace and try again.

## Acknowledgements

A special thanks to the following awesome Hubbers who have contributed in many different ways to our workshops. 
[blackgirlbytes](https://github.com/blackgirlbytes), [pierluigi](https://github.com/pierluigi), [yuichielectric](https://github.com/yuichielectric), [dchomh](https://github.com/dchomh), [nolecram](https://github.com/nolecram), [rsymo](https://github.com/rsymo), [damovisa](https://github.com/damovisa) and anyone else I've inadvertently missed.

Enjoy your workshop!
[anthonyborton](https://github.com/anthonyborton)

_v1.0 Released May, 2023_
