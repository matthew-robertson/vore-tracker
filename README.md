# vore-tracker
A simple discord bot designed to keep track of however long a server can go without referencing vore.

The bot provides one command: "!vt" which will tell you how long the server has gone without mentioning the word "vore."

The bot also monitors all messages for a message like "vore" (specifically, case-insensitive, ensuring there are word-breaks on either side of the phrase), and will reset the server's counter if it finds a message containing a match after calling out the user publically.
