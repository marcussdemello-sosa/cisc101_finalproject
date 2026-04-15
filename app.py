import gradio as gr


def format_stops(stops):
    pieces = []  # this makes a list to store each stop as text

    for stop in stops:
        pieces.append(f"{stop[0]} ({stop[1]})")  # adds stop name and crowd count together

    return " | ".join(pieces)  # joins everything with | between each stop


def format_group_numbers(stops):
    pieces = []  # this stores only the crowd numbers

    for stop in stops:
        pieces.append(str(stop[1]))  # takes just the number part from each stop

    return "[" + ", ".join(pieces) + "]"  # puts the numbers in brackets


def format_numbers_line(stops):
    pieces = []  # this stores the numbers for one line

    for stop in stops:
        pieces.append(str(stop[1]))  # adds each number as text

    return " | ".join(pieces)  # joins the numbers with |


def merge(left, right):
    new_list = []  # this will hold the merged sorted list
    i = 0  # pointer for the left list
    j = 0  # pointer for the right list

    while i < len(left) and j < len(right):  # keep going while both lists still have items
        if left[i][1] <= right[j][1]:  # compare the crowd counts
            new_list.append(left[i])  # add the smaller one from left
            i = i + 1  # move left pointer forward
        else:
            new_list.append(right[j])  # add the smaller one from right
            j = j + 1  # move right pointer forward

    while i < len(left):  # if left list still has items
        new_list.append(left[i])  # add them to the end
        i = i + 1  # move pointer forward

    while j < len(right):  # if right list still has items
        new_list.append(right[j])  # add them to the end
        j = j + 1  # move pointer forward

    return new_list  # return the finished merged list


def get_divide_levels(stops):
    levels = []  # stores every level of splitting
    current_level = [stops]  # start with the full list

    while True:
        levels.append(current_level)  # save the current split level
        all_single = True  # assume all groups are size 1
        next_level = []  # this will store the next split

        for group in current_level:
            if len(group) > 1:  # if the group can still be split
                all_single = False  # not at the end yet
                middle = len(group) // 2  # find the middle index
                next_level.append(group[:middle])  # add left half
                next_level.append(group[middle:])  # add right half
            else:
                next_level.append(group)  # keep single groups as they are

        if all_single:
            break  # stop when every group has one item

        current_level = next_level  # move to the next level

    return levels  # return all divide levels


def merge_sort_with_steps(stops, sorting_steps, merge_steps):
    if len(stops) <= 1:
        return stops  # a list of 1 item is already sorted

    middle = len(stops) // 2  # find the middle
    left_side = stops[:middle]  # left half
    right_side = stops[middle:]  # right half

    left_sorted = merge_sort_with_steps(left_side, sorting_steps, merge_steps)  # sort left side
    right_sorted = merge_sort_with_steps(right_side, sorting_steps, merge_steps)  # sort right side

    merged = merge(left_sorted, right_sorted)  # merge the two sorted halves

    if len(left_sorted) == 1 and len(right_sorted) == 1:
        sorting_steps.append(
            f"{format_group_numbers(left_sorted)} + {format_group_numbers(right_sorted)} → {format_group_numbers(merged)}"
        )  # save small pair sorting steps
    else:
        merge_steps.append(
            f"{format_group_numbers(left_sorted)} + {format_group_numbers(right_sorted)} → {format_group_numbers(merged)}"
        )  # save bigger merge steps

    return merged  # return the sorted merged list


def sort_input(text):
    lines = text.split("\n")  # split the textbox into lines
    stops = []  # this will store all valid stops

    for line in lines:
        if line.strip() == "":
            continue  # skip empty lines

        parts = line.split(",")  # split each line by comma

        if len(parts) != 2:
            return "please use correct format: stop name, crowd count"  # checks format

        stop_name = parts[0].strip()  # get the stop name

        if stop_name == "":
            return "please enter a stop name."  # stop name cannot be blank

        try:
            crowd_count = int(parts[1].strip())  # turn the crowd count into a whole number
        except:
            return "please make crowd count a whole number."  # error if not an integer

        if crowd_count < 0:
            return "crowd count cannot be negative."  # negative numbers are not allowed

        stops.append((stop_name, crowd_count))  # add valid stop to the list

    if len(stops) == 0:
        return "please enter at least one shuttle stop."  # user must enter something

    divide_levels = get_divide_levels(stops)  # get all splitting levels
    sorting_steps = []  # saves the first small sorting steps
    merge_steps = []  # saves the larger merge steps
    sorted_stops = merge_sort_with_steps(stops, sorting_steps, merge_steps)  # sort everything

    output = "## Shuttle Stop Crowd Ranking\n\n"  # main title

    output += "Original list:  \n"
    output += format_stops(stops) + "\n\n"  # show the starting list

    output += "### Divide\n"
    for level in divide_levels:
        formatted_groups = []  # stores each group for one divide level

        if len(level) == 1:
            output += format_numbers_line(level[0]) + "  \n"  # show the full list numbers first
        else:
            for group in level:
                formatted_groups.append(format_group_numbers(group))  # add each split group
            output += "→ " + " | ".join(formatted_groups) + "  \n"  # show the divide level

    output += "\n### Sorting\n"
    for step in sorting_steps:
        output += step + "  \n"  # show the first sorting steps

    output += "\n### Merge\n"
    for step in merge_steps:
        output += step + "  \n"  # show the bigger merge steps

    output += "\n→ " + format_numbers_line(sorted_stops) + "\n\n"  # show final sorted numbers

    output += "### Final Ranking\n"
    for stop in sorted_stops:
        output += f"{stop[0]} ({stop[1]})  \n"  # show the final sorted stop list

    return output  # send the finished output back


app = gr.Interface(
    fn=sort_input,  # this tells gradio what function to run
    inputs=gr.Textbox(
        lines=8,  # height of the input box
        label="Enter shuttle stops",  # label shown above the box
        placeholder="ARC, 67\nBioSci, 50\nStauffer, 99\nBus Loop, 12"  # example input
    ),
    outputs=gr.Markdown(label="Sorted output"),  # output will be shown as markdown
    title="Marcus DeMello's Shuttle Stop Crowd Ranking"  # app title
)

app.launch()  # starts the gradio app
