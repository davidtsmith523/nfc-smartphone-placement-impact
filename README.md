<h1 align="center">
    Impact of Smartphone NFC Placement
</h1>

This is a project to analyze NFC placement on smartphones. We use a github repository that collected the NFC positions on 116 smartphones. Our goal was to use concepts and equations learned in class to conclude an optimal NFC placement on a smartphone.

To find the most optimal placement a few techniques were used:

1. Path Loss Calculation Program

- This uses the Friis equation to calculate the path loss of each NFC placement in the smartphone.
  - A standard phone is used for the width (75mm) and height (150mm).
  - The receiver is placed 4cm from the head of the phone.
  - The reciever is assumed to be 75mm x 75mm.
  - The reciever gain is fixed since the receiver area is fixed.
  - The transmitted gain is scaled based on the size of the NFC in each smartphone.

2. Signal Strength Calculation Program

- This uses the formula Pr = Pt - PL to find the most optimal NFC placement
  - For PL, the same formula from above is used.
  - For Pt, an average NFC size and power is used and then scaled based on the size of NFC in each smartphone

## Technologies Used

- [Python](https://www.python.org/)

## Development

To get a local copy of the code, clone it using git:

```
git clone https://github.com/davidtsmith523/nfc-smartphone-placement-impact.git
```

### Running Path Loss Calulcations

```
python PathLoss-Algo.py
```

### Running Signal Strength Calulcations

```
python SignalStrength-Algo.py
```
