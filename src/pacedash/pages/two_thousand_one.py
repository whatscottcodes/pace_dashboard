import dash_html_components as html
from ..components import Col, Row
from ..settings import color_palette

titles = [
    "Shrek",
    "Osmosis Jones",
    "Harry Potter and the Sorcerer's Stone",
    "Spirited Away",
    "Zoolander",
    "Monsters, Inc.",
    "Donnie Darko",
    "The Fast and the Furious",
    "The Royal Tenenbaums",
    "The Lord of the Rings: The Fellowship of the Ring",
    "A Beautiful Mind",
    "Amélie",
    "Ocean's Eleven",
    "Training Day",
    "Black Hawk Down",
    "The Fast and the Furious",
    "The Others",
    "Pearl Harbor",
    "Mulholland Dr.",
    "The Mummy Returns",
    "A.I. Artificial Intelligence",
    "Jurassic Park III",
    "Moulin Rouge!",
    "Hannibal",
    "Vanilla Sky",
    "American Pie 2",
    "Blow",
    "Enemy at the Gates",
    "Bridget Jones's Diary",
    "Planet of the Apes",
    "Lara Croft: Tomb Raider",
    "Rush Hour 2",
    "Swordfish",
    "K-PAX",
    "Legally Blonde",
    "A Knight's Tale",
    "Jay and Silent Bob Strike Back",
    "From Hell",
    "Scary Movie 2",
    "I Am Sam",
    "Spy Game",
    "Shallow Hal",
    "The Princess Diaries",
    "The Score",
    "Evolution",
    "Ghost World",
    "Rat Race",
    "Jeepers Creepers",
    "Spy Kids",
    "Serendipity",
    "The Mexican",
    "The Man Who Wasn't There",
    "Behind Enemy Lines",
    "Lagaan: Once Upon a Time in India",
    "Atlantis: The Lost Empire",
    "Super Troopers",
    "Not Another Teen Movie",
    "Ali",
    "The Experiment",
    "The One",
    "Sweet November",
    "Monster's Ball",
    "Final Fantasy: The Spirits Within",
    "Kate & Leopold",
    "Thir13en Ghosts",
    "Gosford Park",
    "Frailty",
    "The Wedding Planner",
    "Along Came a Spider",
    "Shaolin Soccer",
    "The Last Castle",
    "Bandits",
    "Joy Ride",
    "Brotherhood of the Wolf",
    "Kiss of the Dragon",
    "Waking Life",
    "The Devil's Backbone",
    "Save the Last Dance",
    "The Animal",
    "Cats & Dogs",
    "America's Sweethearts",
    "The Majestic",
    "Session 9",
    "The Pledge",
    "Wet Hot American Summer",
    "The Piano Teacher",
    "Heartbreakers",
    "Koroshiya 1",
    "Ghosts of Mars",
    "Joe Dirt",
    "15 Minutes",
    "Formula 51",
    "Jason X",
    "Don't Say a Word",
    "The Hole",
    "My Sassy Girl",
    "No Man's Land",
    "Hedwig and the Angry Inch",
    "Bully",
    "Bubble Boy",
    "Valentine",
    "Riding in Cars with Boys",
    "Rock Star",
    "Summer Catch",
    "Hardball",
    "Hearts in Atlantis",
    "The Glass House",
    "Knockaround Guys",
    "One Night at McCool's",
    "Baby Boy",
]

image_urls = [
    "https://m.media-amazon.com/images/M/MV5BMTUwYjczNmItYzczNS00MDQwLTkxNDctN2MwYzI5YzhmNGU4XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMzcwYWFkYzktZjAzNC00OGY1LWI4YTgtNzc5MzVjMDVmNjY0XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTY1NTI0ODUyOF5BMl5BanBnXkFtZTgwNTEyNjQ0MDE@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZjZlZDlkYTktMmU1My00ZDBiLWFlNjEtYTBhNjVhOTM4ZjJjXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNDg4NjM1YjMtYmNhZC00MjM0LWFiZmYtNGY1YjA3MzZmODc5XkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNjQ3NWNlNmQtMTE5ZS00MDdmLTlkZjUtZTBlM2UxMGFiMTU3XkEyXkFqcGdeQXVyNjUwNzk3NDc@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BOGZhM2FhNTItODAzNi00YjA0LWEyN2UtNjJlYWQzYzU1MDg5L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BOGJjNzZmMmUtMjljNC00ZjU5LWJiODQtZmEzZTU0MjBlNzgxL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYzVmYzVkMmUtOGRhMi00MTNmLThlMmUtZTljYjlkMjNkMjJkXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMDZkMTUxYWEtMDY5NS00ZTA5LTg3MTItNTlkZWE1YWRjYjMwL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYWMwMzQxZjQtODM1YS00YmFiLTk1YjQtNzNiYWY1MDE4NTdiXkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNzlkNzVjMDMtOTdhZC00MGE1LTkxODctMzFmMjkwZmMxZjFhXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTAxMDE4Mzc3ODNeQTJeQWpwZ15BbWU4MDY2Mjg4MDcx._V1_UY268_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTQ3MDc0MDc1NF5BMl5BanBnXkFtZTYwODI1ODY2._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNWM2MDZmMDgtYjViOS00YzBmLWE4YzctMDMyYTQ2YTc4MmVkXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMjE2NzU1NTk2MV5BMl5BanBnXkFtZTgwMjIwMzcxMTE@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNWU2NzEyMDYtM2MyOS00OGM3LWFkNzAtMzRiNzE2ZjU5ZTljXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZDMyZGJjOGItYjJkZC00MDVlLWE0Y2YtZGIwMDExYWE3MGQ3XkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMWFhYjliNjYtYjNhNS00OGExLWFhMjQtNDgwOWYyNWJiYzhmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYmUzODQ5MGItZTZlNy00MDBhLWIxMmItMjg4Y2QyNDFlMWQ2XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZDMxMjhiZmItNWMxMC00NzYyLWJiOTYtNGYwOTAyYjU5OWY4XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UY268_CR2,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYzFlMTJjYzUtMWFjYy00NjkyLTg1Y2EtYmZkMjdlOGQ1ZGYwL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BODI4NDY2NDM5M15BMl5BanBnXkFtZTgwNzEwOTMxMDE@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BOTEyYjhiMjYtNjU3YS00NmQ4LTlhNTEtYTczNWY3MGJmNzE2XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYjg5ZDkzZWEtZDQ2ZC00Y2ViLThhMzYtMmIxZDYzYTY2Y2Y2XkEyXkFqcGdeQXVyODAwMTU1MTE@._V1_UY268_CR3,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYWFlY2E3ODQtZWNiNi00ZGU4LTkzNWEtZTQ2ZTViMWRhYjIzL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYjc3NjU1ZTEtNmNjNi00YzNiLWI3OWQtMTJmYTRkZDc1NDE2XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BY2RlMDhlY2MtMjQ1Zi00NzI5LTgxOTgtZjliNWMzYTY3NWZkL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNzMzODVjMWUtYmIxZS00NDlkLTlmNTktNjI5NTdhZjUzYzY1XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BODhlNGJjMWQtZGMyYS00MzJhLWJhZGMtY2NlNDI5Nzg5NTU2XkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNzk5ZmQxMWYtM2QyNi00MTY3LTlmNjItYjUwODY3Y2YwOTIwXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMjE5ZDVkNDAtMTJmYy00NzkzLTg2ZDUtOTZkOTU1ZDYwYTFhL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_UY268_CR4,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNTEyNjUwMTkxMV5BMl5BanBnXkFtZTcwNjk0NDk0NA@@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTE5OTE4OTE2Nl5BMl5BanBnXkFtZTYwMDkzMTQ3._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BY2EyYWEwZmQtZWU0Yy00M2Y3LThiZTktOTQxZDUxY2ZjOTYwXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTM1MjkxNTQxMV5BMl5BanBnXkFtZTYwMDMxNDg2._V1_UY268_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMzQxYjU1OTUtYjRiOC00NDg2LWI4MWUtZGU5YzdkYTcwNTBlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYzEyNzc0NjctZjJiZC00MWI1LWJlOTMtYWZkZDAzNzQ0ZDNkXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNjNhOGZkNzktMGU3NC00ODk2LWE4NjctZTliN2JjZTQxZmIxXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTcwMzY2NDE0NF5BMl5BanBnXkFtZTYwNjg2Njc2._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMzcwYjEwMzEtZTZmMi00ZGFhLWJhZjItMDAzNDVkNjZmM2U5L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UY268_CR2,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZDNjYmY1ZDEtM2I3YS00MDhmLTk5NDYtYzU5MTA4ZjIyYzJiL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZTU3YjhjZmItNzBjNi00YWVjLWE0ZGQtNGY1NTFmMDczMzhkXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNWYwODRlYjgtODUxNy00YmMyLWE3NWYtNTYzZmUwNDJiZGVlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNWEzM2NjMjctM2U3Yi00MGZhLWJlYTYtMWEyYjVjZDEzZjM4XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTkwNDU0NTE0OV5BMl5BanBnXkFtZTgwNzAzNzQyMTI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BY2JhODU1NmQtNjllYS00ZmQwLWEwZjYtMTE5NjA1M2YyMzdjXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTkzMjEzOTQ3Nl5BMl5BanBnXkFtZTYwMjI1NzU5._V1_UY268_CR3,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNWIxZTExZjctZjA5ZC00NGQ2LTk4M2YtMWIyMGM2NzRlNWVkXkEyXkFqcGdeQXVyMTA0MjU0Ng@@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYjEwMGZkYTgtMTA5Ny00OWFhLTgzMWItYjhhMWUxYTIxNDgwXkEyXkFqcGdeQXVyNTc1NTQxODI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BM2RhNjdlYjMtOTM4Ni00MWZhLTkyZmItNmI2NDkxMjBhYTJkL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UY268_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNDYxNWUzZmYtOGQxMC00MTdkLTkxOTctYzkyOGIwNWQxZjhmXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNjM2NzNjMDAtZTAyMi00NTQzLWFlMTctNTUzMGE1ODE2NDRlXkEyXkFqcGdeQXVyNjY5NDU4NzI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYzAyOTZjZDItZjNiYy00YTA3LWEyYWMtZTA0NmUzYjZhNjg0XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BODYyNTQyNzAzNF5BMl5BanBnXkFtZTgwNTA4ODYxMTE@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZjA3OTUxNTktN2FlNC00NGUyLWI1NDktY2FlZTc5MDlmOGFhXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNThiMDc1YjUtYmE3Zi00MTM1LTkzM2MtNjdlNzQ4ZDlmYjRmXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UY268_CR3,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNzY4YmUzMDAtMDYyZS00MTBmLWEzZDAtOGY3MDE2YjJkMGUxL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTc4NjYzNzkzNl5BMl5BanBnXkFtZTYwNjg1ODc5._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNTkyMzk3NTYtY2FiYy00MWIwLWIyYzctODIzNzVlOGQxZmYwXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZWFmYmViNGEtNzM5NC00NDliLThmNTUtYTY1NjhiN2ZjMGM5XkEyXkFqcGdeQXVyMDM5ODIyNw@@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNmNlN2VlOTctYTdhMS00NzUxLTg0ZGMtYWE2ZTJmMThlMTk2XkEyXkFqcGdeQXVyMzI0NDc4ODY@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BOTlmNzY5YzgtOTBhYS00NDBlLWJhMTYtMzZmNjI4ODVkYmM4XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYzM4YzlhZGMtYTI2Yi00OTY4LWE0MzctNDFlYTQ3YmFlOTBjXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTIxNTE2MTY1Ml5BMl5BanBnXkFtZTYwODYyMTc2._V1_UY268_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNzBlYTE4NDAtN2RkNi00YWZmLWI3MWQtZDg2YTQ5OTI4YTVhL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BOTVlY2VhMWEtYmRlOC00YWVhLWEzMDktZWJlYzNiMWJmZTIwXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZjdiYTBiMDUtNTg0Yy00N2NhLWIxZmEtMTEwNDNlYzRkMGY3L2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_UY268_CR15,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTQ3MTY0MjU3M15BMl5BanBnXkFtZTYwMzkwOTc5._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTkyMzA3OTI3NV5BMl5BanBnXkFtZTYwMjU0ODM3._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYTA2NjNkYjUtMWFiYy00MjA4LTk3YTUtYjQwNTVjNjZkZDUxXkEyXkFqcGdeQXVyNTE4Mzg4MTE@._V1_UY268_CR3,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMzQ2N2NlNWQtY2Q1Mi00ZTc3LWE5YmMtNGVjMjYxODRjOGZjXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNTkxMjg5MDYtZDkyMS00NjFlLTk5YTItMWUyOTNkOTg4YmRhXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYzM0ZDIxNDYtZDJjMy00NTc5LWIyMTgtMzBhNGRiZTU0ZmRjL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMWM0ZjY5ZjctODNkZi00Nzk0LWE1ODUtNGM4ZDUyMzUwMGYwXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZTI3MDcwZGItZDMwNS00ZDBjLWEwOGEtMWEyMWUxNDlkYzBjL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_UY268_CR4,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNjkzMjFkNmQtYTQ2Yy00NTRhLWE0ZGYtNjBmYTcyOTgxNGYxL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMjE1OTExNTEzMV5BMl5BanBnXkFtZTYwNDQ3MDk2._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BY2JmMDJlMmEtYTk4OS00YWQ5LTk2NzMtM2M3NzhkMjI4MGJkL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYzNkY2E5MTgtYTE4NC00MjVhLWE5NzEtMjRjZjdiM2ZlOGU4XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BOTI2NjkzMTkxM15BMl5BanBnXkFtZTYwMzM2MjA5._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMWYyYzc4MTItOTdkOS00ZTIwLWE2N2MtZjA4N2YxMTI2NjViXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNTJjNTMyOGUtOTE2Ni00MGZhLWI5OGEtNWQ3MzQ2NGIzYTJiXkEyXkFqcGdeQXVyMjA0MzYwMDY@._V1_UY268_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZjdjYjlhNTctNDY0Yi00ZTM4LWE1MWItYWUzNmYwYWU0OTI4XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZDBkYjYxYjUtMTdmMS00MDJhLWEyNzktYzg2OWY5NWY0Y2QyL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNDkzNTM2ODg@._V1_UY268_CR1,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTQ2NjE3NjQzOF5BMl5BanBnXkFtZTcwMDIwOTA0NA@@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNDZmOWE3M2YtMDNkNC00YzFmLTljZTItNTk3NTlkODIxNGE3XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UY268_CR4,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMGFlNzNmY2ItYmZjMi00ZjQ1LWJjMmMtODM5MWQ0NzI3NzBhXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_UY268_CR3,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTE5NDgxNzU1MV5BMl5BanBnXkFtZTYwODQ4ODE3._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTI3MzQ1MzIwNl5BMl5BanBnXkFtZTYwMTAxODc5._V1_UY268_CR2,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTg5NzU4NjEwNV5BMl5BanBnXkFtZTYwNTk4NzM3._V1_UY268_CR1,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BYzc0MDllYjktYzFjZi00OTgwLWJmZWMtODlmMTVlODQyZTgwXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNzM1OThlODItMTI5NC00ZDE1LWE4MzQtOTJiNDQ5NDAxZTBkXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNWNiYzNmOWYtMjNjMS00OGNjLThkYTktYWUxMDgxYjQ1N2Y4XkEyXkFqcGdeQXVyNjU0NTI0Nw@@._V1_UY268_CR2,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMjM2NTYxMTE3OV5BMl5BanBnXkFtZTgwNDgwNjgwMzE@._V1_UY268_CR9,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMGFkNjNmZWMtNDdiOS00ZWM3LWE1ZTMtZDU3MGQyMzIyNzZhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZGY5NWUyNDUtZWJhZi00ZjMxLWFmMjMtYmJhZjVkZGZhNWQ4XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNGY2NjNkYjEtY2M5Ni00NzQwLTk1MjctYjEzOWFmNWE2NGZjL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZWQxM2JjNTktYWE4Ni00YmZiLWFlNDEtMWYzMmI4N2NhYjk4XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BOGM5MzU5NTgtMmJjZC00Y2E2LThhZGQtMGE5YzUxZTgwZDdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMzAxNzNmMzMtYTU4Ni00Y2IxLTk4MGEtZGExNmFiMzBjN2MyL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BODQ1MTE5MzY0OV5BMl5BanBnXkFtZTYwMzk1MjI5._V1_UY268_CR2,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTk5NTg2NzM0OV5BMl5BanBnXkFtZTYwNTk5Mjg5._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMjY3Nzk0NzkxMF5BMl5BanBnXkFtZTgwMTYxNzYxMTE@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BNjFjNWNmYWUtZTFlMi00ZDcxLWJkY2MtNjMwYmM0OTc5OTM1XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTY3MzA4NzYyOF5BMl5BanBnXkFtZTYwNjk3Nzc5._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BMTM0OTA1NzY2Ml5BMl5BanBnXkFtZTYwMDI4NDU3._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BZmE1OTg1ZmItNGMyOC00MzA5LTgyMWEtYmE0MzcwNjE3Y2MwXkEyXkFqcGdeQXVyNjU0NTI0Nw@@._V1_UX182_CR0,0,182,268_AL_.jpg",
    "https://m.media-amazon.com/images/M/MV5BOTc4MTJmMzYtYTg4Yy00YTE3LWI5MGQtYTcxYWU2MmIxY2U3XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
]


def create_list(titles):
    hs = []
    for title in titles:
        hs.append(html.H2(title, style={"color": color_palette[0]}))
    return hs


def create_images(image_urls):
    imgs = []
    for url in image_urls:
        imgs.append(html.Img(src=url))
    return imgs


layout = html.Div(
    [
        Row(
            [Col(create_list(titles)), Col(create_images(image_urls))],
            style={
                "margin-top": "4vh",
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "center",
            },
        )
    ],
    style={"height": "100%"},
)

