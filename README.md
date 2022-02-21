# stake.com-Scraper-and-Autobetting-tool

## Scrape "Stake.com" odds easily, place bets, even bypassing their CAPTCHA protection with "anti-captcha"!

*Personal note: This is was one of my actual Stake.com scrapers before my account was limited to pennies and two factor auth has gotten forcefully enabled, so I decided to abandon this project. The same thing is likely to happen to you, although two factor authentication can be bypassed with additional work. **I am not responsible for any account closures or lost funds with the use of this tool**!*

## REQUIREMENTS

- Libraries: `pip install -r requirements.txt`
- AntiCaptcha: [You need to have a funded account with API KEY](https://anti-captcha.com/)
- [PostgreSQL](https://www.postgresql.org/download/)

## USAGE
### You need to create a database.
  - This can be done by simply executing *stake_postgresql.py* OR creating it manually via pgAdmin 4.
  - Make sure that the connection data is correct in *stake_postgresql.py*
  ```
  POSTGRES_USERNAME = 'postgres'
  POSTGRES_PASSWORD = 'asd'
  POSTGRES_IP = 'localhost'
  POSTGRES_PORT = '5432'
  POSTGRES_DB_NAME = 'stake_data'
  POSTGRES_SCHEMA_NAME = 'public'
  ```
  - The tables will be stored in the *public* schema, so no need to create an additional one.

### General usage, logic of the program
  - Just simply run [main.py](https://github.com/matthews-g/stake.com-Scraper-and-Autobetting-tool/blob/main/main.py) and check code to easily understand how it works, and how it should be extended.
  - The tables in the database are handled automatically using prewritten functions. No need to worry about creating them before.
  - For automatic sport id updates, add `import stake_sport_id_updater.py` to the main code, the update will get executed on every program launch.

### You should know
  - The authentication is only working for accounts **_without_** two factor authentication (2FA) enabled.

  - I recommend extracting out bits from this code and building your own tool, this one serving as a helper for CAPTCHA bypassing, scraping, data storing and automatic betting. It is very similiar for all bookmakers. 

## TO DO (recommended)
- 2FA bypass
- OneXTwo, OverUnder, Handicap scraping & betting modules
- Currency converter

## LEARN MORE ABOUT ODDS SCRAPING & PROGRAMMATIC BETTING! JOIN THE COMMUNITY!
- [PRIMARY DISCORD (General)](https://discord.gg/NsSRzJk)
- [SECONDARY DISCORD (Bet365)](https://discord.gg/MjFr2HvUtK)


