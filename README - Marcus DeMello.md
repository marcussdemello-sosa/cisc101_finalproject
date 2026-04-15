# Algorithm Name: Shuttle Stop Crowding Ranking using Merge Sort

## Demo video/gif/screenshot of test

## Problem Breakdown & Computational Thinking

### Chosen Problem:
I must organize shuttle stops based off how crowded they are. Each shuttle stop comes with a name and a crowd count. The goal is to sort the stops so that I can see which stops are the most crowded.

### Chosen Algorithm:
I've selected to go with Merge Sort.  It works by splitting a list into smaller parts, and then sorting those parts, and then merging them back together in order.  

### Why Merge Sort Fits the Problem
Each shuttle stop has a crowd count that can be compared easily, so merge sort fits the problem well.  It's also able to easily display how the list was sorted and merged, making it easy for users to understand the process.

### Assumptions & Preconditions
-shuttle stops have valid names

-each crowd count is an integer

-the list doesn't need to be sorted before running the algorithm

### Decomposition:
-take the user input which includes stop names & crowd counts

-put that data into a list

-merge sort the list in order of crowd counts

-display each of the steps of the sorting process

-display the final sorted list

### Pattern Recognition:

-repeatedly splitting list into smaller ones

-compares elements and then merges them back in order

-continue until the full list is sorted

### Abstraction

-I only need to show the important steps such as splitting & merging

-hide things like memory or recursion depth

-focusing on how the list changes during sorting

### Algrithm Design

Input: shuttle stops and crowd counts

Process: 

-store data in list 

-sort into smaller parts 

-compare crowd counts

-merge lists back together in sorted order

Output: Sorted list of shuttle stops ranging lowest to highest crowd

### Flowchart

![Flowchart](flowchart.png)

## Steps to Run

1. install python
2. install gradio using pip3 install gradio
3. run the program using: python3 app.py
4. open link from terminal
5. enter shuttle stops in correct format: name, number

## Hugging Face Link

## Author & AI Acknowledgment
Author: Marcus DeMello
AI Disclosure:  AI such as ChatGPT was used to debug code, help with structuring, help with efficiency, and provide new ideas.  All final changes, testing, and modifications were done by me.	