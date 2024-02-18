import time

import typer
import libtmux
import rich


class TmuxSession:
    """Class to manage Tmux sessions for running commands."""

    COLORS = [
        "turquoise2",
        "deep_sky_blue2",
        "dodger_blue1",
        "steel_blue",
        "medium_purple",
        "light_slate_blue",
        "blue_violet",
        "dark_violet",
    ]

    def __init__(self, session_prefix, session_count, cmd):
        self.session_prefix = session_prefix.replace(" ", "_").replace(".", "_")
        self.session_count = session_count
        self.cmd = f"python3 {cmd}" if cmd.endswith(".py") else cmd
        self.server = libtmux.Server()
        self.target_sessions = []
        self.session_colors = [
            self.COLORS[i % len(self.COLORS)] for i in range(session_count)
        ]
        self.last_logs = [""] * session_count

    def __enter__(self):
        self._cleanup_sessions()
        self._create_sessions()
        return self

    def _cleanup_sessions(self):
        """Clean up existing sessions with the same prefix."""
        for session in self.server.sessions:
            if session.name.startswith(self.session_prefix):
                session.kill_session()

    def _create_sessions(self):
        """Create new Tmux sessions."""
        for i in range(self.session_count):
            session_name = f"{self.session_prefix}_{i}"
            session = self.server.new_session(
                session_name=session_name, kill_session=True
            )
            self.target_sessions.append(session)
            session.windows[0].attached_pane.send_keys(self.cmd)

    def logs(self, log_all=False):
        """Print logs from all sessions."""
        for i, session in enumerate(self.target_sessions):
            pane = session.windows[0].attached_pane
            stdout = pane.cmd("capture-pane", "-p").stdout
            if log_all:
                colored_session_name = f"[{self.session_colors[i]}]{session.name}[/{self.session_colors[i]}]"
                rich.print(colored_session_name, "\n".join(stdout))
            elif stdout[-1] != self.last_logs[i]:
                colored_session_name = f"[{self.session_colors[i]}]{session.name}[/{self.session_colors[i]}]"
                rich.print(colored_session_name, stdout[-1])

            self.last_logs[i] = stdout[-1]

    def __exit__(self, exc_type, exc_value, traceback):
        for session in self.target_sessions:
            session.kill_session()


app = typer.Typer()


@app.command()
def main(cmd: str, count: int = typer.Option()):
    """Main function to handle the command line interface."""
    with TmuxSession(cmd, count, cmd) as tmux:
        first_time = True
        while True:
            time.sleep(1)
            tmux.logs(log_all=first_time)
            first_time = False


if __name__ == "__main__":
    app()
