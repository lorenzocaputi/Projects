#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    string name;
    int votes;
    bool eliminated;
}
candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

//--------------------------------

    // Keep querying for votes

    // for each voter (i)
    for (int i = 0; i < voter_count; i++)
    {

        // For (n° candidates) times
        for (int j = 0; j < candidate_count; j++)
        {
            // get the 1st, 2nd, 3rd... rank
            string name = get_string("Rank %i: ", j + 1);

            // Record vote, unless it's invalid
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }
    return 0;
}

// Record preference if vote is valid
bool vote(int voter, int rank, string name)
{
    // 1st voter - 1st rank;  1st voter - 2nd rank...

    //iterate over the candidates's names and see if 'name' matches any of them
    for (int i = 0; i < candidate_count; i++)
    {
        //if it's a match
        if (strcmp(name, candidates[i].name) == 0)
        {
            // update preferences
            preferences[voter][rank] = i;
            return true;
        }

    }

    // if no match
    return false;
}


// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    // I have the preference global array {preference[voter][rank]}

    int choice;
    //iterate over each voter and add one to their top choice candidate if not eliminated
    for (int i = 0; i < voter_count; i++)
    {
        // loop through their choices
        for (int j = 0; j < candidate_count; j++)
        {
            choice = preferences[i][j];
            
            // add 1 to the first one that's not been eliminated and break
            if (!candidates[choice].eliminated)
            {
                candidates[choice].votes += 1;
                break;
            }
        }

    }

}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    // check if any candidates.votes has more than half of voter.count, they win
    for (int i = 0; i < candidate_count; i++)
    {
        //if more than 50%
        if (candidates[i].votes > voter_count / 2)
        {
            printf("%s\n", candidates[i].name);
            return true;
        }
    }

    //if no winner yet
    return false;
}


// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    // loop through the candidates and find the minimum votes total for a non elminated candidate

    int minIndex;
    // find the index of the first guy who's not been eliminated (minIndex)
    for (int j = 0; j < candidate_count; j++)
    {
        if (!candidates[j].eliminated)
        {
            minIndex = j;
        }
    }

    //update minIndex with the real minIndex
    for (int i = 0; i < candidate_count; i++)
    {
        if (!candidates[i].eliminated && candidates[i].votes < candidates[minIndex].votes)
        {
            minIndex = i;
        }
    }

    //return the min votes
    return candidates[minIndex].votes;

}


// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    // loop through the candidates and see if any candidates[x].votes is different and they're not eliminated

    for (int i = 0; i < candidate_count; i++)
    {
        if (!candidates[i].eliminated && candidates[i].votes > min)
        {
            return false;
        }
    }

    //if they're all the same
    return true;
}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min)
{
    // set candidates[i].eliminated to true if their votes is the minimum
    for (int i = 0; i < candidate_count; i ++)
    {
        if (!candidates[i].eliminated && candidates[i].votes == min)
        {
            candidates[i].eliminated = true;
        }
    }
}
