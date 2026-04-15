# Shuttle Stop Crowding Ranking using Merge Sort

def merge_sort(stops):       # sort the list using merge sort
    if len(stops) <= 1:    # if there is 1 or 0 items, it is already sorted
        return stops      # return the sorted list

    middle = len(stops) // 2      # find the middle of the list
    left_side = stops[:middle]  # take the left half
    right_side = stops[middle:]       # take the right half

    left_side = merge_sort(left_side)  # sort the left half
    right_side = merge_sort(right_side)     # sort the right half

    return merge(left_side, right_side)    # merge the 2 sorted halves together


def merge(left, right):   # combine 2 sorted lists into 1 sorted list
    new_list = []     # make a new empty list
    i = 0          # starting index for the left list
    j = 0        # starting index for the right list

    while i < len(left) and j < len(right): # keep comparing while both lists still have items
        if left[i][1] < right[j][1]:      # compare the crowd counts
            new_list.append(left[i])    # add the smaller left item
            i = i + 1        # move to the next left item
        else:
            new_list.append(right[j])         # add the smaller right item
            j = j + 1           # move to the next right item

    while i < len(left):       # if items are left in the left list
        new_list.append(left[i])      # add them to the new list
        i = i + 1        # move forward in the left list

    while j < len(right):      # if items are left in the right list
        new_list.append(right[j])    # add them to the new list
        j = j + 1      # move forward in the right list

    return new_list        # return the merged sorted list


def format_stops(stops):       # make the stops look nicer in the output
    pieces = []             # store each stop as formatted text

    for stop in stops:            # go through each stop in the list
        pieces.append(f"{stop[0]} ({stop[1]})")     # format it like Name (count)

    return " | ".join(pieces)      # join all stops with lines between them


import gradio as gr       # import gradio for the interface

def sort_input(text):      # process the user's input
    lines = text.split("\n")     # split the input into separate lines
    stops = []                # make an empty list for the stops

    for line in lines:        # go through each line
        if line.strip() == "":        # check if the line is empty
            continue                # skip empty lines

        parts = line.split(",")      # split the line by the comma

        if len(parts) != 2:        # make sure there are exactly 2 parts
            return "please use correct format: stop name, crowd count"

        stop_name = parts[0].strip()     # get the stop name and remove extra spaces

        if stop_name == "":    # make sure the stop name is not blank
            return "please enter a stop name."

        try:
            crowd_count = int(parts[1].strip())        # turn the crowd count into an integer
        except:
            return "please make crowd count a whole number."

        if crowd_count < 0:         # make sure the crowd count is not negative
            return "crowd count cannot be negative."

        stops.append((stop_name, crowd_count))  # add the stop as a tuple to the list

    if len(stops) == 0:        # check if the user entered no valid stops
        return "please enter at least one shuttle stop."

    sorted_stops = merge_sort(stops)         # sort the stops using merge sort

    output = "## Shuttle Stop Crowd Ranking\n\n"    # make the title for the output
    output += "**Original list:**  \n"       # label for the original list
    output += format_stops(stops) + "\n\n"       # show the original list

    output += "**Sorted list:**  \n"       # label for the sorted list
    output += format_stops(sorted_stops) + "\n\n"      # show the sorted list

    output += "### Final Ranking\n"           # add a heading for the ranking

    rank = 1           # start the ranking at 1
    for stop in sorted_stops:            # go through the sorted stops
        output += f"{rank}. {stop[0]} ({stop[1]})  \n" # add each stop with its rank
        rank = rank + 1            # move to the next rank number

    return output         # return the final formatted output


app = gr.Interface(
    fn=sort_input,          # use the sort_input function
    inputs=gr.Textbox(       # make the input box
        lines=8,        # make the box 8 lines tall
        label="Enter shuttle stops",     # label for the input
        placeholder="ARC, 67\nBioSci, 50\nStauffer, 99\nBus Loop, 12"
    ),
    outputs=gr.Markdown(label="Sorted output"),  # show the result as markdown
    title="Marcus DeMello's Shuttle Stop Crowd Ranking" # title of the app
)

app.launch()   # launch the app
