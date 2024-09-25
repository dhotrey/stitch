# Ares

Ares will be the name of the text processor

It will be responsible
- Encoding
    - compression
    - chunking
- Decoding - done by Hephaestus
    - Putting chunks together in order
    - inflating the compressed file

# Notes on compression
- Using pure go implementation of xz utils
