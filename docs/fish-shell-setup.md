# Fish Shell + Oh My Posh  

:leftwards_arrow_with_hook: [python-cybersecurity-tools](../README.md)

## Installation Notes & Common Customizations

This document summarizes the installation steps, configuration, and common questions/issues encountered while setting up **Fish shell** with **Oh My Posh**, including customization of the welcome message.

---

## 1. Fish Shell Installation

Install Fish shell using your system package manager.

Example (Debian / Ubuntu):

```bash
sudo apt install fish
```
Verify installation:

```bash
fish --version
```
(Optional) Set Fish as the default shell:
```bash
chsh -s (which fish)
```

Log out and back in for the change to take effect.

---

## 2. Oh My Posh Installation (Fish)

After installing Oh My Posh, initialize it inside Fish.

Edit the Fish configuration file:

nano ~/.config/fish/config.fish


Add:

oh-my-posh init fish --config ~/.poshthemes/paradox.omp.json | source


List available themes:

oh-my-posh theme list

## 3. Default Fish Greeting Issue

By default, Fish displays:

Welcome to fish, the friendly interactive shell
Type help for instructions on how to use fish

Solution: Disable the Default Greeting

Add the following line to config.fish:

set fish_greeting


This removes the default welcome message.

## 4. Custom Dynamic Greeting (User + Date + Phrase)

A custom greeting can be created using Fish functions.

Requirements

fortune package (for random phrases)

Install fortune:

Debian / Ubuntu:

sudo apt install fortune


Arch:

sudo pacman -S fortune-mod

## 5. Fish Greeting Function

To display:

Current username

Current date (weekday, day-month)

A random programming-related phrase

A line break between greeting and phrase

Add this function to config.fish:

function custom_greeting
    set username (whoami)
    set today (date "+%A, %d-%b")
    set phrase (fortune | head -n 1)

    set fish_greeting "Hello, $username! Today is $today.\n$phrase"
end

custom_greeting

## 6. Common Questions & Clarifications
❓ Can Fish use functions like fortune?

Yes. Fish can execute any available system command inside variables and functions.

❓ How to add a line break in the greeting?

Use \n inside the fish_greeting string.

❓ Why define a function instead of a single line?

Functions allow:

Cleaner logic

Easier customization

Reuse and expansion later

## 7. Notes

fish_greeting must be set after any logic that builds the message.

If fortune is not installed, the greeting will fail silently.

Restart the terminal after modifying config.fish.

## 8. Status

✔ Fish installed
✔ Oh My Posh initialized
✔ Default greeting removed
✔ Dynamic greeting implemented