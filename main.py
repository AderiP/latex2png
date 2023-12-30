import fitz  # PyMuPDFのモジュール
from PIL import Image


def save_table_as_png(pdf, bbox, output_path, margin=10):
    # 座標情報を使用して描画範囲を取得
    x0, y0, x1, y1 = bbox
    # 余白を追加
    x0 -= margin
    y0 -= margin
    x1 += margin
    y1 += margin
    rect = fitz.Rect(x0, y0, x1, y1)

    # 描画を行い、その部分を画像として取得
    pix = pdf[0].get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect)

    # PILのImageオブジェクトを作成
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

    # 透明なピクセルを特定して、それを保存時に透明にする
    transparent_color = (255, 255, 255)  # 透明にしたい色を指定
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for item in data:
        if item[:3] == transparent_color:
            new_data.append((255, 255, 255, 0))  # 透明ピクセル
        else:
            new_data.append(item)
    img.putdata(new_data)

    # 画像を保存
    img.save(output_path, format="PNG")

    pdf.close()


def main():
    input_path = 'main.pdf'
    output_path = 'table.png'
    pdf = fitz.open(input_path)
    text_page = pdf[0].get_textpage()
    boxes = text_page.extractBLOCKS()

    # boxesの座標をすべて合わせる
    x0 = min([b[0] for b in boxes])
    y0 = min([b[1] for b in boxes])
    x1 = max([b[2] for b in boxes])
    y1 = max([b[3] for b in boxes])
    bbox = (x0, y0, x1, y1)

    save_table_as_png(pdf, bbox, output_path)


if __name__ == '__main__':
    main()
