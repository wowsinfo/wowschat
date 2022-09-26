import os
import json
from typing import NamedTuple

from replay_unpack.core.entity import Entity
from replay_unpack.clients.wows.player import ReplayPlayer as WoWSReplayPlayer

class Chat(NamedTuple):
    player_id: int
    namespace: str
    message: str


class ChatPlayer(WoWSReplayPlayer):
    _chats = []

    def __init__(self, version: str, replay_path: str):
        super(WoWSReplayPlayer, self).__init__(version)
        # listen to chat messages
        Entity.subscribe_method_call("Avatar", "onChatMessage", self._on_chat_message)

        # the output file will be in the same directory as the replay with .log as extension
        self._output_file = os.path.splitext(replay_path)[0] + '.log'

    def _on_chat_message(self, entity: Entity, player_id, namespace, message, unk):
        if player_id in [0, -1]:
            return
        
        self._chats.append(Chat(player_id, namespace, message))

    def writeChats(self):
        '''
        Read information about the match
        '''
        players = self._battle_controller._players.get_info()
        with open(self._output_file, 'w', encoding='utf-8') as f:
            for chat in self._chats:
                player = players[chat.player_id]
                player_name = player['name']
                player_clan = player['clanTag']

                final_message = '{}: {}'.format(player_name, chat.message)
                if player_clan.strip() != '':
                    final_message = '[{}]{}'.format(player_clan, final_message)
                print(final_message)
                f.write(final_message + '\n')
            