# stake.com-Scraper-and-Autobetting-tool

### Scrape "Stake.com" odds easily, place bets, even bypassing their CAPTCHA protection with "anti-captcha"!

*Personal note: This is was one of my actual Stake.com scrapers before my account was limited to pennies and two factor auth has gotten forcefully enabled, so I decided to abandon this project. The same thing is likely to happen to you, although two factor authentication can be bypassed with additional work. **I am not responsible for any account closures or lost funds with the use of this tool**!*

## Important
### External dependencies:
- Pandas: `pip install pandas`
- AntiCaptcha: [You need to have a funded account with API KEY](https://anti-captcha.com/)

### Usage
- The authentication is only working for accounts without two factor authentication (2FA) enabled.
- The relevant data gets saved to the execution directories in Pickle format. This was a personal preference because of my complicated betting software, you should edit it to suit your methodology.
- For practical usage, see [main.py](https://github.com/matthews-g/stake.com-Scraper-and-Autobetting-tool/blob/main/main.py)

I recommend extracting out bits from this code and building your own tool, this one serving as a helper for CAPTCHA bypassing, scraping and automatic betting. It is very similiar for all bookmakers. 

## TO DO (recommended)
- 2FA bypass
- OneXTwo, OverUnder, Handicap scraping & betting modules
- Currency converter

### LEARN MORE ABOUT ODDS SCRAPING & PROGRAMMATIC BETTING! JOIN THE COMMUNITY!
- [PRIMARY DISCORD (General)](https://discord.gg/NsSRzJk)
- [SECONDARY DISCORD (Bet365)](https://discord.gg/MjFr2HvUtK)


