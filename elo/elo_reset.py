import openpyxl
from elo.models import Player
import traceback
from elo.constants import source, rank_elo_map


def reset():
    try:
        book = openpyxl.load_workbook(source)
        player_sheet = book.get_sheet_by_name('Player')
        c = 2
        player_name = player_sheet.cell(row=c, column=1).value
        ini_rank = player_sheet.cell(row=c, column=2).value
        while player_name and ini_rank is not None:
            ini_elo = rank_elo_map[ini_rank]
            player = Player.objects.get(name=player_name)
            player.elo = ini_elo
            player.total_games = 0
            player.save()
            c += 1
            player_name = player_sheet.cell(row=c, column=1).value
            ini_rank = player_sheet.cell(row=c, column=2).value
        print('player elo reset finished')
    except:
        book.close()
        traceback.print_exc()