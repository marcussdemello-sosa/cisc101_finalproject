# Shuttle Stop Crowding Ranking using Merge Sort

def merge_sort(stops):
    # if the list has 1 item or less, it is already sorted
    if len(stops) <= 1:
        return stops

    # find the middle of the list
    middle = len(stops) // 2

    # split the list into 2 smaller lists
    left_side = stops[:middle]
    right_side = stops[middle:]

    # sort both halves
    left_side = merge_sort(left_side)
    right_side = merge_sort(right_side)

    # merge the sorted halves
    return merge(left_side, right_side)


def merge(left, right):
    new_list = []

    i = 0
    j = 0

    # compare the crowd counts from both lists
    while i < len(left) and j < len(right):
        if left[i][1] < right[j][1]:
            new_list.append(left[i])
            i = i + 1
        else:
            new_list.append(right[j])
            j = j + 1

    # add the rest of the left list if there is anything left
    while i < len(left):
        new_list.append(left[i])
        i = i + 1

    # add the rest of the right list if there is anything left
    while j < len(right):
        new_list.append(right[j])
        j = j + 1

    return new_list


import gradio as gr

def sort_input(text):
    lines = text.split("\n")
    stops = []

    for line in lines:
        if line.strip() == "":
            continue

        parts = line.split(",")

        if len(parts) != 2:
            return "please use correct format: stop name, crowd count"

        stop_name = parts[0].strip()

        try:
            crowd_count = int(parts[1].strip())
        except:
            return "please make crowd count a whole number."

        stops.append((stop_name, crowd_count))

    sorted_stops = merge_sort(stops)

    output = ""
    for stop in sorted_stops:
        output += stop[0] + " - " + str(stop[1]) + "\n"


    return output

app = gr.Interface(
    fn=sort_input,
    inputs=gr.Textbox(lines=8, label="Enter shuttle stops"),
    outputs=gr.Textbox(lines=8, label="Sorted output"),
    title="Marcus DeMello's Shuttle Stop Crowd Ranking"
)

app.launch()
