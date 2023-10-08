import openpyxl
from elo.models import Player, Game
import traceback

rank_elo_map = {
    '15k': 600,
    '10k': 1100,
    '5k': 1600,
    '1d': 2100,
    '3d': 2300,
    '5d': 2500
}

try:
    book = openpyxl.load_workbook('LIHKG-Record.xlsx')
    player_sheet = book.get_sheet_by_name('Player')
    c = 2
    player_name = player_sheet.cell(row=c, column=1).value
    ini_rank = player_sheet.cell(row=c, column=2).value
    while player_name and ini_rank is not None:
        ini_elo = rank_elo_map[ini_rank]
        new_player = Player(name=player_name, elo=ini_elo, total_games=0)
        new_player.save()
        c += 1
        player_name = player_sheet.cell(row=c, column=1).value
        ini_rank = player_sheet.cell(row=c, column=2).value
    print('player data input finished')

    game_sheet = book.get_sheet_by_name('Record')
    c = 2
    black = game_sheet.cell(row=c, column=3).value
    white = game_sheet.cell(row=c, column=4).value
    result = game_sheet.cell(row=c, column=7).value
    game_date = game_sheet.cell(row=c, column=2).value
    while black is not None and white is not None and result is not None and game_date is not None:
        black_player = Player.objects.get(name=black)
        white_player = Player.objects.get(name=white)
        new_game = Game(black=black_player, white=white_player, result=result, game_date=game_date)
        new_game.save()
        black_player.total_games += 1
        black_player.save()
        white_player.total_games += 1
        white_player.save()
        c += 1
        black = game_sheet.cell(row=c, column=3).value
        white = game_sheet.cell(row=c, column=4).value
        result = game_sheet.cell(row=c, column=7).value
        game_date = game_sheet.cell(row=c, column=2).value
    print('game data input finished')
    book.close()
except:
    book.close()
    traceback.print_exc()