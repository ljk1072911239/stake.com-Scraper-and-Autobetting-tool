from stake_auth import AuthClass
from stake_sport_id_updater import SportIdUpdater
from stake_scraper import EventScraper
from stake_scraper_markets import MoneyLine
from stake_autobet import MoneyLineBet

if __name__ == "__main__":
    # SAMPLE USAGE....

    username = "STAKE_USERNAME"
    password = "STAKE_PASSWORD"
    anti_cpt_api_key = "ANTI_CAPTCHA_API_KEY"

    bet_currency = "ltc"
    bet_stake = 0.1

    main_user = AuthClass(username, password, anti_cpt_api_key)
    # main_user.cycle()

    sport_id_updater = SportIdUpdater()
    sport_id_updater.cycle()

    events_table_tennis_pre = EventScraper("table_tennis", False)
    events_table_tennis_pre.cycle()

    market_table_tennis_moneyline_pre = MoneyLine("table_tennis", False)
    market_table_tennis_moneyline_pre.cycle()
    df = market_table_tennis_moneyline_pre.dataframe
    print(df)
    start_time = df["TIME"][0]
    home_player = df["HOME"][0]
    away_player = df["AWAY"][0]

    autobet_table_tennis_moneyline = MoneyLineBet(df, bet_stake, bet_currency, main_user)
    autobet_table_tennis_moneyline.home(start_time, home_player, away_player)
