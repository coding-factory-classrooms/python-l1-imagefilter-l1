import cv2 as cv2
import os
import sys

from app.filters_process.pipeline import pipeline as pip
from app.log.logger import transfer_log as log


def initialisation():
    """

    :return:
    """

    path = {
        "input_dir": '',
        "output_dir": '',
    }

    args = sys.argv
    log('\n----------------------\n  Running the file...\n-----------------------')
    for i, arg in enumerate(args):

        if arg == "-i":
            if i + 1 >= len(args):
                log("ERROR : IndexError : You did not provided a path.")
                return

            input_dir = args[i + 1]
            path["input_dir"] = input_dir

        if arg == "-o":
            if i + 1 >= len(args):
                log("ERROR : IndexError : You did not provided a path.")
                return

            output_dir = args[i + 1]
            path["output_dir"] = output_dir

        if arg == "-f":
            if args[i + 1] == '-h':
                print('\nList of usable filters :\n')
                print('"grayscale", ColorToGray\n"blur:integer_odd", CleanToBlur\n"dilate:integer", CleanToDilate')
                print('Usage example : -f "blur:5|grayscale"\n')
                return

        if arg == "-h":
            print("\nList of commands :")
            print("-h , --help\n-i , --input_dir <directory>\n-o , --output_dir <directory>\n--f, --filters <-h for "
                  "more help>\n")

    return path


def get_filter(argument):
    """

    :param argument:
    :return:
    """

    filter_argument = {}
    if '|' in argument:
        separated_argument = argument.split('|')
        for arg in separated_argument:
            if ':' in arg:
                temp_filter_argument = arg.split(':')
                filter_argument[str(temp_filter_argument[0])] = int(temp_filter_argument[1])
            else:
                filter_argument[str(arg)] = str(arg)
    else:
        if ':' in argument:
            temp_filter_argument = argument.split(':')
            filter_argument[str(temp_filter_argument[0])] = int(temp_filter_argument[1])
        else:
            filter_argument[str(argument)] = str(argument)

    log(f"Filters extracted and waiting to be applied : {filter_argument}")
    return filter_argument


def processing(path):
    """

    :param path:
    :return:
    """

    if path is None:
        return
    """
    
    If the path is empty : nothing happened
    """
    args = sys.argv
    for i, arg in enumerate(args):
        if arg == '--f':

            if i + 1 >= len(args):
                log("ERROR : IndexError : You did not provided a filter.")
                return
            """
            
            If the filter is unknown then an error message appears
            """

            images_list = os.listdir(path['input_dir'])
            if len(images_list) == 0:
                return log('ERROR : IndexError : The directory returned NULL.')
            """
            
            If there is no image then an error message appears
            """

            # ------------------------------------------------------------------- #

            filtered_image_directory = path['output_dir']
            if not os.path.exists(f"{filtered_image_directory}"):
                log(f'Creating directory {filtered_image_directory}...')
                os.makedirs(f"{filtered_image_directory}")
                """
                
                Tidy the filtered images in "output", if "output" doesn't exist then an "output" is created
                """

            filter_argument = get_filter(args[i + 1])

            for image in images_list:
                log(f"Opening image data from = {path['input_dir']}/{image}")
                image_read = cv2.imread(f"{path['input_dir']}/{image}")
                to_directory_filter = f"{path['output_dir']}/{image}"
                """
                
                Filter confirmation
                """

                for filter_name, argument in filter_argument.items():
                    image_read = pip(filter_name, argument, image_read)

                cv2.imwrite(to_directory_filter, image_read)
                log(f"Save result image to = {to_directory_filter}\n")
                """
                
                Put the filtered image to "output"
                """

    return 0
