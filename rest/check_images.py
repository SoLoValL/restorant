import urllib.request
r = urllib.request.urlopen('http://127.0.0.1:8000/')
html = r.read().decode()
# Count placeholder icons vs real images
placeholder_count = html.count('fa-utensils fa-3x')
media_count = html.count('/media/dishes/')
print(f"Placeholder icons: {placeholder_count}")
print(f"Media dish URLs: {media_count}")
