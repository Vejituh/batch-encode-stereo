#!/bin/bash

# Create output directory if it doesn't exist
if [ ! -d "out" ]; then
    mkdir "out"
fi

# Process MKV files if options.json exists
if [ -f "options.json" ]; then
    for f in *.mkv; do
        mkvmerge @options.json -o "out/$f" "$f"
        rm "$f"
    done

# Otherwise just move files except this script
else
    for f in *; do
        if [ "$f" != "mkvtoolnix.sh" ] && [ "$f" != "out" ]; then
            mv "$f" out/
        fi
    done
fi

echo "Starting Encode"

cd out
cp /home/vejituh/Documents/batch_encoder.py .
python batch_encoder.py
cd ..

read -p "Press enter to continue"
