import imouse

def main():
    print("Hello from imouse-py!")
    api = imouse.api(host='localhost')
    helper = imouse.helper(api)
    device = helper.devices[0]
    print(f'{device.info}')
    ret = device.image.screenshot()
    if ret:
        print('Screenshot is successful.')
        with open('test.bmp', 'wb') as f:
            f.write(ret)
    else:
        print('Screenshot fails.')
    ret = device.mouse.swipe(imouse.types.MouseSwipeParams(direction='up', len=0.9))
    if ret:
        print('Swipe up')
    else:
        print(f'Swipe up fails: {device.error_msg}')


if __name__ == "__main__":
    main()
