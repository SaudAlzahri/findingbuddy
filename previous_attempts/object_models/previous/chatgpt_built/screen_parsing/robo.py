
from kora.drive import upload_public
url = upload_public('data/video/cars.mp4')

from IPython.display import HTML
HTML(f"""<video src={url} width=500 controls/>""")