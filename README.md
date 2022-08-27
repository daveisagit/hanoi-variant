# hanoi-variant
Inspired by MathsJam shout July 2022 we made a problem for ourselves.

A variant of the Towers of Hanoi, except that a ring can only be placed on another
ring if it is the immediate predecessor. i.e. ring 4 can only be on ring 5 or on a base.

[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/OyEpxcxX_Bk/0.jpg)](http://www.youtube.com/watch?v=OyEpxcxX_Bk)

## Maximum Number of Rings
Let **R(p)** be maximum number of rings you can solve it for when using **p** poles.

We split the pile into 2 (not necessarily equal groups) Upper(**U**) and Lower(**L**) such that it is 
possible to move the Upper group onto a different pole using some sequence of moves

Let **U(p)** and **L(p)** be maximum number of rings we can do this for with **p** poles


- R(p) = U(p) + L(p)

Convince yourself that 

- **L(p) = R(p-1)** _as it is effectively the same problem but with 1 less pole._

- **U(p) = 2 x U(p-1)** _Split U into A & B and use a similar argument for A(p),B(p)_

Then it only goes to show given U(p-1) = R(p-1) - L(p-1) 

- R(p) = 2 x [ R(p-1) - L(p-1) ]  + R(p-1)

and since L(p-1) = R(p-2)

- R(p) = 3R(p-2) - 2R(p-2)

We know R(1)=0 and R(2)=1, so the first few terms are

| Poles (**p**)      |     1     |       2 | 3   | 4   | 5   | 6 |
|--------------------|:---------:|--------:|-----|-----|-----|---|
| Max Rings **R(p)** | 0 | 1 | 3   | 7   | 15  |31|

You can prove by induction that R(p) = 2 ** (p-1) - 1

[Here](https://docs.google.com/document/d/1QAWLkAg6UvP5uxFRO2-lsh0sMqImcpjuWqKgZgnwfmA/edit?usp=sharing)
is an easier document to read as markdown does not render subscripts and also gives a fuller explanation.
## Algorithm
So we have a maximum, but what does the algorithm look like?

It follows the same recursive structure as the argument for the maximum rings as described
by the code and seen in the videos, a nice analogy is the 2048 game.

## Sample Videos

[4 Poles](https://youtu.be/OyEpxcxX_Bk)

[5 Poles](https://youtu.be/sgeHreqfI4w)

[6 Poles](https://youtu.be/7RxftPVYauw)

[7 Poles](https://youtu.be/JYb1_TlOaW0)