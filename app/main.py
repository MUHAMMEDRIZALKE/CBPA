import logging

from app.bot.runner import run_bot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

def main():
    run_bot()


if __name__ == "__main__":
    main()
