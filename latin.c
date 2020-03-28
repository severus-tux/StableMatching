#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
 
/*
 * rls.c
 *
 * A straightforward implementation of the algorithm by Jacobson and 
 * Matthews, _Generating uniformly distributed random Latin square_,
 * Journal of Combinatorial Design, 1996.
 *
 * I actually couldn't find the original paper, so this is an implementation
 * based upon other descriptions of the algorithm.
 *
 * Written by Mark VandeWettering.
 *
 */
 
 
#define DIM (10)
 
typedef struct t_incidence_cube {
    int s[DIM][DIM][DIM] ;
} IncidenceCube ;
 
 
void
InitIncidenceCube(IncidenceCube *c)
{
    int i, j, k ;
 
    /* First, zero the cube */
    for (i=0; i<DIM; i++)
        for (j=0; j<DIM; j++)
            for (k=0; k<DIM; k++)
                c->s[i][j][k] = 0 ;
 
    /* And then dump ones in the right place... */
    for (i=0; i<DIM; i++)
        for (j=0; j<DIM; j++)
            c->s[i][j][(i+j)%DIM] = 1 ;
}
 
void
PrintIncidenceCube(IncidenceCube *c)
{
    int i, j, k ;
 
    for (i=0; i<DIM; i++) {
        for (j=0; j<DIM; j++) {
            for (k=0; k<DIM; k++) {
                if (c->s[i][j][k]) {
                    printf("%2d ", k+1) ;
                    break ;
                }
            }
        }
        printf("\n") ;
    }
    printf("\n") ;
}
 
void
CompactPrintIncidenceCube(IncidenceCube *c)
{
    int i, j, k ;
 
    for (i=0; i<DIM; i++) {
        for (j=0; j<DIM; j++) {
            for (k=0; k<DIM; k++) {
                if (c->s[i][j][k]) {
                    printf("%01d", k+1) ;
                    break ;
                }
            }
        }
    }
    printf("\n") ;
}
 
void
ShuffleIncidenceCube(IncidenceCube *c)
{
    int i, j ;
 
    for (i=0; i<DIM*DIM*DIM; i++) {
         
        // Assume we have a "proper" matrix...
        
        // Pick a random zero from the incidence cube... 
        int rx, ry, rz ;
        do {
            rx = lrand48() % DIM ;
            ry = lrand48() % DIM ;
            rz = lrand48() % DIM ;
        } while (c->s[rx][ry][rz]) ;
 
        int ox, oy, oz ;
 
        for (j=0; j<DIM; j++) {
            if (c->s[j][ry][rz] == 1)
                ox = j ;
            if (c->s[rx][j][rz] == 1)
                oy = j ;
            if (c->s[rx][ry][j] == 1)
                oz = j ;
        }
 
        // do the +/- 1 move...  
        // These are all square with zeros in them...
        c->s[rx][ry][rz] ++ ;
        c->s[rx][oy][oz] ++ ;
        c->s[ox][ry][oz] ++ ;
        c->s[ox][oy][rz] ++ ;
 
        // These all have ones, except for maybe the last one...
        c->s[rx][ry][oz] -- ;
        c->s[rx][oy][rz] -- ;
        c->s[ox][ry][rz] -- ;
        c->s[ox][oy][oz] -- ;
 
        while (c->s[ox][oy][oz] < 0) {
 
            rx = ox ;
            ry = oy ;
            rz = oz ;
 
            // Pick one of the two 1's that are in conflict
            if (drand48() < 0.5) {
                for (j=0; j<DIM; j++) {
                    if (c->s[j][ry][rz] == 1) {
                        ox = j ;
                    }
                }
            } else {
                for (j=DIM-1; j>=0; j--)  {
                    if (c->s[j][ry][rz] == 1) {
                        ox = j ;
                    }
                }
            }
 
            if (drand48() < 0.5) {
                for (j=0; j<DIM; j++) {
                    if (c->s[rx][j][rz] == 1) {
                        oy = j ;
                    }
                }
            } else {
                for (j=DIM-1; j>=0; j--)  {
                    if (c->s[rx][j][rz] == 1) {
                        oy = j ;
                    }
                }
            }
 
            if (drand48() < 0.5) {
                for (j=0; j<DIM; j++) {
                    if (c->s[rx][ry][j] == 1) {
                        oz = j ;
                    }
                }
            } else {
                for (j=DIM-1; j>=0; j--)  {
                    if (c->s[rx][ry][j] == 1) {
                        oz = j ;
                    }
                }
            }
           
            // do the +/- 1 move...  
            // These are all square with zeros in them...
            c->s[rx][ry][rz] ++ ;
            c->s[rx][oy][oz] ++ ;
            c->s[ox][ry][oz] ++ ;
            c->s[ox][oy][rz] ++ ;
 
            // These all have ones, except for maybe the last one...
            c->s[rx][ry][oz] -- ;
            c->s[rx][oy][rz] -- ;
            c->s[ox][ry][rz] -- ;
            c->s[ox][oy][oz] -- ;
        }
 
    }
}
 
int
main(int argc, char *argv[])
{
    IncidenceCube c ;
    int i ;
    int x = atoi(argv[1]);
    srand48(getpid()) ;
    InitIncidenceCube(&c) ;
    ShuffleIncidenceCube(&c) ;
    PrintIncidenceCube(&c) ;
    return 1 ;
}