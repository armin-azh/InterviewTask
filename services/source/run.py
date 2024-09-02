from argparse import ArgumentParser, Namespace

import cv2

import onnxruntime as ort
def main(args: Namespace)->None:

    
    source = cv2.VideoCapture(0)

    while source.isOpened():
        ret,frame = source.read()
        if not ret:
            break

        cv2.imshow('Main', frame)

        cv2.waitKey(1)


if __name__ == '__main__':
    parser = ArgumentParser()
    main(parser.parse_args())