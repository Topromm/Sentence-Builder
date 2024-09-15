# Sentence-Builder
Sentence Builder is used for collaborative sentence writing in a designated chat/channel. The Bot has several features to help ensure that the sentences are written correctly and to prevent spamming.

How it all works:
- Set the sentence builder channel and the finished sentences channel using the set_builder_channel and set_finished_channel commands.
- Checks that each message in the sentence builder channel only contain one word and that the sentence ends once someone uses a period.
- Once a valid sentence is completed, the bot sends the sentence to the finished sentences channel along with the author's name(s) and the sentence number.
