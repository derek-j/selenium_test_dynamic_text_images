import unittest
from selenium import webdriver
import time
import re

"""
    Author Derek Johnson
    408-836-9698
    Coding Challenge using this url:  https://the-internet.herokuapp.com/dynamic_content
    3/13/2020
"""


class TestSuite(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.addCleanup(self.driver.quit)

    def test_01_lorem_ipsum_text(self):
        """
        Coding Challenge 1:
        Assert that the dynamic text (the lorem ipsum text block) on the page contains a word
        at least 10 characters in length.
        Stretch goal:
            Print the longest word on the page.  I'm Printing all of the longest words on the page!
        :return:
        """
        print("\nRunning test: test_01_lorem_ipsum_text")
        self.driver.get('https://the-internet.herokuapp.com/dynamic_content')
        time.sleep(5)

        def print_max_word_len_and_words_that_size(text_string):
            # Create an array of "tuples" of [(len, "word") ... (len, "word")]
            len_word_array = [(len(element), element) for element in text_string]

            # Find the maximum word length and create an array of all words which match the longest word length.
            max_word_len = 0
            word_list = []
            for i in range(len(len_word_array)):
                #print("{}: {} - {}".format(i, len_word_array[i][0], len_word_array[i][1]))
                if len_word_array[i][0] > max_word_len:
                    max_word_len = len_word_array[i][0]
                    word_list = []
                    word_list.append(len_word_array[i][1])
                elif len_word_array[i][0] == max_word_len:
                    if len_word_array[i][1] not in word_list:  # Don't add duplicates
                        word_list.append(len_word_array[i][1])

            # Stretch Goal:
            # NOTE: I'm making an assumption here and printing ALL words of the longest length, without duplicates.
            print("Stretch Goal:  Largest word(s) of length {} are: {}".format(max_word_len, word_list))

            # Goal:  Assert that the text has a word is at least 10 characters long
            self.assertTrue(max_word_len >= 10, "No words have 10 characters in them")
            print("Largest Word length = {}".format(max_word_len))

        # Create a list of the Text Fields to find longest string.
        texts = self.driver.find_elements_by_class_name("large-10.columns")
        print_max_word_len_and_words_that_size(texts[0].text.split())  # All text fields
        #print_max_word_len_and_words_that_size(texts[1].text.split()) # First text field
        #print_max_word_len_and_words_that_size(texts[2].text.split()) # Second text field
        #print_max_word_len_and_words_that_size(texts[3].text.split()) # Third text field


    def test_02_punisher_not_found_print_image_names(self):
        """
        Coding Challenge 2:
        Assert that the "Punisher" image (silhouette with a skull on his chest) does not appear on the page.
        This test may pass or fail on any given execution depending on whether the punisher happens to be on the page.
        1- check for it in the filename

        Stretch Goal:
        2- Create names for each image and print the names for the Avatars which appear.
        :return:
        """
        print("\nRunning test: test_02_punisher_not_found_print_image_names")
        self.driver.get('https://the-internet.herokuapp.com/dynamic_content')
        time.sleep(5)

        # Create a dictionary to map filename to name.
        # For completeness purposes, I'm going to assume other images might be in the folder and could get chosen.
        # If that occurs, any unknown file will default to "unknown"
        image_names = {"Original-Facebook-Geek-Profile-Avatar-1.jpg": "Mario",
                       "Original-Facebook-Geek-Profile-Avatar-2.jpg": "Boba Fett",
                       "Original-Facebook-Geek-Profile-Avatar-3.jpg": "Punisher",
                       "Original-Facebook-Geek-Profile-Avatar-4.jpg": "Missing Avatar-4",
                       "Original-Facebook-Geek-Profile-Avatar-5.jpg": "Hawk-Punisher",
                       "Original-Facebook-Geek-Profile-Avatar-6.jpg": "StormTrooper",
                       "Original-Facebook-Geek-Profile-Avatar-7.jpg": "Jester"}

        # NOTE:  I made several attempts to get the filename of the image.  but all failed,
        # Maybe there is a way in selenium to get at it from this info, but I wasn't able to quickly determine that.
        # Attempt 1: get by class name
        # This gets the 3 images I want, but I'm not sure where to extract the filename?
        # images_class = self.driver.find_elements_by_class_name("large-2.columns")

        # Attempt 2: get by full xpath (same as above)
        # img1 = self.driver.find_elements_by_xpath("/html/body/div[2]/div/div/div/div/div[1]/div[1]/img")
        # img2 = self.driver.find_elements_by_xpath("/html/body/div[2]/div/div/div/div/div[1]/div[2]/img")
        # img3 = self.driver.find_elements_by_xpath("/html/body/div[2]/div/div/div/div/div[1]/div[3]/img")

        # Attempt 3:  Try parsing xml file with ElementTree
        # tree = etree.fromstringlist(driver.page_source)
        # The above give me this parsing error. (ie, a BUG in the returned xml.)
        # xml.etree.ElementTree.ParseError: mismatched tag: line 15, column 4

        # Attempt 4:  Just parse the page source myself.
        lines = self.driver.page_source.splitlines()
        found_punisher = False
        print("Stretch Goal:  Print Names of Images")
        for l in lines:
            # Extract just the "<filename>.jpg"
            searchResult = re.search(r'(^.*/img/avatars/)(.*jpg)(.*$)', l, re.M | re.I)
            if searchResult is not None:
                filename = searchResult.group(2)
                try:
                    image_name = image_names[filename]
                    if image_name == "Punisher":
                        found_punisher = True
                except KeyError:
                    image_name = "unknown image for file: " + filename

                print("Found image: {}".format(image_name))
        self.assertFalse(found_punisher, "Failed, found the Punisher image on the screen")

if __name__ == '__main__':
    unittest.main()
