# df-combat-clicker

-Check out the game itself on [the official site](https://dragonfable.com).

-All rights belong to the amazing developers and Artix Entertainment.

## clicker.py

-Script for automated clicking to farm gold in DragonFable, used for ChaosWeaver in the Ninja Arena quest.

-Mostly timing based using a quick rotation based on the number of opponents, requires the game to be open as a window, and be on top.

-Prone to breaks either duo to flash being laggy or network delays, honestly, unless you would want to leave it on for the night or something, you're better off doing it manually.

-Simply run from command line, then swap to the game window, ready to start the quest. The magic constants are entirely based upon window size, so feel free to just convert them into ratios then compute them for yourself based on your window's parameters. Alas' I'm lazy for that.

## reckoning.py

-Script for automated clicking to defeat waves in the reckoning war event with the doomknightV2 class (requires you to be able to clear any opponent with just doom spikes)

-Mostly timing based, but since it uses the win32api click events instead of direct actual clicks no longer requires the window to be on top or active.

-Finds the game window by title, requires the window to forward click inputs to the relevant controls
