from environs import Env
import requests

from pathlib import Path
from urllib.parse import urlparse, quote
import argparse
import json

from dialogflow import create_intent


def create_parser():
    parser = argparse.ArgumentParser(
        description='Add intent to the gialogflow project using a json file.'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-url',
        '--json_file_url',
        type=str,
        help='indicate url of json file'
    )
    group.add_argument(
        '-path',
        '--json_file_path',
        type=str,
        help='indicate url of json file'
    )

    return parser


def is_valid_json_url(json_url):
    parsed_url = urlparse(json_url)
    if (parsed_url.scheme and
        parsed_url.netloc and
        parsed_url.path.endswith('.json')):
        return True
    else:
        return False


def is_valid_file_path(filepath):
    if not isinstance(filepath, Path):
        filepath = Path(filepath)
    return filepath.exists() and filepath.is_file()


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.json_file_url:
        json_url = args.json_file_url
        if is_valid_json_url(json_url):
            response = requests.get(json_url)
            response.raise_for_status()
            questions = response.json()
        else:
            print(f'Page {args.json_file_path} not found.')
            return

    if args.json_file_path:
        json_path = Path(args.json_file_path)
        if is_valid_file_path(json_path):
            with open(json_path, 'r', encoding='utf8') as file:
                questions = json.load(file)
        else:
            print(f'File {args.json_file_path} not found.')
            return

    env = Env()
    env.read_env()
    project_id = env.str('DIALOGFLOW_PROJECT_ID')

    for display_name, phrases in questions.items():
        if display_name and phrases.get('questions') and phrases.get('answer'):
            create_intent(
                project_id,
                display_name,
                phrases.get('questions'),
                phrases.get('answer')
            )


if __name__ == '__main__':
    main()
