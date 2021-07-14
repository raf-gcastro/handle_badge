#!/bin/bash

# 0. Define some constants
BIN_PATH="`dirname \"$0\"`"             # Directory where are the scripts
GW_DIR=$HOME/gateway                    # Directory where gateway are installed
MUNICIPIOS_YML=db/seeds/municipios.yml  # Directory where is municipios.yml
BADGES_DIR=public/images                # Directory where the badge will be stored
AUX_FILE_IMG=/tmp/aux.png               # PNG file used as auxiliar image
AUX_FILE_TXT=/tmp/city_code.txt         # TXT file used as auxiliar text file
WIDTH=120                               # Set final width image
HEIGHT=120                              # Set final height image

# 1. Get the city code
IMG_INPUT=$1                            # Get the input image name
CITY_NAME=(${IMG_INPUT//./ }[1])        # Remove the filename extension...
CITY_NAME=$(echo ${CITY_NAME} | rev | \
    cut -d/ -f1 | rev)                  # ... and the file path
python3 $BIN_PATH/get_city_code.py $GW_DIR/$MUNICIPIOS_YML \
    $CITY_NAME $AUX_FILE_TXT > /dev/tty # Call Python script that finds the city code based on city name
CITY_CODE=$(cat $AUX_FILE_TXT)          # Save the city code in a variable

# 2. Handle the badge image
IMG_OUTPUT=brasao-${CITY_CODE}.png      # Create the output name
convert $IMG_INPUT -flatten -fuzz 5% -trim +repage -resize ${WIDTH}x${HEIGHT} -background white \
    -gravity center -extent ${WIDTH}x${HEIGHT}     \
    $GW_DIR/$BADGES_DIR/$IMG_OUTPUT     # Handle image

# 3. Optimize image to reduce size
if ! [ -x "$(command -v optipng)" ]; then
    optipng -o2 $GW_DIR/$BADGES_DIR/$IMG_OUTPUT -strip all -clobber -backup
fi

# 4. Remove auxiliar files
rm $AUX_FILE_TXT

# 5. Notice the user where the file was stored
echo "Brasão salvo em:" $GW_DIR/$BADGES_DIR/$IMG_OUTPUT


