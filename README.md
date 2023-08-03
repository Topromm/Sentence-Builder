# Sentence-Builder
[![license](https://camo.githubusercontent.com/e8d5c98b8acdc98a82b8e1b03c8c256539417ce8eb7199f0e20e50edc50f6d03/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f61707075313233322f446973636f72642d53656c66626f742e7376673f7374796c653d666c61742d737175617265)](https://github.com/Wanrell/Lunabot/blob/main/LICENSE)

A lightweight sentence building game bot written for Discord using Python!

## What does this bot actually do?
Sentence Builder is used for collaborative sentence writing in a designated Discord channel. The bot has several features to help ensure that the sentences are written correctly and to prevent spamming.

The bot has the following capabilities:

- Set the sentence builder channel and the finished sentences channel using the set_builder_channel and set_finished_channel commands.
- Checks that each message in the sentence builder channel only contain one word and that the sentence ends once someone uses a period.
- Once a valid sentence is completed, the bot sends the sentence to the finished sentences channel along with the author's name(s) and the sentence number.
