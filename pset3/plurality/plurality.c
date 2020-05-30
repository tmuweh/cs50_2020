#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);
int compare(const void *a, const void *b);
bool winner_s(int a);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i].name) == 0)
        {
            candidates[i].votes += 1;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{

    //sort array
    qsort(candidates, candidate_count, sizeof(candidate),  compare);

    //print winner(s)
    printf("%s\n", candidates[candidate_count - 1].name);

    //test for other winners
    for (int i = candidate_count - 2; i >= 0; i--)
    {
        if (candidates[i].votes < candidates[candidate_count - 1].votes)
        {
          return;
        }
        printf("%s\n", candidates[i].name);
    }

}
//compare fucntion
int compare(const void *a, const void *b)
{
    candidate value1 = * ((candidate *) a);
    candidate value2 = * ((candidate *) b);

    if (value1.votes > value2.votes)
    {
        return 1;
    }
    if (value1.votes < value2.votes)
    {
        return -1;
    }

    return 0;
}






