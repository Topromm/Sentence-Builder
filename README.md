# Sentence-Builder

A lightweight sentence building game bot written for Discord using Python!

## What does this bot actually do?
Sentence Builder is used for collaborative sentence writing in a designated Discord channel. The bot has several features to help ensure that the sentences are written correctly and to prevent spamming.

The bot has the following capabilities:

- Set the sentence builder channel and the finished sentences channel using the set_builder_channel and set_finished_channel commands.
- Checks that each message in the sentence builder channel only contain one word and that the sentence ends once someone uses a period.
- Once a valid sentence is completed, the bot sends the sentence to the finished sentences channel along with the author's name(s) and the sentence number.
