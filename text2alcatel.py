import os
import subprocess
import csv
import argparse
import sys
import venv
from TTS.api import TTS

def setup_virtual_env(env_dir):
    if not os.path.exists(env_dir):
        print("Création de l'environnement virtuel...")
        venv.create(env_dir, with_pip=True)
        subprocess.run([os.path.join(env_dir, "bin", "pip"), "install", "coqui-tts", "ffmpeg-python"], check=True)

def text_to_speech(text, output_path, model_name, language_idx, speaker_idx):
    tts = TTS(model_name=model_name)
    tts.tts_to_file(text=text, file_path=output_path, language=language_idx, speaker=speaker_idx)

def convert_audio(input_file, output_file):
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-ar", "8000", "-ac", "1", "-c:a", "pcm_alaw",
        output_file
    ]
    subprocess.run(ffmpeg_cmd, check=True)

def process_csv_file(input_csv_file, output_base_folder, model_name, speaker_idx):
    with open(input_csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 3:
                print(f"Ligne ignorée (mauvais format): {row}")
                continue

            filename, text, language_idx = row[0].strip(), row[1].strip(), row[2].strip()
            if not filename or not text or not language_idx:
                print(f"Ligne incomplète ignorée : {row}")
                continue

            output_folder = os.path.join(output_base_folder, language_idx)
            os.makedirs(output_folder, exist_ok=True)

            tts_output = os.path.join(output_folder, f"{filename}_temp.wav")
            final_output = os.path.join(output_folder, f"{filename}.wav")

            print(f"[{language_idx}] Génération de : {final_output}")
            text_to_speech(text, tts_output, model_name, language_idx, speaker_idx)
            convert_audio(tts_output, final_output)
            os.remove(tts_output)

def list_available_models():
#    print("Modèles disponibles :", TTS.list_models())
    models = TTS.list_models()
    print("Modèles disponibles : ")
    for model in models:
        print(f" - {model}")

def list_languages_for_model(model_name):
    print(f"Chargement du modèle : {model_name} ...")
    tts = TTS(model_name=model_name)
    languages = tts.languages
    print("\nLangues disponibles pour ce modèle :")
    for lang in languages:
        print(f" - {lang}")


def list_speakers_for_model(model_name):
    print(f"Chargement du modèle : {model_name} ...")
    tts = TTS(model_name=model_name)
    speakers = tts.speakers
    print("\nLocuteurs disponibles pour ce modèle :")
    for speaker in speakers:
        print(f" - {speaker}")

def main():
    parser = argparse.ArgumentParser(description="Générer des fichiers audio avec Coqui-TTS et les convertir avec FFmpeg.")
#    parser.add_argument("input_csv", help="Fichier CSV d'entrée contenant les messages.")
    parser.add_argument("--input_csv", help="Fichier CSV d'entrée contenant les messages.")
    parser.add_argument("--output_folder", default="output_audio", help="Dossier de sortie pour les fichiers audio.")
    parser.add_argument("--model_name", default="tts_models/multilingual/multi-dataset/xtts_v2", help="Nom du modèle Coqui TTS.")
    parser.add_argument("--speaker_idx", default="Abrahan Mack", help="Nom du locuteur (par défaut : 'Abrahan Mack').")
    parser.add_argument("--list_models", action="store_true", help="Lister les modèles disponibles.")
    parser.add_argument("--list_languages", action="store_true", help="Lister les langues disponibles pour le modèle.")
    parser.add_argument("--list_speakers", action="store_true", help="Lister les locuteurs disponibles pour le modèle.")

    args = parser.parse_args()
    # Si on veut lister les modèles ou les langues disponibles : 
    if args.list_models:
        list_available_models()
        sys.exit(0)

    if args.list_languages:
        list_languages_for_model(args.model_name)
        sys.exit(0)

 
    if args.list_speakers:
        list_speakers_for_model(args.model_name)
        sys.exit(0)

    # Sinon, on vérifie que le CSV est bien fourni
    if not args.input_csv:
        print("Erreur : Vous devez spécifier un fichier CSV avec --input_csv")
        parser.print_help()
        sys.exit(1)

#    env_dir = "venv_coqui"
#    setup_virtual_env(env_dir)
    process_csv_file(args.input_csv, args.output_folder, args.model_name, args.speaker_idx)

if __name__ == "__main__":
    main()

