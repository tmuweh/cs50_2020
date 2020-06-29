// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 1801;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    int sum = 0;
    for (int i = 0; i != '\0'; i++)
    {
        sum += tolower(word[i]);
    }
    //multiply by the ascii value of the first char in the word;
    sum *= word[0];

    return sum % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    char buffer[LENGTH + 1];

    FILE *fp = fopen(dictionary, "r");

    if (fp == NULL)
    {
        return false;
    }

    while ( fscanf(fp, "%s", buffer) != EOF)
    {
        node *word = malloc(sizeof(node));

        //if at any given time, memory isn't  allocated
        if (word == NULL)
        {
            return false;
        }
        //first element into the hash table
        if ((table[hash(buffer)]) == NULL)
        {
            table[hash(buffer)] = word;
            word->next = NULL;
        }

        //adding new words at the begining of the linked list
        word->next = table[hash(buffer)];
        table[hash(buffer)] = word;


    }

    //close file
    fclose(fp);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{

    //numbers of words/nodes
    int words = 0;
    //loop through hash table
    for (int i = 0; i < N; i ++)
    {
        //for array pointer to a link list
        for (node *tmp = table[i]; tmp != NULL; tmp = tmp->next)
        {
            //counts nodes/words
            words++;
        }
    }
    return words;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    return false;
}
