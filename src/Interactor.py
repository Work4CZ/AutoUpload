import curses
from typing import List, Union


class RepeatCallError(Exception):
    pass


class CommandLineInteractor():

    def __init__(self):
        self._is_initialized = False
        self.stdscr = curses.initscr()
        self.height, self.width = self.stdscr.getmaxyx()
        self.static_cursor = 0
        # 最后一行用于输入，倒数第二行显示错误信息
        self.error_line = self.height - 2
        self.input_line = self.height - 1

        self.status_line = self.height - 3

        self.display_message(self.static_cursor, "-" * self.width)
        self.static_cursor += 1

        self.display_static_prompt(
            "Enter a following command to select the function:".ljust(
                self.width - 4))
        self.display_static_prompt("Template, Swap, Copy".center(self.width -
                                                                 4))
        self.display_message(self.static_cursor, "-" * self.width)
        self.static_cursor += 1

        self._is_initialized = True

    def __del__(self):
        curses.endwin()

    def get_input(self, prompt: str = None) -> str:
        # Print the prompt at the bottom of the screen
        if prompt:
            self.display_message(self.input_line, prompt)
        # Get the user input
        else:
            self.stdscr.move(self.input_line, 0)
        return self.stdscr.getstr().decode()

    def display_message(self, line: int, message):
        self.stdscr.addstr(line, 0, message)
        self.stdscr.refresh()

    def display_static_prompt(self, prompts: Union[List[str], str]):
        """
        Display a static prompt to the user.
        """
        if self._is_initialized:
            raise RepeatCallError(
                "display_static_prompt can only be called once.")
        if type(prompts) is str:
            self.display_message(self.static_cursor, "| " + prompts + " |")
            self.static_cursor += 1
        elif isinstance(prompts, list) and all(
                isinstance(prompt, str) for prompt in prompts):
            for prompt in prompts:
                self.display_message(self.static_cursor, "| " + prompt + " |")
                self.static_cursor += 1
        else:
            raise TypeError(
                "display_static_prompt accepts only list[str] and str as arguments"
            )

    def display_dynamic_info(self, info: str):
        # Display the dynamic info in the middle of the screen
        self.display_message(self.status_line, info)

    def report_error(self, error):
        # Display the error message in the middle of the screen
        self.display_message(self.error_line, f"ERROR: {error}")


tui = CommandLineInteractor()
