# StableMatching
algorithms in stable matchings

```
galeshaply_all.py <n> <seed>
```

This program can be used for :
- Generating random preference list for n men n women
- Generating all possible stable matchings for this preference list
- Analyzing rotations and drawing H(M) for a given stable matching
- Plotting the whole lattice of stable matchings


#### Some of the stable marriage matching lattice plotted (random preference lists):
![n=30, number of stable matching = 7](https://github.com/severus-tux/StableMatching/blob/master/images/image2.png)

![n=30, number of stable matching = 11](https://github.com/severus-tux/StableMatching/blob/master/images/image3.png)

![n=30, number of stable matching = 50](https://github.com/severus-tux/StableMatching/blob/master/images/image4.png)

Sample Run:
```
[user@system StableMatching]$ python galeshaply_all.py 10

Enter your choice:
1) Random SM instance
2) Random SM instance with disjoint M0 and Mz
3) Random SM instance where preference lists are latin squares
: 1

seed: 47827303

Mens List:

0 -> [9, 5, 0, 7, 6, 8, 1, 4, 3, 2]
1 -> [4, 2, 9, 1, 6, 3, 0, 8, 7, 5]
2 -> [6, 5, 9, 8, 0, 2, 7, 1, 4, 3]
3 -> [7, 9, 1, 2, 0, 3, 8, 5, 6, 4]
4 -> [1, 8, 4, 7, 3, 2, 9, 5, 6, 0]
5 -> [7, 2, 6, 3, 0, 8, 9, 5, 4, 1]
6 -> [7, 9, 2, 8, 0, 4, 1, 5, 3, 6]
7 -> [3, 7, 5, 6, 9, 4, 2, 1, 0, 8]
8 -> [6, 3, 2, 4, 1, 8, 7, 5, 0, 9]
9 -> [5, 4, 7, 2, 9, 3, 0, 8, 1, 6]

Womens List:

0 -> [0, 6, 7, 3, 9, 1, 5, 2, 4, 8]
1 -> [0, 2, 1, 9, 8, 4, 7, 6, 3, 5]
2 -> [0, 5, 1, 8, 3, 2, 6, 4, 9, 7]
3 -> [4, 0, 2, 6, 5, 9, 8, 7, 3, 1]
4 -> [3, 8, 4, 2, 9, 6, 7, 5, 1, 0]
5 -> [0, 2, 8, 4, 6, 9, 1, 7, 5, 3]
6 -> [1, 4, 7, 9, 5, 6, 8, 0, 3, 2]
7 -> [5, 2, 0, 3, 7, 6, 9, 1, 8, 4]
8 -> [5, 4, 8, 7, 0, 6, 3, 1, 2, 9]
9 -> [8, 2, 0, 7, 4, 6, 1, 5, 3, 9]


Total number of matchings:  9
M0 -> (9, 2, 5, 0, 1, 7, 8, 3, 6, 4)
M1 -> (5, 2, 9, 0, 1, 7, 8, 3, 6, 4)
M2 -> (9, 2, 5, 0, 1, 7, 8, 6, 3, 4)
M3 -> (5, 2, 9, 0, 1, 7, 8, 6, 3, 4)
M4 -> (9, 2, 5, 0, 1, 7, 8, 6, 4, 3)
M5 -> (5, 2, 9, 0, 1, 7, 8, 6, 4, 3)
M6 -> (9, 2, 5, 4, 8, 7, 0, 6, 1, 3)
M7 -> (5, 2, 9, 4, 8, 7, 0, 6, 1, 3)
M8 -> (5, 2, 1, 4, 8, 7, 0, 6, 9, 3)

Rotations: 
ρ0 -> (2, 0)
ρ1 -> (8, 7)
ρ2 -> (8, 9)
ρ3 -> (6, 3, 8, 4)
ρ4 -> (8, 2)

Mens MGS-List:
0 -> [9, 5, 0, 8, 1, 3, 2]
1 -> [2, 1, 6]
2 -> [5, 9, 1, 4, 3]
3 -> [0, 4]
4 -> [1, 8, 4, 3, 6]
5 -> [7, 2, 6, 3, 8]
6 -> [8, 0, 3, 6]
7 -> [3, 6, 0, 8]
8 -> [6, 3, 4, 1, 8, 9]
9 -> [4, 3, 1, 6]

Womens MGS-List:

0 -> [0, 6, 7, 3]
1 -> [0, 2, 1, 9, 8, 4]
2 -> [0, 5, 1]
3 -> [4, 0, 2, 6, 5, 9, 8, 7]
4 -> [3, 8, 4, 2, 9]
5 -> [0, 2]
6 -> [1, 4, 7, 9, 5, 6, 8]
7 -> [5]
8 -> [5, 4, 8, 7, 0, 6]
9 -> [8, 2, 0]

[user@system StableMatching]$ 
```
![n=30, number of stable matching = 50](https://github.com/severus-tux/StableMatching/blob/master/images/image5.png)

![n=30, number of stable matching = 50](https://github.com/severus-tux/StableMatching/blob/master/images/image6.png)
