import sys
# replays_unpack is used as a submodule so we need to fix the path for it
sys.path.insert(0, 'replays_unpack')
from replay_parser import ReplayReader
from chat_player import ChatPlayer

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 run.py <replay_file>')
        sys.exit(1)
    replay_path = sys.argv[1]

    reader = ReplayReader(replay_path)
    replay = reader.get_replay_data()
    chat = ChatPlayer(replay.engine_data.get('clientVersionFromXml').replace(' ', '').split(','), replay_path)
    chat.play(replay.decrypted_data, strict_mode=True)
    chat.writeChats()
