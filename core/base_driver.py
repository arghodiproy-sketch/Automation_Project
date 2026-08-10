"""
core/base_driver.py — Abstract Base Driver.

Interview Tip:
    ABC (Abstract Base Class) is a key OOP concept.
    Declaring abstract methods means every subclass MUST implement them.
    This enforces the Liskov Substitution Principle: anywhere a
    BaseDriver is expected, any concrete driver (Desktop/Mobile/Web)
    can be used interchangeably.

    Common interview question:
        "What is the difference between an abstract class and an interface?"
        Python has no interface keyword; ABCs serve the same purpose.
"""

from abc import ABC, abstractmethod


class BaseDriver(ABC):
    """
    Contract that every platform driver must fulfil.

    Subclasses:
        DesktopDriver  →  pywinauto
        MobileDriver   →  Appium
        WebDriver      →  Selenium
    """

    @abstractmethod
    def start(self):
        """
        Launch the application / browser / session.

        Returns:
            The driver or window handle to be passed to Page Objects.
        """
        ...

    @abstractmethod
    def quit(self):
        """
        Cleanly close the app / browser / session.
        Always called in fixture teardown (the 'finally' equivalent).
        """
        ...
