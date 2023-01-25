# Overview
This is a script to find solutions of the [Brainvita puzzle](https://en.wikipedia.org/wiki/Peg_solitaire) by brute force.

This code is not optimized. It just explores all possible optoions at every stage until a solution is found. If a solution is not found, it backtracks and goes down a different path. It keeps doing this until the target number of solutions are found.

If you run this with a compute_solutions flag, then it computes the solutions and writes the solutions to solutions.json file. The next time you run it without the compute_solutions flag, it just reads the solutions off the file. You can provide a solution number to be shown to you visually.

If you run this without the compute_solutions flag, and there is no "solutions.json" file to read from, then the tool computes the solutions and creates the file.

# How to run
Just run it as below

```
python3 find_solutions.py
```

By default it stops after 100 solutions are found. The solutions are written to solutions.json. It is just an array of arrays. Each sub-array is a solution, and each dict within the sub-array is a move. The structure of the file is given below. A move is a dict containing the (zero indexed) row and column number of the marble to be moved and the direction it is to be moved in,.

```
[
    [        
        {
            "row": 0,
            "col": 2,
            "direction": "down"
        }
    .
    .
    .
    ],
    [
        {
            "row": 0,
            "col": 4,
            "direction": "down"
        },
    .
    .
    .
    
    ]
]
```

Once the file is ready you can view any solution that you want with a command like this:
```
python3 find_solutions.py --solution_num 55
```
