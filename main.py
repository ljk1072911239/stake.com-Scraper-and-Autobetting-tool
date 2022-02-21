from stake_auth import AuthClass
from stake_scraper import EventScraper
from stake_scraper_markets import MoneyLine
from stake_autobet import MoneyLineBet

if __name__ == "__main__":
    # SAMPLE USAGE....

    # Declaring variables, and creating objects #

    username = "STAKE_USERNAME"
    password = "STAKE_PASSWORD"
    anti_cpt_api_key = "ANTI_CAPTCHA_API_KEY"

    bet_currency = "ltc"
    bet_stake = 0.1

    main_user = AuthClass(username, password, anti_cpt_api_key)
    events_table_tennis_pre = EventScraper("table_tennis", False)
    market_table_tennis_moneyline_pre = MoneyLine("table_tennis", False)
    autobet_tabletennis_moneyline = MoneyLineBet(market_table_tennis_moneyline_pre.table_name, 0.1, "ltc", main_user)

    # Do the authentication, ETL processes...
    #main_user.cycle()
    events_table_tennis_pre.cycle()
    market_table_tennis_moneyline_pre.cycle()

    df = market_table_tennis_moneyline_pre.dataframe
    print(df)

    """start_time = df["TIME"][0]
    home_player = df["HOME"][0]
    away_player = df["AWAY"][0]
    autobet_tabletennis_moneyline.home(start_time, home_player, away_player)"""

    input("PRESS ENTER TO EXIT")