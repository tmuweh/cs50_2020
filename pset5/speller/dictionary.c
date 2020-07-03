// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <strings.h>
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
const unsigned int N = 991;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    for (node *tmp = table[hash(word)]; tmp != NULL; tmp = tmp->next)
    {
        if (strcasecmp(tmp->word, word) == 0)
        {
            return true;
        }

    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int sum = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        sum += tolower(word[i]);
    }
    sum *=tolower(word[0]);
    //printf("sum is %d, mode N is %d\n", sum, sum % N);
    return (sum % N);
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    /*//initialize table to
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    */
    char buffer[LENGTH + 1];

    FILE *fp = fopen(dictionary, "r");

    if (fp == NULL)
    {
        return false;
    }

    while ( fscanf(fp, "%s", buffer) != EOF)
    {
        node *n = malloc(sizeof(node));

        //if at any given time, memory isn't  allocated
        if (n == NULL)
        {
            return false;
        }

        //copy buffer into allocated memory
        strcpy(n->word, buffer);

        //store word in hash table
        n->next = table[hash(n->word)];
        table[hash(n->word)] = n;

    }

    //close file
    fclose(fp);
    for (int i = 0; i < N; i++)
    {
        printf("[%i]-> ", i);
        for (node *tmp = table[i]; tmp != NULL; tmp = tmp->next)
        {
            printf(" %s ->", tmp->word);
        }
        printf("\n");
    }
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

    printf("[words %d]", words);
    return words;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i ++)
    {
        while (table[i] != NULL)
        {
           node *tmp = table[i]->next;
           free(table[i]);
           table[i] = tmp;
        }
    }

    return true;
}
