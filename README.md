# BUS LINE READER
This is a project developed in image processing class. It takes a bus front photo as input and use the device speaker to annouce the line name. For now, can be used to Sorocaba city lines, but can be changed to support other cities, since the bus sign is in oragne or white color. The project use the Google Vision API to try identificate the line number too.

## Setup
To run this project, you need to install python, pip, pytesseract, openCV and eSpeak

Use the following command to install the dependencies

```
sudo apt install python
```
```
sudo apt install espeak
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

You need a Google Cloud Platform account too, to use the Google Vision API. To create you account and get API access [click here](https://cloud.google.com/)

## Config Google Key In Yout System

Every time you open the terminal, you need to execute the following command to config the Google Key
```
export GOOGLE_APPLICATION_CREDENTIALS="<authJsonFilePath>"
```

If you don't want to execute this command every time, you can open the ./bashrc file in your computer root folder and add it at the end of file

<strong>OBS: </strong> Professor, a chave do Google Vision API está anexa no .zip dentro da pasta jsons, então não é necessário que o senhor crie uma nova, apenas configure o caminho com o comando exports acima, porém as requisições a partir de agora estão sendo pagas, uma vez que utilizamos o limite gratuito para executar o trabalho, então se possível, não rodar o script que gera as estatísticas por completo pois isso pode nos gerar um custo alto. Acredito que seja suficiente executar o codigo original para o ver em funcionamento uma vez que os dados obtidos ao longo do experimento também estão anexados na pasta stats.

## Running
In the project folder, execute

```
python busLineReader.py '<imageName>'
```

note that the selected image has to be inside the images folder.

## Generating stats
You can only generate stats in a Linux OS. First, check the path of the bash folder in your system
```
which bash
```

copy this path in the first line of getStats file like this
```
#!<bashPath>
```

In the root folder, give permission to the stats script running the command
```
chmod 777 getStats
```

and then, execute
```
./getStats
```
This script create a file named stats.csv inside stats folder. If already have one, the file will be override.


P.S: It's necessary to change the attemptsNumber variable in busLineReaderStat.py file. If you are testing both methods set 33, just in local 16 and just in Google Vision API set 17.

P.S 2: <strong>Pay attention</strong> before execute the stats script. The Google Vision it's paid and you can be taxed making a high quantity of requests.
