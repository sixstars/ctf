# Braid

In short, this challange is about Conjugacy Search Problem in [Braid Group](https://en.wikipedia.org/wiki/Braid_group). 

The key point is that the *Ultra Summit Sets* for given `x` and `c0` are likely to be small when random braids are formed by multiplying randomly chosen permutation braids. 
I refered to ["A FAST ALGORITHM TO THE CONJUGACY PROBLEM"](https://pdfs.semanticscholar.org/b4ea/35f8c157d3799c2dae05d7a0d46def815818.pdf) for this property.
Thus you can just keep *cycling* `x,c0` and record the path. If you find one joint element for these two sets, the recorded path will give you the conjugacy element.

More details can be found in `solve.py`. Unfortunately as usual, the script is in a mess. Some parts have been rewritten several times during competition and test code not removed.

I think the main difficulty is that there are too many papers about solving Conjugacy Search Problem, several of which look like reasonable for our task and cannot be filtered out by reading abstract and introduction only. I spent 10+ hours and mostly on searching and reading papers. (In fact you can even find some implementations of another paper in my script lol)
