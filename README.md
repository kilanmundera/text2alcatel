# Text2Alcatel

A Python tool to generate audio files from a CSV list of text entries using [Coqui TTS](https://github.com/coqui-ai/TTS), then convert them to A-Law encoded, mono, 8kHz `.wav` files suitable for telephony systems like Alcatel.

---

## Features

- Prepare a `csv` file containing multilingual text entries for the vocal messages you would like to generate and give it to `text2alcatel`
- `text2alcatel` will then generate `.wav` files, using [Coqui TTS](https://github.com/coqui-ai/TTS) and convert them to the appropriate format for Alcatel telephony servers (mono, 8kHz, A-Law codec).
- `text2alcatel` uses a checkpoint system in order not to generate a message that has already been generated.
- Supports models, speaker and language ID selection.

---

## Requirements

- Python 3.8+
- FFmpeg installed and available in the system `PATH`

---

## Installation

1. Clone the repository or copy the files to a local folder:
   ```bash
   git clone https://github.com/kilanmundera/text2alcatel
   cd text2alcatel
   ```

## Usage

1. Activate the virtual environment and install dependencies:
   ```bash
   source ./activate_venv

   # Example : 
   user@myhost:~/text2alcatel# source ./activate_venv
   [...]
   # The (venv_coqui) below shows that you're indeed in the venv_coqui virtual environment :
   (venv_coqui) user@myhost:~/text2alcatel# 
   ```

2. Prepare a CSV file
The CSV must be UTF-8 encoded, comma separated, double-quoted values, without any header :
```csv
"welcome01","Welcome to our service","en"
"accueil01","Bienvenue dans notre entreprise.","fr"
"occupe01","Votre correspondant est occupé. Merci de laisser un message s'il vous plait","fr"
```
Use Libre-Office or any Linux text editing software program (`nano`, `vim`, etc.)
**Do not use Microsoft Excel**.

3. Run the script
```bash
python3 ./text2alcatel.py --input_csv ./messages.csv
```
4. The audio files are written to the output directory (`output_audio` by default), in a directory named after their language.
Example : 
```bash
output_audio/
├── en
│   ├── bienvenue.wav
│   └── fin_appel.wav
└── fr
    ├── bienvenue.wav
    └── correspondant_occupé.wav
```
5. To exit for the virtual invironment : 
```bash
deactivate
```

### Available options:

| Option              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `--input_csv`       | Path to the input CSV file (required unless listing models/languages)       |
| `--output_folder`   | Output directory for audio files (`output_audio` by default)                |
| `--model_name`      | Coqui TTS model name to use                                                 |
| `--speaker_idx`     | Name of the speaker voice (default: `"Abrahan Mack"`)                       |
| `--list_models`     | List all available models                                                   |
| `--list_languages`  | List supported languages for the given model                                |
| `--list_speakers`   | List supported speakers for the given model                                 |


## To do :
* Implement an _already done_ system for the messages that have already be generated
* Translate the comments and options to english

