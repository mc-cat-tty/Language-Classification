# File Language Analyzer
> File Language Analyzer is a suite of Python modules, that provides objects, constants and functions, to recognise the language of a file, analyze its informations and process (elaborate and create) .csv letter frequency tables.
<br>
Keep in mind that this project is programmed very poorly, however the logic behind the adopted method is interesting.

## Table of Contents
* [Project Status](#project-status)
* [Features](#features)
* [Math behind it](#math-behind-it)
* [Technologies](#technologies)
* [Requirements](#requirements)
* [Launch](#launch)
* [Usage](#usage)

## Project Status

![License](https://img.shields.io/badge/license-MIT-brightgreen) ![build](https://img.shields.io/badge/build-passed-brightgreen) ![Version](https://img.shields.io/badge/version-1.0.0-blue)

## Features

- Recognise the language of a file
- Convert .csv frequency table to Python dictionary
- Convert Python dictionary to .csv frequency table
- Generate frequency table starting from a set of Twitter messages

## Math behind it

By analyzing the frequency of every single letter is possible to detect the language of a given text. <br>
Once the characters' frequencies have been extracted, this information can be used as a representation of the text. <br>
We want to find out which is its language, so we have to determine which is the table's column that has the nearest values. <br>
To accomplish that, it can be used the Pythagorean theorem extended to 26 dimensions, the number of letters in the Latin alphabet. <br>
By computing the distance between the given text and each language inside the table, it's possible to define which is the nearest language. <br>

## Technologies

- **_Python_** 3.x
- Python built-in libraries
- Twitter API wrapped by **_tweepy_** library
- **_wikipedia-api_** module
- **_Flask_**

## Requirements

Use one of the following commands (according to the configuration of your environment):

```sh
$ pip install -r requirements.txt
```
or

```sh
$ py -m pip install -r requirements.txt
```

## Launch

If you are in Bash-like environment with Python installed, you can run directly by typing:

```sh
$ ./Main.py
```

Otherwise, depending on your Python interpreter installation and your OS:

```sh
$ python Main.py
```
or
```sh
$ py Main.py
```
After that, go to http://127.0.0.1:5000 or http://localhost:5000 and try out the web interface.

Default frequency table is `letters_frequency_twitter.csv`

## Usage

If you want to use `tweetrain.py`'s functions, you have to insert your personal Twitter tokens.
Look at the first four uppercase variables and fill in double quotes with the proper value.
