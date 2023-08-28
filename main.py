import bot


def main():
    current_session = bot.Bot()
    current_session.main()


if __name__ == "__main__":
    main()
# TODO: add music downloading
# TODO: improve photo downloading by creating database with |filename|: |type{sender_id}_{id}|
# TODO: make realization of -load-only-docs