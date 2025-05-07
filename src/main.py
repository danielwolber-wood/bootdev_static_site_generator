from textnode import TextNode, TextType


def main():
    tn = TextNode("text", TextType.CODE, None)
    print(tn)

if __name__ == '__main__':
    main()