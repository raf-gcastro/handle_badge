#!/bin/bash

# 0. Define some constants
BIN_PATH="`dirname \"$0\"`"             # Directory where are the scripts
GW_DIR=$HOME/gateway                    # Directory where gateway are installed
MUNICIPIOS_YML=db/seeds/municipios.yml  # Directory where is municipios.yml
BADGES_DIR=public/images                # Directory where the badge will be stored
AUX_FILE_IMG=/tmp/aux.png               # PNG file used as auxiliar image
AUX_FILE_SVG=/tmp/aux.svg               # SVG file used as auxiliar vectorized image
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
python3 $BIN_PATH/remove_borders.py $IMG_INPUT \
    $AUX_FILE_IMG                       # Call Python script that remove the borders of the input badge image
inkscape -f $AUX_FILE_IMG -h $HEIGHT -w $WIDTH -l $AUX_FILE_SVG
inkscape -z -e $GW_DIR/$BADGES_DIR/$IMG_OUTPUT -w $WIDTH -h $HEIGHT $AUX_FILE_SVG


# 3. Optimize image to reduce size
if ! [ -x "$(command -v optipng)" ]; then
    optipng -o2 $GW_DIR/$BADGES_DIR/$IMG_OUTPUT -strip all -clobber -backup
fi

# 4. Remove auxiliar files
rm $AUX_FILE_SVG
rm $AUX_FILE_IMG
rm $AUX_FILE_TXT

# 5. Notice the user where the file was stored
echo "Brasão salvo em:" $GW_DIR/$BADGES_DIR/$IMG_OUTPUT


