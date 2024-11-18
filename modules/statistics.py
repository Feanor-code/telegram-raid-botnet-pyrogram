from pyrogram import Client
from rich.console import Console

import phonenumbers
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
    country_code_for_region
)


console = Console()


class Statistics:
    """Statistics"""

    async def ask(self) -> None:
        self.code = []
        self.country_list = {}

    async def check_number(self, session: Client) -> None:
        try:
            me = await session.get_me()
        except Exception as error:
            return console.print(error, style="bold white")
            
        country = phonenumbers.parse(f"+{me.phone_number}")

        string_country = region_code_for_country_code(country.country_code)
        code_country = country_code_for_region(string_country)

        self.country_list[string_country]=code_country
        self.code.append(code_country)

    async def execute(self, session: Client) -> None:
        await self.checking_number(session)

    def prt(self) -> None:
        print()

        for name, code in self.country_list.items():
            if code in self.code:
                console.print(
                    "[*] [white]+{code} [magenta]{country}[/] COUNT: {count}"
                    .format(code=code, country=name, count=self.code.count(code))
                )
        
        print()