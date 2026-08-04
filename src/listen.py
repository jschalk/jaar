from ch90_puncher_app.puncher_app import ETLApp


def listen_main():
    """Entry point for the keg2 listen CLI."""
    ETLApp().mainloop()


if __name__ == "__main__":
    listen_main()
