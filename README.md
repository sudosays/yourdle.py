# yourdle.py: A local CLI-based Wordle clone

This was written in about 2 hours while procrastinating. It is hacky and
probably prone to errors. Caveat emptor.

Requires Python 3 and (initially) an internet connection to setup the wordlist file.

## Getting started

Run:

``` sh
./yourdle.py
```

On first run it will download and prepare a wordlist into `wordlist-en.txt` roughly ~95KB in size.

### How to play

The feedback from your guesses is a bit minimal. Upper case characters mean that
the character is both correct and in the correct place. Lower case characters
mean that the character is correct, but in the wrong position. An asterisk means
that the character was incorrect.

Example:

1. The secret word is "ISSUE".
2. Your guess is "SCENE".
3. The feedback is `s***E`.

Here 's' is correct, but in the wrong position. 'E' is also correct and in the
correct position.


Some options include:

`--wordfile`: Specify an alternate wordfile to use. Must contain one word per line. It won't complain if there are words longer or shorter than 5 characters. That is up to you.

`--secret`: Provide a secret word to try and guess. Useful for debugging or challenging friends.

## Acknowledgements

Thanks to [ @dwyl ](https://github.com/dwyl/) for the
[english-words](https://github.com/dwyl/english-words/) repository. This project
makes use of `words_alpha.txt` to generate an english wordlist.

Thank you to the alpha testers [@HermanMartinus](https://github.com/HermanMartinus) and Simon. 

## Contributing

I am not planning on accepting any pull requests.

I encourage you to report issues, but above all to fork this and hack on it
yourself. Citation is appreciated, but not necessary.

## FAQ

1. Where is the EXE???

> The use of EXE's is a crutch. This project does not provide one because it has
> your best interests at heart. Hopefully by denying you the convenience of the
> EXE you crave you will come to realise that the EXE was an illusion all along.
> That when it came down to it, it was just a way for the powerful to maintain
> control of your systems by keeping you ignorant and comfortable. Cast off the
> shackles and rediscover how to use your machine. Seize the means of shaping
> your own destiny through knowledge and effort. Embrace discomfort.

2. Why?

> I don't know. I have been musing about how to implement a Wordle clone for a
> while now. It seemed the best way to scratch that itch. I still think there is
> maybe a cool way to implement a tree-like data structure for efficient
> searching/validation of ambiguous length Wordles, but I won't touch it anytime
> soon.

3. I could have done this easily. This doesn't look so hard.

> Please do! I encourage you to implement your own version and let me know.
> Maybe do it in $PROGLANG? Write it in pure x86 assembly? Overengineer it? Do
> it. And you might find that it makes you feel something.
