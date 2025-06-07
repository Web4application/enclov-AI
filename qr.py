import qrcode
import io

def print_qr(command="start"):
    url = f"https://web4application.github.io/enclovAI/enclov-{command}.html"
    qr = qrcode.QRCode(box_size=1, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # print QR in terminal with unicode blocks
    import sys
    qr.print_ascii(out=sys.stdout)

    print(f"\nOpen manual page: {url}")

# Use in help output
print_qr("start")
