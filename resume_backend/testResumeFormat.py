from resumeTextExtract import Resume


def main():
    paul_res = Resume("../Resume_Paul_Flanagan.pdf")
    print(paul_res.text)


if __name__ == "__main__":
    main()
