#!/bin/bash
pip3 install -r requirements.txt
chmod +x decoder.py encoder.py generate_keys.py
mv decoder.py decoder
mv encoder.py encoder
mv generate_keys.py generate_keys
