# BUS LINE READER
This is a project developed in image processing class. It takes a bus front photo as input and use the device speaker to annouce the line name. For now, can be used to Sorocaba city lines, but can be changed to support other cities, since the bus sign is in oragne or white color. The project use the Google Vision API to try identificate the line number too.

## Setup
To run this project, you need to install python, pip, pytesseract and cv2

Use the following command to install the dependencies

```
sudo apt install python
```

```
sudo apt install python-pip
```

```
pip install pytesseract
```

```
pip install opencv-python
```

You need a Google Cloud Platform account too, to use the Google Vision API. TO create you account and get API access [click here](https://cloud.google.com/)

## Config Google Key In Yout System

Every time you open the terminal, you need to execute the following command to config the Google Key
```
export GOOGLE_APPLICATION_CREDENTIALS="<authJsonFilePath>"
```

If you don't want to execute this command every time, you can open the ./bashrc file in your computes root folder and add it at the end of file

## Running
In the project folder, execute

```
python busLineReader.py '<imageName>'
```

## Generating stats
You can only generate stats in a Linux OS. First, check the path of the bash folder in your system
```
which bash
```

copy this path in the start of file like this
```
#!<bashPath>
```

In the root folder, give permission to the stats script running the command
```
chmod 777 getStats
```

and than, execute
```
./getStats
```

P.S: It's necessary to change the attemptsNumber variable in busLineReaderStat.py file. If you are testing both methods set 33, just in local 16 and just in Google Vision API set 17.

P.S 2: <strong>Pay attention</strong> before execute the stats script. The Google Vision it's paid and you can be taxed making a high quantity of requests.
