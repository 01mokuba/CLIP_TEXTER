# CLIP_TEXTER
## future spec
1. get URL of PDF from DB
2. convert from PDF to text
3. put the text into ES

## current spec
- convert from PDF to text
  - put PDF file to be converted into source folder.
  - kick texter.sh with following parameters.
      - s: source PDF file
      - d: destination text file (will be created if it does not exit)

## author
- hirata_y
