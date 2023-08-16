import tests
import bot


def main():
    tests.test()
    current_session = bot.Bot()
    current_session.main()


if __name__ == "__main__":
    main()
    # TODO: argparse run props
